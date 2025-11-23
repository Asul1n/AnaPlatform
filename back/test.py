# stp_pipeline.py
from __future__ import annotations
from typing import Any, Dict, List, Tuple, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Body, HTTPException
import os
import subprocess
import json

# ------------------------
# Pydantic models (input)
# ------------------------
class NodeModel(BaseModel):
    id: str
    type: str
    params: Optional[Dict[str, Any]] = None
    bits: Optional[int] = None
    inputs: Optional[List[str]] = None
    outputs: Optional[List[str]] = None

class EdgeModel(BaseModel):
    source: str
    target: str
    source_port: Optional[str] = None
    target_port: Optional[str] = None

class GraphSpec(BaseModel):
    algorithm: Optional[str] = None
    block_size: int
    word_size: Optional[int] = None
    rounds: Optional[int] = 1
    nodes: List[NodeModel]
    edges: List[EdgeModel]
    inputs: Optional[List[str]] = None
    outputs: Optional[List[str]] = None
    variables: Optional[Dict[str, Dict[str, Any]]] = None
    stp_semantics: Optional[Dict[str, str]] = None

# ------------------------
# Utility helpers
# ------------------------
def ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)

# ------------------------
# Graph parsing + topo sort
# ------------------------
class GraphParser:
    def __init__(self, spec: GraphSpec):
        self.spec = spec
        # map node id -> NodeModel
        self.node_map = {n.id: n for n in spec.nodes}
        self.adj: Dict[str, List[str]] = {}
        self.indeg: Dict[str, int] = {}
        self._build_graph()

    def _build_graph(self):
        # init nodes (include inputs and outputs as nodes)
        ids = set(self.node_map.keys())
        if self.spec.inputs:
            ids.update(self.spec.inputs)
        if self.spec.outputs:
            ids.update(self.spec.outputs)
        for id_ in ids:
            self.adj[id_] = []
            self.indeg[id_] = 0
        # add edges
        for e in self.spec.edges:
            s, t = e.source, e.target
            if s not in self.adj:
                self.adj[s] = []
                self.indeg[s] = self.indeg.get(s, 0)
            if t not in self.adj:
                self.adj[t] = []
                self.indeg[t] = self.indeg.get(t, 0)
            self.adj[s].append(t)
            self.indeg[t] = self.indeg.get(t, 0) + 1

    def topo_sort(self) -> List[str]:
        # Kahn's algorithm
        queue = [n for n, d in self.indeg.items() if d == 0]
        order: List[str] = []
        while queue:
            u = queue.pop(0)
            order.append(u)
            for v in self.adj.get(u, []):
                self.indeg[v] -= 1
                if self.indeg[v] == 0:
                    queue.append(v)
        # if cycle detection
        if len(order) != len(self.adj):
            raise ValueError("Graph has a cycle or disconnected components")
        return order

# ------------------------
# IR Builder -> STP templates
# ------------------------
class NodeRegistry:
    """
    Registry mapping node types to STP template generators.
    Each generator returns list[str] of STP assertions/decls.
    """
    def __init__(self, spec: GraphSpec):
        self.spec = spec
        # default semantics (can be overridden per-spec)
        self.semantics = spec.stp_semantics or {
            "ROTATE_LEFT": "(ASSERT (= {out} (bvrol {in} {amount})));",
            "ROTATE_RIGHT": "(ASSERT (= {out} (bvror {in} {amount})));",
            "ADD_MOD": "(ASSERT (= {out} (bvadd {a} {b})));",
            "XOR": "(ASSERT (= {out} (bvxor {a} {b})));",
            "AND": "(ASSERT (= {out} (bvand {a} {b})));",
            "OR": "(ASSERT (= {out} (bvor {a} {b})));",
            "SBOX": "//SBOX_PLACEHOLDER",
            "SWAP": "//SWAP_PLACEHOLDER",
            "INPUT": "//INPUT_PLACEHOLDER",
            "OUTPUT": "//OUTPUT_PLACEHOLDER",
            "KEY_PART": "//KEY_PART_PLACEHOLDER"
        }

    def declare_bitvec(self, name: str, width: int) -> str:
        # declaration line (STP/YOUR dialect)
        return f"{name} : BITVECTOR({width});"

    def gen_rotate_left(self, out: str, inp: str, amount: int) -> List[str]:
        """
        生成 ROTATE_LEFT 的汇编/伪代码文本。
        解决点：不能使用关键字名 'in'，所以使用 dict 解包传参给 str.format。
        """
        tpl = self.semantics.get("ROTATE_LEFT")
        if tpl is None:
            raise KeyError("semantics 中缺少 'ROTATE_LEFT' 模板")

        # 如果模板可能是列表，统一处理成字符串列表
        if isinstance(tpl, list):
            # 把每个模板都格式化后返回
            return [t.format(**{"out": out, "in": inp, "amount": amount}) for t in tpl]

        if not isinstance(tpl, str):
            raise TypeError("ROTATE_LEFT 模板应为字符串或字符串列表")

        # 使用字典方式给 format 传参，避免关键字参数名冲突
        formatted = tpl.format(**{"out": out, "in": inp, "amount": amount})
        return [formatted]

    def gen_add_mod(self, out: str, a: str, b: str) -> List[str]:
        tpl = self.semantics["ADD_MOD"]
        return [tpl.format(out=out, a=a, b=b)]

    def gen_xor(self, out: str, a: str, b: str) -> List[str]:
        tpl = self.semantics["XOR"]
        return [tpl.format(out=out, a=a, b=b)]

    def gen_sbox_lut(self, out: str, inp: str, table: List[int], in_w: int = 4) -> List[str]:
        # produce disjunction of input->output mappings, input/out in binary literal
        parts: List[str] = []
        for i, o in enumerate(table):
            in_bin = format(i, f"0{in_w}b")
            out_bin = format(o, f"0{in_w}b")
            parts.append(f"({inp} = 0bin{in_bin} & {out} = 0bin{out_bin})")
        clause = " | ".join(parts)
        return [f"ASSERT({clause});"]

    def gen_split(self, src: str, parts: List[Tuple[str,int]]) -> List[str]:
        # parts: list of (name, width)
        # split via extract, we assume MSB-first indexing: src[MSB:..]
        lines: List[str] = []
        total = sum(w for _, w in parts)
        hi = total - 1
        offset = 0
        # we assume parts are ordered [high..low] if needed adjust
        for name, width in parts:
            lo = hi - width + 1
            lines.append(f"ASSERT({name} = {src}[{hi}:{lo}]);")
            hi = lo - 1
        return lines

    def gen_merge(self, out: str, parts: List[Tuple[str,int]]) -> List[str]:
        # BVCONCAT(order high->low)
        args = ", ".join(p for p,_ in parts)
        return [f"ASSERT({out} = BVCONCAT({args}));"]

# ------------------------
# STP generator
# ------------------------
class STPGenerator:
    def __init__(self, spec: GraphSpec):
        self.spec = spec
        self.registry = NodeRegistry(spec)
        self.decls: Dict[str,int] = {}  # name -> width
        self.lines: List[str] = []

    def declare_if_needed(self, name: str, width: int) -> None:
        if name not in self.decls:
            self.decls[name] = width

    def build_declarations(self) -> None:
        # declare inputs, variable placeholders
        # inputs from spec.inputs and spec.variables
        if self.spec.inputs:
            for inp in self.spec.inputs:
                self.declare_if_needed(inp, self.spec.word_size or 16)
        if self.spec.variables:
            for k,v in self.spec.variables.items():
                bits = int(v.get("bits", self.spec.word_size or 16))
                self.declare_if_needed(k, bits)
        # also declare node outputs if they have bits
        for n in self.spec.nodes:
            if n.bits:
                self.declare_if_needed(n.id, n.bits)

    def render_declarations(self) -> List[str]:
        decls: List[str] = []
        for name,width in self.decls.items():
            decls.append(self.registry.declare_bitvec(name, width))
        return decls

    def find_node_by_id(self, node_id: str) -> Optional[NodeModel]:
        for n in self.spec.nodes:
            if n.id == node_id:
                return n
        return None

    def node_inputs(self, node_id: str) -> List[str]:
        # gather incoming edges to node
        ins: List[str] = []
        for e in self.spec.edges:
            if e.target == node_id:
                ins.append(e.source)
        return ins

    def node_outputs(self, node_id: str) -> List[str]:
        outs: List[str] = []
        for e in self.spec.edges:
            if e.source == node_id:
                outs.append(e.target)
        return outs

    def generate_for_graph(self) -> str:
        # main entry: generate declarations + body
        self.build_declarations()
        body: List[str] = []
        body += self.render_declarations()
        # topological order
        parser = GraphParser(self.spec)
        try:
            order = parser.topo_sort()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # Process nodes in topological order; skip raw inputs which are declared
        for node_id in order:
            node = self.find_node_by_id(node_id)
            if node is None:
                # could be input/output/variable; skip
                continue
            typ = node.type.upper()
            # assume width
            width = int(node.bits) if node.bits else (self.spec.word_size or 16)
            # determine incoming names (prefer explicit node.inputs if present else edges)
            ins = node.inputs or self.node_inputs(node.id)
            outs = node.outputs or self.node_outputs(node.id)

            # declare outs
            for out in outs:
                self.declare_if_needed(out, width)

            # map templates
            if typ == "ROTATE_LEFT":
                # expects 1 input, 1 output
                if not ins:
                    raise HTTPException(status_code=400, detail=f"ROTATE_LEFT {node.id} has no input")
                inp = ins[0]
                out = outs[0] if outs else node.id + "_out"
                amount = int(node.params.get("amount", 1) if node.params else 1)
                body += self.registry.gen_rotate_left(out, inp, amount)
            elif typ == "ADD_MOD":
                # expects 2 inputs
                if len(ins) < 2:
                    raise HTTPException(status_code=400, detail=f"ADD_MOD {node.id} needs 2 inputs")
                a,b = ins[0], ins[1]
                out = outs[0] if outs else node.id + "_out"
                body += self.registry.gen_add_mod(out, a, b)
            elif typ == "XOR":
                if len(ins) < 2:
                    raise HTTPException(status_code=400, detail=f"XOR {node.id} needs 2 inputs")
                a,b = ins[0], ins[1]
                out = outs[0] if outs else node.id + "_out"
                body += self.registry.gen_xor(out, a, b)
            elif typ == "SBOX":
                if len(ins) < 1:
                    raise HTTPException(status_code=400, detail=f"SBOX {node.id} needs 1 input")
                a = ins[0]
                out = outs[0] if outs else node.id + "_out"
                table = node.params.get("table") if node.params else None
                if not table:
                    raise HTTPException(status_code=400, detail=f"SBOX {node.id} missing table param")
                body += self.registry.gen_sbox_lut(out, a, table, in_w=node.bits or 4)
            elif typ == "SWAP":
                # map outputs to inputs in order
                # gather ins (two inputs expected)
                ins_all = ins
                outs_all = outs
                if len(ins_all) < 2 or len(outs_all) < 2:
                    # might be special syntax (swap node outputs specified like swapL.out0 target etc)
                    # fallback: if node has explicit outputs, assign mapping in order
                    pass
                else:
                    # equality mapping
                    body.append(f"ASSERT({outs_all[0]} = {ins_all[0]});")
                    body.append(f"ASSERT({outs_all[1]} = {ins_all[1]});")
            elif typ in ("INPUT", "OUTPUT", "KEY_PART"):
                # declaration already handled
                continue
            else:
                raise HTTPException(status_code=400, detail=f"Unknown node type: {typ}")

        # join body lines
        stp_text = "\n".join(body)
        return stp_text

# ------------------------
# STP writer + executor
# ------------------------
class STPWriter:
    def __init__(self, out_path: str):
        self.out_path = out_path

    def write(self, content: str) -> str:
        ensure_dir(self.out_path)
        with open(self.out_path, "w") as f:
            f.write(content)
        return self.out_path

class STPExecutor:
    def __init__(self, stp_bin: str = "stp"):
        self.stp_bin = stp_bin

    def run(self, file_path: str, timeout: Optional[int] = 60) -> Tuple[int, str, str]:
        # call external stp; returns (retcode, stdout, stderr)
        try:
            p = subprocess.run([self.stp_bin, file_path], capture_output=True, text=True, timeout=timeout)
            return (p.returncode, p.stdout, p.stderr)
        except FileNotFoundError:
            return (-1, "", f"stp binary not found: {self.stp_bin}")
        except subprocess.TimeoutExpired:
            return (-2, "", "timeout")

# ------------------------
# FastAPI app
# ------------------------
app = FastAPI(title="Graph->STP pipeline")

@app.post("/generate_stp")
def generate_stp(spec: GraphSpec = Body(...), filename: Optional[str] = "model.cvc"):
    gen = STPGenerator(spec)
    try:
        stp_text = gen.generate_for_graph()
    except HTTPException as e:
        raise e
    out_path = os.path.abspath(filename)
    writer = STPWriter(out_path)
    writer.write(stp_text)
    return {"path": out_path, "size": len(stp_text)}

@app.post("/run_stp")
def run_stp(spec: GraphSpec = Body(...), filename: Optional[str] = "model.cvc"):
    # generate then run
    gen = STPGenerator(spec)
    stp_text = gen.generate_for_graph()
    out_path = os.path.abspath(filename)
    STPWriter(out_path).write(stp_text)
    execer = STPExecutor()
    rc, out, err = execer.run(out_path)
    return {"rc": rc, "stdout": out, "stderr": err, "path": out_path}

# ------------------------
# Example helper (local CLI)
# ------------------------
if __name__ == "__main__":
    # quick test: load example JSON file 'example.json' and produce model.cvc
    import sys
    if len(sys.argv) < 2:
        print("usage: python stp_pipeline.py example.json")
        raise SystemExit(1)
    with open(sys.argv[1], "r") as f:
        j = json.load(f)
    spec = GraphSpec(**j)
    gen = STPGenerator(spec)
    stp = gen.generate_for_graph()
    out = "out_model.cvc"
    STPWriter(out).write(stp)
    print("wrote", out)

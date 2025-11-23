from typing import Dict, List
from fastapi import HTTPException
from models import GraphSpec
from models import NodeModel as Node
from models import EdgeModel as Edge

""" 有向图解析器 """
class GraphParser:
    # 初始化图结构
    def __init__(self, spec: GraphSpec):
        self.spec = spec                               # 存储视图
        self.node_map = {n.id: n for n in spec.nodes}  
        self.adj: Dict[str, List[str]] = {}            # 邻接表，用字典记录每个节点的出边
        self.indeg: Dict[str, int] = {}                # 入读表，每个节点被指向的次数
        self._build_graph()
    
    # 构建邻接表
    def _build_graph(self):
        ids = set(self.node_map.keys())
        if self.spec.inputs:
            ids.update(self.spec.inputs)
        if self.spec.outputs:
            ids.update(self.spec.outputs)
        # 把变量（如 subkey_L，subkey_R）也纳入节点集合
        if self.spec.variables:
            ids.update(self.spec.variables.keys())
            
        for id_ in ids:
            self.adj[id_] = []
            self.indeg[id_] = 0
        for e in self.spec.edges:
            s, t = e.source, e.target
            self.adj.setdefault(s, [])
            self.indeg.setdefault(t, 0)
            self.adj[s].append(t)
            self.indeg[t] += 1
            
    # 拓扑排序
    def topo_sort(self) -> List[str]:
        print("Adjacency list:", self.adj)
        print("Indegree:", self.indeg)
        queue = [n for n, d in self.indeg.items() if d == 0]
        print("Initial zero-indegree nodes:", queue)
        order: List[str] = []
        while queue:
            u = queue.pop(0)
            order.append(u)
            for v in self.adj.get(u, []):
                self.indeg[v] -= 1
                if self.indeg[v] == 0:
                    queue.append(v)
        print("Topo order:", order)
        if len(order) != len(self.adj):
            remaining = [k for k, v in self.indeg.items() if v > 0]
            print("❌ Remaining nodes with indegree > 0:", remaining)
            raise HTTPException(status_code=400, detail="Graph has a cycle")
        return order



def test_graph_ballet():
    json_data = {
        "algorithm": "Ballet",
        "block_size": 64,
        "word_size": 16,
        "rounds": 2,

        "nodes": [
            { "id": "X0", "type": "INPUT", "bits": 16 },
            { "id": "X1", "type": "INPUT", "bits": 16 },
            { "id": "X2", "type": "INPUT", "bits": 16 },
            { "id": "X3", "type": "INPUT", "bits": 16 },

            { "id": "rot6", "type": "ROTATE_LEFT", "params": { "amount": 6 } },
            { "id": "rot15", "type": "ROTATE_LEFT", "params": { "amount": 15 } },

            { "id": "sumL", "type": "ADD_MOD", "params": { "mod": "2^16" } },
            { "id": "sumR", "type": "ADD_MOD", "params": { "mod": "2^16" } },

            { "id": "xorL", "type": "XOR" },
            { "id": "xorR", "type": "XOR" },

            { "id": "rot9", "type": "ROTATE_LEFT", "params": { "amount": 9 } },
            { "id": "rot14", "type": "ROTATE_LEFT", "params": { "amount": 14 } },

            { "id": "swapL", "type": "SWAP" },
            { "id": "swapR", "type": "SWAP" },

            { "id": "Y0", "type": "OUTPUT", "bits": 16 },
            { "id": "Y1", "type": "OUTPUT", "bits": 16 },
            { "id": "Y2", "type": "OUTPUT", "bits": 16 },
            { "id": "Y3", "type": "OUTPUT", "bits": 16 }
        ],

        "edges": [
            { "source": "X0", "target": "rot6" },
            { "source": "X2", "target": "rot15" },

            { "source": "rot6", "target": "sumL" },
            { "source": "X1", "target": "sumL" },
            { "source": "rot15", "target": "sumR" },
            { "source": "X3", "target": "sumR" },

            { "source": "sumL", "target": "xorL" },
            { "source": "sumR", "target": "xorR" },
            { "source": "subkey_L", "target": "xorL" },
            { "source": "subkey_R", "target": "xorR" },

            { "source": "xorL", "target": "rot9" },
            { "source": "xorR", "target": "rot14" },

            { "source": "rot9", "target": "swapL" },
            { "source": "X1", "target": "swapL" },
            { "source": "rot14", "target": "swapR" },
            { "source": "X3", "target": "swapR" },

            { "source": "swapL", "target": "Y0" },
            { "source": "swapL", "target": "Y1" },
            { "source": "swapR", "target": "Y2" },
            { "source": "swapR", "target": "Y3" }
        ],

        "variables": {
            "subkey_L": { "type": "KEY_PART", "bits": 16 },
            "subkey_R": { "type": "KEY_PART", "bits": 16 }
        }
    }


    # 构造 GraphSpec 对象
    nodes = [Node(**n) for n in json_data["nodes"]]
    edges = [Edge(**e) for e in json_data["edges"]]
    spec = GraphSpec(
        algorithm=json_data["algorithm"],
        block_size=json_data["block_size"],
        word_size=json_data["word_size"],
        rounds=json_data["rounds"],
        nodes=nodes,
        edges=edges,
        variables=json_data["variables"]
    )

    # 执行解析
    parser = GraphParser(spec)
    topo_order = parser.topo_sort()

    print("✅ Ballet 图结构拓扑排序结果：")
    for i, node_id in enumerate(topo_order, 1):
        print(f"{i:2d}. {node_id}")

# ------------------------------
# 主程序入口
# ------------------------------
if __name__ == "__main__":
    test_graph_ballet()
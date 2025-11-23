

class Node:
    """ 单个节点的结构定义 """
    def __init__(self, node_id, node_type, params=None):
        self.id = node_id
        self.type = node_type
        self.params = params or {}
        self.inputs = []
        self.outputs = []
        
    def __repr__(self):
        return (f"<Node id={self.id}, type={self.type}, "
                f"inputs={self.inputs}, outputs={self.outputs}, params={self.params}>")

class NodeRegistry:
    """ 通用节点注册表，用于存储和查询每个节点的属性 """
    def __init__(self, json_spec: dict):
        self.nodes = {}
        self.alias_map = {}    # 记录变量别名映射
        self._build(json_spec)
        
    def _build(self, spec: dict):
        # 初始化所有节点
        for node in spec["nodes"]:
            self.nodes[node["id"]] = Node(
                node_id=node["id"],
                node_type=node["type"],
                params=node.get("params")
            )
            
        # 预扫描所有边，判断是否为“变量对变量”连接
        raw_edges = spec["edges"]
        merged_edges = []

        for e in raw_edges:
            src, dst = e["source"], e["target"]

            # 判断 source、target 是否都是“外部变量”或未注册节点
            is_src_ext = src not in self.nodes or self.nodes[src].type == "EXTERNAL"
            is_dst_ext = dst not in self.nodes or self.nodes[dst].type == "EXTERNAL"

            # ✅ 若两端都不是组件节点（即无功能性操作），则视为变量等价
            if is_src_ext and is_dst_ext:
                # 把 dst 映射到 src
                self.alias_map[dst] = self.alias_map.get(src, src)
            else:
                merged_edges.append((src, dst))

        # 构建输入输出连接表 ---
        for src, dst in merged_edges:
            # 若存在别名映射，则替换真实变量名
            src = self.alias_map.get(src, src)
            dst = self.alias_map.get(dst, dst)

            if src not in self.nodes:
                self.nodes[src] = Node(src, "EXTERNAL")
            if dst not in self.nodes:
                self.nodes[dst] = Node(dst, "EXTERNAL")

            # 构建连接关系
            if dst not in self.nodes[src].outputs:
                self.nodes[src].outputs.append(dst)
            if src not in self.nodes[dst].inputs:
                self.nodes[dst].inputs.append(src)

        # 注册额外变量（如 subkey_L、subkey_R）---
        if "variables" in spec:
            for vid, var in spec["variables"].items():
                if vid not in self.nodes:
                    self.nodes[vid] = Node(vid, var["type"], {"bits": var["bits"]})
                    
    def __getitem__(self, node_id):
        """支持 registry[node_id] 直接访问"""
        return self.nodes[self.alias_map.get(node_id, node_id)]

    def __iter__(self):
        return iter(self.nodes.values())

    # --- 可视化摘要 ---
    def summary(self):
        print(f"{'节点ID':<12} | {'类型':<15} | {'输入':<25} | {'输出':<25} | 参数")
        print("-" * 90)
        for node in self.nodes.values():
            print(f"{node.id:<12} | {node.type:<15} | "
                  f"{str(node.inputs):<25} | {str(node.outputs):<25} | {node.params}")

        # 打印别名映射表
        if self.alias_map:
            print("\n🔁 变量映射表（已合并变量）:")
            for k, v in self.alias_map.items():
                print(f"  {k} → {v}")
    
    def __len__(self):
        """返回节点总数"""
        return len(self.nodes)


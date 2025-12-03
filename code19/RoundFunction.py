import collections

class RoundGraphParser:
    def __init__(self, json_data, parent_solver):
        """
        :param json_data: 前端传来的完整JSON对象
        :param parent_solver: Difference类的实例，用于调用父类的方法(如modulo_addition)
        """
        self.data = json_data
        self.solver = parent_solver
        self.nodes = {n['id']: n for n in json_data['roundFunction']['nodes']}
        self.edges = json_data['roundFunction']['edges']
        
        # 预处理：构建邻接表，方便查找输入源
        # target_node_id -> list of source_node_ids
        self.incoming_edges = collections.defaultdict(list)
        for edge in self.edges:
            # edge['target'] 可能是 "NodeID" 也可能是 "NodeID_portName"
            # 我们需要解析出 NodeID
            target_raw = edge['target']
            source_id = edge['source']
            
            # 简单处理：假设 ID 不包含 "_" 或者通过匹配节点列表来确定 ID
            # 更加稳健的方法是遍历所有 nodes 的 ID 进行匹配
            target_id = self._extract_node_id(target_raw)
            self.incoming_edges[target_id].append(source_id)

        # 获取拓扑排序序列，确定计算顺序
        self.execution_order = self._topological_sort()

    def _extract_node_id(self, target_str):
        """
        从 'NodeID_input1' 或 'NodeName_input1' 中提取真正的 'NodeID'
        """
        # 情况 1: target_str 本身就是 ID
        if target_str in self.nodes:
            return target_str
        
        # 情况 2: 尝试通过分割 "_" 来获取 ID (处理 NodeID_PortID 格式)
        # 例如: "k3xAp5..._input1" -> "k3xAp5..."
        if "_" in target_str:
            potential_id = target_str.rsplit("_", 1)[0] # 从右边切掉最后一个 _ 后的内容
            if potential_id in self.nodes:
                return potential_id
            # 或者是 "NodeID_input_1" 这种多下划线的情况，尝试前缀匹配
            for node_id in self.nodes:
                if target_str.startswith(node_id):
                    return node_id

        # 情况 3: 尝试通过 "节点名称" (Name) 来查找对应的 ID
        # 很多时候前端传的是 "XOR1_input1"，但 ID 其实是乱码 UUID
        for node_id, node_data in self.nodes.items():
            name = node_data.get('name')
            if name:
                # 检查 target 是否以该节点的 Name 开头
                # 例如 target="XOR1_input1", name="XOR1"
                if target_str == name or target_str.startswith(name + "_") or target_str.startswith(name + "-"):
                    return node_id
        
        # 情况 4: 暴力前缀匹配 (作为最后的手段)
        # 如果 ID 是 "abc"，target 是 "abcd"，这可能会误判，所以放在最后
        for node_id in self.nodes:
            if target_str.startswith(node_id):
                return node_id

        # 如果实在找不到，打印调试信息并返回原字符串(这会导致后面的 KeyError)
        print(f"[!] 警告: 无法解析目标节点: {target_str}")
        return target_str

    def _topological_sort(self):
        """对节点进行拓扑排序，确保先处理输入，再处理中间节点"""
        in_degree = {node_id: 0 for node_id in self.nodes}
        graph = collections.defaultdict(list)
        
        for edge in self.edges:
            u = edge['source']
            v = self._extract_node_id(edge['target'])
            graph[u].append(v)
            in_degree[v] += 1
            
        queue = [n for n in in_degree if in_degree[n] == 0]
        order = []
        
        while queue:
            u = queue.pop(0)
            order.append(u)
            for v in graph[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
                    
        return order

    def _get_rotate_constraint(self, src_var, dst_var, props):
        """生成循环移位的约束 (CVC语法)"""
        # 注意：STP 的 BITVECTOR 索引通常是 [high:low]
        # 假设 bitwidth 是 128
        width = props.get('bitwidth', 128)
        offset = int(props.get('offset', 0))
        direction = props.get('direction', 'left')
        
        offset = offset % width
        if offset == 0:
            return [f"ASSERT({dst_var} = {src_var});"]

        # 差分分析中，循环移位是线性的，输入差分移位等于输出差分
        # CVC 拼接语法通常是 @ 或 concat
        # Left Rotate n: A[width-n-1 : 0] @ A[width-1 : width-n]
        
        if direction == 'left':
            # 举例 8bit 左移 2: 76543210 -> 54321076
            # split point = width - offset
            high_part = f"{src_var}[{width - offset - 1}:0]"
            low_part = f"{src_var}[{width - 1}:{width - offset}]"
            return [f"ASSERT({dst_var} = {high_part} @ {low_part});"]
        else: # right
            # Right Rotate n: A[n-1 : 0] @ A[width-1 : n]
            high_part = f"{src_var}[{offset - 1}:0]"
            low_part = f"{src_var}[{width - 1}:{offset}]"
            return [f"ASSERT({dst_var} = {high_part} @ {low_part});"]

    def gen_constraints(self, round_num):
        """
        为指定轮数生成约束
        :return: (constraint_list, variable_declaration_list)
        """
        constraints = []
        declarations = []
        
        # 存储当前轮 每个节点ID 对应的 CVC变量名
        # Key: NodeID, Value: CVC_Var_Name
        node_var_map = {}
        
        # 1. 首先处理 输入/输出 变量的映射
        sorted_nodes = [self.nodes[nid] for nid in self.execution_order]

        # 计数器
        input_counter = 1
        output_counter = 1

        # --- 第一遍遍历：声明变量 (并过滤 Key) ---
        for node in sorted_nodes:
            nid = node['id']
            name = node.get('name', '')
            ntype = node['type']
            
            # 【修改点 1】直接跳过 keyVar，不为它生成任何 CVC 变量，也不存入 map
            if ntype == 'keyVar':
                continue 

            # 动态生成当前轮的变量名
            base_name = name if name else nid
            base_name = base_name.replace("-", "_")
            current_var = f"{base_name}_r{round_num}" 
            
            # --- 系统输入 ---
            if ntype == 'plainVar' and not self.incoming_edges[nid]:
                sys_input_var = getattr(self.solver, f"input{input_counter}_At_Round")(round_num)
                node_var_map[nid] = sys_input_var
                input_counter += 1
                continue
            
            # --- 系统输出 ---
            if ntype == 'plainVar' and name.startswith('Y'):
                sys_output_var = getattr(self.solver, f"output{output_counter}_At_Round")(round_num)
                node_var_map[nid] = sys_output_var
                output_counter += 1
                continue

            # --- 中间节点 (XOR, MODADD, ROTATE) ---
            if nid not in node_var_map:
                node_var_map[nid] = current_var
                # 默认取 props 里的宽度，如果没有则用 BlockSize / BranchNum
                default_width = self.solver.Blocksize // self.solver.Branch_number
                bitwidth = node['props'].get('bitwidth', default_width)
                declarations.append(f"{current_var} : BITVECTOR({bitwidth});")

        # --- 第二遍遍历：生成约束 (处理被过滤的 Key 连接) ---
        for nid in self.execution_order:
            node = self.nodes[nid]
            ntype = node['type']
            
            # 如果当前节点本身就是 Key，直接跳过
            if ntype == 'keyVar':
                continue
                
            # 如果当前节点没有被映射（可能是未使用的孤立节点），跳过
            if nid not in node_var_map:
                continue
                
            # 获取当前节点的 CVC 变量名
            dst_var = node_var_map[nid]
            
            # 获取原始的所有输入源 ID
            source_ids = self.incoming_edges[nid]
            
            # 【修改点 2】收集有效输入变量
            # 如果源 ID 在 map 中，说明是数据节点；如果不在，说明是 Key 节点被过滤了
            valid_src_vars = []
            for sid in source_ids:
                if sid in node_var_map:
                    valid_src_vars.append(node_var_map[sid])
            
            # --- 根据有效输入的数量生成约束 ---
            
            # 处理 plainVar 输出节点的连线 (Y0 = ...)
            if ntype == 'plainVar':
                if len(valid_src_vars) > 0:
                    constraints.append(f"ASSERT({dst_var} = {valid_src_vars[0]});")
                continue

            # 处理运算节点
            if ntype == 'xor':
                if len(valid_src_vars) == 0:
                    # 异常：没有数据输入（只有Key或悬空）
                    pass
                elif len(valid_src_vars) == 1:
                    # 【修改点 3】只有一个数据输入，另一个是Key -> 变成直连 (Pass-through)
                    # 差分分析中：Delta X ^ Delta K(0) = Delta X
                    constraints.append(f"ASSERT({dst_var} = {valid_src_vars[0]});")
                else:
                    # 正常的 XOR (两个都是数据变量)
                    expr = valid_src_vars[0]
                    for i in range(1, len(valid_src_vars)):
                        expr = f"BVXOR({expr}, {valid_src_vars[i]})"
                    constraints.append(f"ASSERT({dst_var} = {expr});")
            
            elif ntype == 'modadd':
                if len(valid_src_vars) == 1:
                    # 【修改点 3】ModAdd(Data, Key) -> 变成直连
                    # 在单密钥差分中通常简化为 OutputDiff = InputDiff
                    constraints.append(f"ASSERT({dst_var} = {valid_src_vars[0]});")
                elif len(valid_src_vars) == 2:
                    # 正常的模加差分 (两个数据流混合)
                    add_constraints = self.solver.modulo_addition(valid_src_vars[0], valid_src_vars[1], dst_var)
                    constraints.extend(add_constraints)
            
            elif ntype == 'rotate':
                # 移位通常只接受一个数据输入，Key 不参与移位操作
                if len(valid_src_vars) == 1:
                    rot_constraints = self._get_rotate_constraint(valid_src_vars[0], dst_var, node['props'])
                    constraints.extend(rot_constraints)

        return constraints, declarations
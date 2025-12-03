import sys
from Root import Root
from collections import Counter
from RoundFunction import RoundGraphParser 
import subprocess

class Difference(Root):
    def __init__(
        self,
        Blocksize,
        Round,
        Branch_number,
        Sbox_bit,
        Sbox_content,
        Matrix,
        NonlinearType,
    ):
        super().__init__(
            Blocksize,
            Round,
            Branch_number,
            Sbox_bit,
            Sbox_content,
            Matrix,
            NonlinearType,
        )
        self.Round = Round
        self.Blocksize = Blocksize
        self.Branch_number = Branch_number
        self.Sbox_bit = Sbox_bit
        self.Sbox_content = Sbox_content
        self.Matrix = Matrix
        self.NonlinearType = NonlinearType
        self.HalfofBlocksize = self.Blocksize // 2
        self.QuarterBlocksize = self.Blocksize // 4
        self.HalfofQuarterBlocksize = self.Blocksize // 8
        self.sum = []
        self.sum1 = []

        # 变量定义区

    def input1_At_Round(self, r):
        assert r >= 1
        return "input1_r" + str(r)

    def input2_At_Round(self, r):
        assert r >= 1
        return "input2_r" + str(r)

    def input3_At_Round(self, r):
        assert r >= 1
        return "input3_r" + str(r)

    def input4_At_Round(self, r):
        assert r >= 1
        return "input4_r" + str(r)

    def output1_At_Round(self, r):
        assert r >= 1
        return "output1_r" + str(r)

    def output2_At_Round(self, r):
        assert r >= 1
        return "output2_r" + str(r)

    def output3_At_Round(self, r):
        assert r >= 1
        return "output3_r" + str(r)

    def output4_At_Round(self, r):
        assert r >= 1
        return "output4_r" + str(r)

    def S_in_At_Round(self, r):
        assert r >= 1
        return "S_in_r" + str(r)

    def S_out_At_Round(self, r):
        assert r >= 1
        return "S_out_r" + str(r)

    def XOR_input1_At_Round(self, r):
        assert r >= 1
        return "XOR_input1_r" + str(r)

    def XOR_input2_At_Round(self, r):
        assert r >= 1
        return "XOR_input2_r" + str(r)

    def XOR_output_At_Round(self, r):
        assert r >= 1
        return "XOR_output_r" + str(r)

    def permutationIn_At_Round(self, r):
        assert r >= 1
        return "permutation_input_r" + str(r)

    def permutationOut_At_Round(self, r):
        assert r >= 1
        return "permutation_output_r" + str(r)

    def p_layer_Input_At_Round(self, r):
        assert r >= 1
        return "p_layer_input_r" + str(r)

    def p_layer_Output_At_Round(self, r):
        assert r >= 1
        return "p_layer_output_r" + str(r)

    def modulo_input1_At_Round(self, r):
        assert r >= 1
        return "modulo_input1_r" + str(r)

    def modulo_input2_At_Round(self, r):
        assert r >= 1
        return "modulo_input2_r" + str(r)

    def modulo_output_At_Round(self, r):
        assert r >= 1
        return "modulo_output_r" + str(r)

    def weight_zhi_At_Round(self, r):
        assert r >= 1
        return "w_r" + str(r)

    def OR_input1_At_Round(self, r):
        assert r >= 1
        return "OR_input1_r" + str(r)

    def OR_input2_At_Round(self, r):
        assert r >= 1
        return "OR_input2_r" + str(r)

    def OR_output_At_Round(self, r):
        assert r >= 1
        return "OR_output_r" + str(r)

    def AND_input1_At_Round(self, r):
        assert r >= 1
        return "AND_input1_r" + str(r)

    def AND_input2_At_Round(self, r):
        assert r >= 1
        return "AND_input2_r" + str(r)

    def AND_output_At_Round(self, r):
        assert r >= 1
        return "AND_output_r" + str(r)

    def Zonggeshu_FullRound(self):
        return "zonggeshu"

    def BVXOR(self, input1, input2, output):
        constraint = []
        constraint += [
            f"ASSERT({'{0} = BVXOR({1}, {2})'.format(output, input1, input2)});"
        ]

        return constraint

    def Permutation(self, inP, outP):  # 比特级置换
        inP_array = [
            "{0}_{1}".format(inP, i)
            for i in range(self.Blocksize // self.Branch_number - 1, -1, -1)
        ]  # 这些在DESL_Feistel_Linear类里的getVars函数里面都设置为了1bit的变量
        outP_array = super().DIF_Matrix_mul(inP_array)
        inP_cascade = "@".join(inP_array)
        outP_cascade = "@".join(outP_array)

        constraint = [f"ASSERT({'{0}'.format(inP) + '= {0}'.format(inP_cascade)});"]
        constraint += [f"ASSERT({'{0}'.format(outP) + '= {0}'.format(outP_cascade)});"]

        return constraint

    def equal(self, inEqual, outEqual):
        constraint = [f"ASSERT({'{0}'.format(outEqual) + ' = {0}'.format(inEqual)});"]

        return constraint

    def shift(self, A, num):
        if num != 0:
            return "({0} << {1})[{2}:0]".format(
                A, num, int(self.Blocksize / self.Branch_number - 1)
            )
        else:
            return "{0}".format(A)

    def modulo_addition(self, In1, In2, Out1):  # In1和In2是两个输入差分，Out1是输出差分
        constraint = [
            "ASSERT((("
            + self.Xor("~" + self.shift(In1, 1), self.shift(In2, 1))
            + " & "
            + self.Xor("~" + self.shift(In1, 1), self.shift(Out1, 1))
            + ") & ("
            + self.Xor(In1, self.Xor(In2, self.Xor(Out1, self.shift(In2, 1))))
            + ")) = 0bin"
            + "0" * int(self.Blocksize // self.Branch_number)
            + ");"
        ]
        # return 'ASSERT(((' + self.Xor('~' + self.shift(In1, 1), self.shift(In2, 1)) + ' & ' + self.Xor('~' + self.shift(
        #     In1, 1), self.shift(Out1, 1)) + ') & (' + self.Xor(In1, self.Xor(In2, self.Xor(Out1, self.shift(In2, 1)))) + ')) = 0bin' + '0' * int(self.Blocksize//self.Branch_number) + ');'
        return constraint

    def Weight(self, L_in, R_in, L_out, zhi):
        constraint = []
        constraint += [
            "ASSERT("
            + zhi
            + "= ~("
            + self.Xor("~" + L_in, R_in)
            + "&"
            + self.Xor("~" + L_in, L_out)
            + "));"
        ]
        return constraint

    def p_layer_1(self, inP, outP):  # 一分支，不用置换
        outP = inP
        constraint = [f"ASSERT({'{0}'.format(outP) + ' = {0}'.format(inP)});"]
        return constraint

    def p_layer_2(self, inP1, inP2, outP1, outP2):  # 二分支置换
        p_array = [inP1, inP2]
        out = super().DIF_Matrix_mul(p_array)
        constraint = [
            f"ASSERT({'{0}'.format(outP1) + '= {0}'.format(out[0])});",
            f"ASSERT({'{0}'.format(outP2) + '= {0}'.format(out[1])});",
        ]

        return constraint

    def p_layer_4(self, inP1, inP2, inP3, inP4, outP1, outP2, outP3, outP4):  # 四分支置换
        p_array = [inP1, inP2, inP3, inP4]
        out = super().DIF_Matrix_mul(p_array)
        constraint = [
            f"ASSERT({'{0}'.format(outP1) + '= {0}'.format(out[0])});",
            f"ASSERT({'{0}'.format(outP2) + '= {0}'.format(out[1])});",
            f"ASSERT({'{0}'.format(outP2) + '= {0}'.format(out[2])});",
            f"ASSERT({'{0}'.format(outP2) + '= {0}'.format(out[3])});",
        ]

        return constraint

    def S_box_Layer(self, inS, outS, inS1, outS1, S_Constraint):
        constraint = []
        if self.Sbox_bit != 8:
            # 先控制非零输入差分激活S盒
            for i in range(self.Sbox_bit):
                constraint += [  # 问题：Sbox_bit不能超过8吗？懂了
                    f"ASSERT(BVGE(S["
                    f"{'0bin{0}@{1}@'.format('0' * (8 - self.Sbox_bit), inS) + '0bin{0}@{1}'.format('0' * (8 - self.Sbox_bit), outS) + '], {0}[{1}:{1}]'.format(inS1, S_Constraint - i)}));"
                ]
            constraint += [f"ASSERT(BVGE(BVPLUS(4, "]
            for i in range(self.Sbox_bit):
                if i < self.Sbox_bit - 1:
                    constraint += [
                        f"{'0bin000@{0}'.format(inS1) + '[{0}:{0}],'.format(S_Constraint - i)}"
                    ]
                else:
                    constraint += [
                        f"{'0bin000@{0}'.format(inS1) + '[{0}:{0}]'.format(S_Constraint - i)}"
                    ]

            constraint += [
                f"), 0bin000@(S["
                f""
                f"{'0bin{0}@{1}@'.format('0' * (8 - self.Sbox_bit), inS) + '0bin{0}@{1}'.format('0' * (8 - self.Sbox_bit), outS)}])));"
            ]

            # 再控制非零输出一定激活S盒
            for i in range(self.Sbox_bit):
                constraint += [  # 问题：Sbox_bit不能超过8吗？懂了
                    f"ASSERT(BVGE(S["
                    f""
                    f"{'0bin{0}@{1}@'.format('0' * (8 - self.Sbox_bit), inS) + '0bin{0}@{1}'.format('0' * (8 - self.Sbox_bit), outS) + '], {0}[{1}:{1}]'.format(outS1, S_Constraint - i)}));"
                ]
            constraint += [f"ASSERT(BVGE(BVPLUS(4, "]
            for i in range(self.Sbox_bit):
                if i < self.Sbox_bit - 1:
                    constraint += [
                        f"{'0bin000@{0}'.format(outS1) + '[{0}:{0}],'.format(S_Constraint - i)}"
                    ]
                else:
                    constraint += [
                        f"{'0bin000@{0}'.format(outS1) + '[{0}:{0}]'.format(S_Constraint - i)}"
                    ]

            constraint += [
                f"), 0bin000@(S["
                f""
                f"{'0bin{0}@{1}@'.format('0' * (8 - self.Sbox_bit), inS) + '0bin{0}@{1}'.format('0' * (8 - self.Sbox_bit), outS)}])));"
            ]

        else:
            constraint = [
                f"ASSERT(NOT(S[{'{0}@'.format(inS) + '{0}'.format(outS)}] = 0bin0));"
            ]

        return constraint

    def OR_Layer(
        self, input1, input2, output1, input_1, input_2, output_1, S_Constraint
    ):
        constraint = []

        # 先控制非零输入差分激活S盒
        for i in range(self.Sbox_bit):
            constraint += [  # 问题：Sbox_bit不能超过8吗？懂了
                f"ASSERT(BVGE(S["
                f"{'0bin{0}@{1}@{2}@'.format('0' * (8 - 2 * self.Sbox_bit), input1, input2) + '0bin{0}@{1}'.format('0' * (8 - self.Sbox_bit), output1) + ', {0}[{1}:{1}]'.format(input_1, S_Constraint - i)}));"
            ]
        constraint += [f"ASSERT(BVGE(BVPLUS(4, "]

        constraint += [
            f"{'0bin000@{0}'.format(input_1) + '[{0}:{0}],'.format(S_Constraint - i)}"
        ]
        constraint += [
            f"{'0bin000@{0}'.format(input_2) + '[{0}:{0}]'.format(S_Constraint - i)}"
        ]

        constraint += [
            f"), 0bin000@(S["
            f"{'0bin{0}@{1}@{2}@'.format('0' * (8 - 2 * self.Sbox_bit), input1, input2) + '0bin{0}@{1}'.format('0' * (8 - self.Sbox_bit), output1)})));"
        ]

        # 再控制非零输出一定激活S盒
        constraint += [  # 问题：Sbox_bit不能超过8吗？懂了
            f"ASSERT(BVGE(S["
            f"{'0bin{0}@{1}@{2}@'.format('0' * (8 - 2 * self.Sbox_bit), input1, input2) + '0bin{0}@{1}'.format('0' * (8 - self.Sbox_bit), output1) + ', {0}[{1}:{1}]'.format(output_1, S_Constraint - i)}));"
        ]
        constraint += [f"ASSERT(BVGE(BVPLUS(4, "]
        constraint += [
            f"{'0bin000@{0}'.format(output_1) + '[{0}:{0}]'.format(S_Constraint - i)}"
        ]
        constraint += [
            f"), 0bin000@(S["
            f"{'0bin{0}@{1}@{2}@'.format('0' * (8 - 2 * self.Sbox_bit), input1, input2) + '0bin{0}@{1}'.format('0' * (8 - self.Sbox_bit), output1)})));"
        ]
        constraint += ["\n"]

        return constraint

    # 非零输入必然导致S盒活跃，非零输出必然导致S盒活跃

    def AND_Layer(
        self, input1, input2, output1, input_1, input_2, output_1, S_Constraint
    ):
        constraint = []

        # 先控制非零输入差分激活S盒
        for i in range(self.Sbox_bit):
            constraint += [  # 问题：Sbox_bit不能超过8吗？懂了
                f"ASSERT(BVGE(S["
                f"{'0bin{0}@{1}@{2}@'.format('0' * (8 - 2 * self.Sbox_bit), input1, input2) + '0bin{0}@{1}'.format('0' * (8 - self.Sbox_bit), output1) + ', {0}[{1}:{1}]'.format(input_1, S_Constraint - i)}));"
            ]
        constraint += [f"ASSERT(BVGE(BVPLUS(4, "]

        constraint += [
            f"{'0bin000@{0}'.format(input_1) + '[{0}:{0}],'.format(S_Constraint - i)}"
        ]
        constraint += [
            f"{'0bin000@{0}'.format(input_2) + '[{0}:{0}]'.format(S_Constraint - i)}"
        ]

        constraint += [
            f"), 0bin000@(S["
            f"{'0bin{0}@{1}@{2}@'.format('0' * (8 - 2 * self.Sbox_bit), input1, input2) + '0bin{0}@{1}'.format('0' * (8 - self.Sbox_bit), output1)})));"
        ]

        # 再控制非零输出一定激活S盒
        constraint += [  # 问题：Sbox_bit不能超过8吗？懂了
            f"ASSERT(BVGE(S["
            f"{'0bin{0}@{1}@{2}@'.format('0' * (8 - 2 * self.Sbox_bit), input1, input2) + '0bin{0}@{1}'.format('0' * (8 - self.Sbox_bit), output1) + ', {0}[{1}:{1}]'.format(output_1, S_Constraint - i)}));"
        ]
        constraint += [f"ASSERT(BVGE(BVPLUS(4, "]
        constraint += [
            f"{'0bin000@{0}'.format(output_1) + '[{0}:{0}]'.format(S_Constraint - i)}"
        ]
        constraint += [
            f"), 0bin000@(S["
            f"{'0bin{0}@{1}@{2}@'.format('0' * (8 - 2 * self.Sbox_bit), input1, input2) + '0bin{0}@{1}'.format('0' * (8 - self.Sbox_bit), output1)})));"
        ]
        constraint += ["\n"]

        return constraint

    # 这个函数需要参照DIF_Struct里面的函数修改一下
    def ZonggeshuConstraint(self, inS):  # 这里让sum1也加上去
        constraint = []
        j = self.Blocksize // self.Branch_number // self.Sbox_bit
        for num in range(j):
            if self.Sbox_bit != 8:
                self.sum1.append(
                    "|".join(
                        [
                            "{0}".format(inS) + "[{0}:{0}]".format(i)
                            for i in range(
                                num * self.Sbox_bit, (num + 1) * self.Sbox_bit
                            )
                        ]
                    )
                )
            else:
                self.sum1.append(
                    "|".join(
                        ["{0}[{1}:{1}]".format(inS, i) for i in range(self.Sbox_bit)]
                    )
                )

    def ZonggeshuConstraint_OR(self, input1, input2):  # 问题出在Sbox_bit上面
        self.sum1.append("{0}[{1}:{1}]|{2}[{1}:{1}]".format(input1, 0, input2))
        self.sum1.append("{0}[{1}:{1}]|{2}[{1}:{1}]".format(input1, 1, input2))

    def ZonggeshuConstraint_AND(self, input1, input2):  # 问题出在Sbox_bit上面
        self.sum1.append("{0}[{1}:{1}]|{2}[{1}:{1}]".format(input1, 0, input2))
        self.sum1.append("{0}[{1}:{1}]|{2}[{1}:{1}]".format(input1, 1, input2))

    def Function_Sbox(self, InF, OutF):
        constraint = []
        i = self.Blocksize // self.Branch_number // self.Sbox_bit
        for num in range(i):
            constraint += self.S_box_Layer(
                InF
                + "[{0}:{1}]".format(
                    self.HalfofBlocksize - 1 - num * self.Sbox_bit,
                    self.HalfofBlocksize - self.Sbox_bit - num * self.Sbox_bit,
                ),
                OutF
                + "[{0}:{1}]".format(
                    self.HalfofBlocksize - 1 - num * self.Sbox_bit,
                    self.HalfofBlocksize - self.Sbox_bit - num * self.Sbox_bit,
                ),
                InF,
                OutF,
                self.HalfofBlocksize - 1 - num * self.Sbox_bit,
            )

        return constraint

    def Function_OR(self, input1, input2, output):
        constraint = []
        i = self.Blocksize // self.Branch_number // self.Sbox_bit
        for num in range(i):
            constraint += self.OR_Layer(
                input1
                + "[{0}:{1}]".format(
                    self.HalfofBlocksize - 1 - num * self.Sbox_bit,
                    self.HalfofBlocksize - self.Sbox_bit - num * self.Sbox_bit,
                ),
                input2
                + "[{0}:{1}]".format(
                    self.HalfofBlocksize - 1 - num * self.Sbox_bit,
                    self.HalfofBlocksize - self.Sbox_bit - num * self.Sbox_bit,
                ),
                output
                + "[{0}:{1}]]".format(
                    self.HalfofBlocksize - 1 - num * self.Sbox_bit,
                    self.HalfofBlocksize - self.Sbox_bit - num * self.Sbox_bit,
                ),
                input1,
                input2,
                output,
                self.HalfofBlocksize - 1 - num * self.Sbox_bit,
            )

        return constraint

    def Function_AND(self, input1, input2, output):
        constraint = []
        i = self.Blocksize // self.Branch_number // self.Sbox_bit
        for num in range(i):
            constraint += self.AND_Layer(
                input1
                + "[{0}:{1}]".format(
                    self.HalfofBlocksize - 1 - num * self.Sbox_bit,
                    self.HalfofBlocksize - self.Sbox_bit - num * self.Sbox_bit,
                ),
                input2
                + "[{0}:{1}]".format(
                    self.HalfofBlocksize - 1 - num * self.Sbox_bit,
                    self.HalfofBlocksize - self.Sbox_bit - num * self.Sbox_bit,
                ),
                output
                + "[{0}:{1}]]".format(
                    self.HalfofBlocksize - 1 - num * self.Sbox_bit,
                    self.HalfofBlocksize - self.Sbox_bit - num * self.Sbox_bit,
                ),
                input1,
                input2,
                output,
                self.HalfofBlocksize - 1 - num * self.Sbox_bit,
            )

        return constraint
    
        # 新增：接收前端 JSON 并存储
    def set_topology(self, json_data):
        """接收前端传来的JSON"""
        self.topology_json = json_data
        # 初始化解析器
        self.parser = RoundGraphParser(json_data, self)

    def genEncryptSubjection(self, totalRound):
        constraint = []
        self.dynamic_vars = [] # 重置

        for r in range(1, totalRound + 1):
            # 1. 生成每一轮内部的约束
            r_constraints, r_decls = self.parser.gen_constraints(r)
            constraint.extend(r_constraints)
            self.dynamic_vars.extend(r_decls)
            
            # 2. 【新增】如果是 S盒相关的算法，且需要统计活跃 S盒数量
            # 你需要确保 Parser 里处理 S盒节点时，能把 input 变量名传出来
            # 或者在这里不做处理，全权交给 Parser 生成 Zonggeshu 相关的约束
            
            # 3. 【新增】连接当前轮和下一轮 (关键！)
            # 只有当不是最后一轮时才连接
            if r < totalRound:
                # 假设 JSON 里有 4 个分支，分别对应 input1~4 和 output1~4
                # 这里默认采用 Feistel/SPN 的直连逻辑：下一轮输入 = 当前轮输出
                # 如果是 Feistel 交换 (左=右, 右=左+F)，通常 JSON 里最后一层的连线决定了 output 的顺序
                # 所以这里简单的直连通常是正确的，只要前端把 output 端口定义好
                for b in range(1, self.Branch_number + 1):
                    # assert input{b}_r{r+1} = output{b}_r{r}
                    next_in = getattr(self, f"input{b}_At_Round")(r + 1)
                    curr_out = getattr(self, f"output{b}_At_Round")(r)
                    constraint.append(f"ASSERT({next_in} = {curr_out});")

        # 4. 【新增】设置差分路径的起点和终点约束
        # 起点：输入差分不能全为0
        width = self.Blocksize // self.Branch_number
        zero_string = "0bin" + "0" * width
        
        # 2. 收集第一轮的所有输入变量名 (input1_r1, input2_r1...)
        r1_input_vars = []
        for b in range(1, self.Branch_number + 1):
            var_name = getattr(self, f"input{b}_At_Round")(1)
            r1_input_vars.append(var_name)
        
        # 3. 生成约束：ASSERT( NOT( (in1=0) AND (in2=0) AND ... ) );
        # 意思是：不能所有分支同时为 0
        
        # 构造 "inX = 0" 的条件列表
        zero_conditions = [f"({var} = {zero_string})" for var in r1_input_vars]
        
        # 用 " AND " 连接起来
        all_zeros = " AND ".join(zero_conditions)
        
        # 加上 NOT 和 ASSERT
        constraint.append(f"ASSERT(NOT({all_zeros}));")
        
        # 例子：限制第一轮输入差分为固定值，或者至少有一个不为0
        # constraint.append(f"ASSERT({self.input1_At_Round(1)} = 0bin...);") 
        
        return constraint

    def getVars(self, r):
        constraint = []

        # 1. 只保留 系统级 的输入输出变量
        # 也就是 inputX_ri 和 outputX_ri
        for i in range(1, r + 1):
            for b in range(1, self.Branch_number + 1):
                # 生成 input1_r1, input2_r1 ... output1_r1 ...
                constraint.append(getattr(self, f"input{b}_At_Round")(i))
                constraint.append(getattr(self, f"output{b}_At_Round")(i))
                
                # 如果有下一轮，需要声明下一轮的输入（虽然它等于这一轮输出，但在 CVC 里变量还是需要声明的）
                if i < r:
                    constraint.append(getattr(self, f"input{b}_At_Round")(i + 1))
        
        # 最后一轮的输出也是需要的，上面的循环已经涵盖了

        # 去重
        constraint = list(set(constraint))

        # 格式化为 CVC 声明
        # 假设所有分支宽度一致，都是 BlockSize // BranchNum
        width = self.Blocksize // self.Branch_number
        constraint = [f"{c} : BITVECTOR({width});" for c in constraint]

        # 2. 必须保留总个数 (如果你的 Parser 生成了涉及 zonggeshu 的约束)
        constraint.append("zonggeshu : BITVECTOR(8);")

        # 3. 添加 Parser 动态生成的中间变量
        if hasattr(self, 'dynamic_vars'):
            unique_dynamic = list(set(self.dynamic_vars))
            constraint.extend(unique_dynamic)

        return constraint

    def RoundFunctionConstraint(self, r):
        input1_bits = self.input1_At_Round(r)
        input2_bits = self.input2_At_Round(r)
        output1_bits = self.output1_At_Round(r)
        output2_bits = self.output2_At_Round(r)
        Sin_bits = self.S_in_At_Round(r)
        Sout_bits = self.S_out_At_Round(r)
        PermutationIn_bits = self.permutationIn_At_Round(r)
        PermutationOut_bits = self.permutationOut_At_Round(r)
        XORin1_bits = self.XOR_input1_At_Round(r)
        XORin2_bits = self.XOR_input2_At_Round(r)
        XORout_bits = self.XOR_output_At_Round(r)
        constraint = []
        constraint += self.equal(input1_bits, XORin1_bits)
        constraint += self.equal(PermutationOut_bits, XORin2_bits)
        constraint += self.equal(input2_bits, Sin_bits)
        constraint += self.equal(Sout_bits, PermutationIn_bits)
        constraint += self.equal(XORout_bits, output1_bits)
        constraint += self.equal(input2_bits, output2_bits)
        constraint += self.equal(output1_bits, self.input2_At_Round(r + 1))
        constraint += self.equal(output2_bits, self.input1_At_Round(r + 1))
        constraint += self.Function_Sbox(Sin_bits, Sout_bits)
        constraint += self.Permutation(PermutationIn_bits, PermutationOut_bits)
        constraint += self.BVXOR(XORin1_bits, XORin2_bits, XORout_bits)
        constraint += ["\n"]
    
        return constraint

    def analyze_and_solve(self, S_num):
        # 1. 生成约束
        DIFresult1 = self.genEncryptSubjection(self.Round)
        DIFresult2 = self.getVars(self.Round)
        
        # 2. 定义文件路径
        DIFlp_file = "/mnt/c/Users/admin/Desktop/密码技术/自动化分析平台源码/backend/code19/DIF.cvc"

        # 3. 写入文件 (简化自您提供的 DIFanalyze 逻辑)
        with open(DIFlp_file, "w") as OFile:
            # 写入变量、约束、求解目标等...
            for i in DIFresult2: OFile.write(i + "\n")
            for i in DIFresult1: OFile.write(i + "\n")
            OFile.write("QUERY(FALSE); \n") 
            OFile.write("COUNTEREXAMPLE; \n")
            # ... 写入所有其他断言 ...

        # 4. 调用求解器
        STP_COMMAND = ["stp", DIFlp_file]
        
        print(f"✅ CVC 文件已生成。正在调用 STP 求解...")
        
        try:
            result = subprocess.run(STP_COMMAND, capture_output=True, text=True, check=True)
            output = result.stdout

            if "Invalid." in output:
                print("✅ 求解成功: 找到差分路径。")
            elif "Valid." in output:
                print("❌ 求解失败: 未找到差分路径。")
            return output
        except Exception as e:
            print(f"🛑 求解器运行出错: {e}")
            return None

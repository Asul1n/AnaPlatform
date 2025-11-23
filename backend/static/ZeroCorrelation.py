import sys
from .Root import Root
from collections import Counter
import numpy as np


class ZeroCorrelation(Root):
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
        self.Matrix = np.linalg.inv(Matrix)
        self.NonlinearType = NonlinearType
        self.HalfofBlocksize = self.Blocksize // 2
        self.QuarterBlocksize = self.Blocksize // 4
        self.HalfofQuarterBlocksize = self.Blocksize // 8
        self.sum = []
        self.sum1 = []
        self.Contradict_Round = 2

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

    def p_layer_Input1_At_Round(self, r):
        assert r >= 1
        return "p_layer_input1_r" + str(r)

    def p_layer_Input2_At_Round(self, r):
        assert r >= 1
        return "p_layer_input2_r" + str(r)

    def p_layer_Input3_At_Round(self, r):
        assert r >= 1
        return "p_layer_input3_r" + str(r)

    def p_layer_Input4_At_Round(self, r):
        assert r >= 1
        return "p_layer_input4_r" + str(r)

    def p_layer_Output1_At_Round(self, r):
        assert r >= 1
        return "p_layer_output1_r" + str(r)

    def p_layer_Output2_At_Round(self, r):
        assert r >= 1
        return "p_layer_output2_r" + str(r)

    def p_layer_Output3_At_Round(self, r):
        assert r >= 1
        return "p_layer_output3_r" + str(r)

    def p_layer_Output4_At_Round(self, r):
        assert r >= 1
        return "p_layer_output4_r" + str(r)

    def modulo_input1_At_Round(self, r):
        assert r >= 1
        return "modulo_input1_r" + str(r)

    def modulo_input2_At_Round(self, r):
        assert r >= 1
        return "modulo_input2_r" + str(r)

    def modulo_output_At_Round(self, r):
        assert r >= 1
        return "modulo_output_r" + str(r)

    def S_zhi_At_Round(self, r):
        assert r >= 1
        return "s_r" + str(r)

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

    def Split1_input1_At_Round(self, r):
        assert r >= 1
        return "split1_input1_r" + str(r)

    def Split1_input2_At_Round(self, r):
        assert r >= 1
        return "split1_input2_r" + str(r)

    def Split1_output_At_Round(self, r):
        assert r >= 1
        return "split1_output_r" + str(r)

    def Split2_input1_At_Round(self, r):
        assert r >= 1
        return "split2_input1_r" + str(r)

    def Split2_input2_At_Round(self, r):
        assert r >= 1
        return "split2_input2_r" + str(r)

    def Split2_output_At_Round(self, r):
        assert r >= 1
        return "split2_output_r" + str(r)

    def Zonggeshu_FullRound(self):
        return "zonggeshu"

    def BVXOR(self, input1, input2, output):
        constraint = []
        constraint += [f"ASSERT({'{0} = {1}'.format(input1, input2)});"]
        constraint += [f"ASSERT({'{0} = {1}'.format(input1, output)});"]

        return constraint

    def Split(self, input1, input2, output):
        constraint = []
        constraint += [
            f"ASSERT({'{0} = BVXOR({1}, {2})'.format(output, input1, input2)});"
        ]

        return constraint

    def Permutation(self, inP, outP):
        inP_array = [
            "{0}_{1}".format(inP, i)
            for i in range(self.Blocksize // self.Branch_number - 1, -1, -1)
        ]  # 这些在DESL_Feistel_Linear类里的getVars
        # 函数里面都设置为了1bit的变量
        outP_array = super().DIF_Matrix_mul(inP_array)
        inP_cascade = "@".join(inP_array)
        outP_cascade = "@".join(outP_array)

        constraint = [f"ASSERT({'{0}'.format(inP) + '= {0}'.format(inP_cascade)});"]
        constraint += [f"ASSERT({'{0}'.format(outP) + '= {0}'.format(outP_cascade)});"]

        return constraint

    def equal(self, inEqual, outEqual):
        constraint = [f"ASSERT({'{0}'.format(outEqual) + ' = {0}'.format(inEqual)});"]

        return constraint

    def modulo_addition(self, In1, In2, Out, s):
        constraint = []
        for i in range(self.Blocksize // self.Branch_number):
            constraint = constraint + [
                "ASSERT(BVGE(BVPLUS({0}, 0bin00@({1}[{5}:{5}]),0bin00@({4}[{6}:{6}]),0bin00@({1}[{6}:{6}])), BVPLUS({0},0bin00@({2}[{6}:{6}]),0bin00@({3}[{6}:{6}]))));".format(
                    3, s, Out, In1, In2, i + 1, i
                )
            ]
            constraint = constraint + [
                "ASSERT(BVGE(BVPLUS({0}, 0bin00@({1}[{5}:{5}]),0bin00@({2}[{6}:{6}]),0bin00@({1}[{6}:{6}])), BVPLUS({0},0bin00@({3}[{6}:{6}]),0bin00@({4}[{6}:{6}]))));".format(
                    3, s, Out, In1, In2, i + 1, i
                )
            ]
            constraint = constraint + [
                "ASSERT(BVGE(BVPLUS({0}, 0bin00@({1}[{5}:{5}]),0bin00@({2}[{6}:{6}]),0bin00@({4}[{6}:{6}])), BVPLUS({0},0bin00@({3}[{6}:{6}]),0bin00@({1}[{6}:{6}]))));".format(
                    3, s, Out, In1, In2, i + 1, i
                )
            ]
            constraint = constraint + [
                "ASSERT(BVGE(BVPLUS({0}, 0bin00@({2}[{6}:{6}]),0bin00@({3}[{6}:{6}]),0bin00@({4}[{6}:{6}]),0bin00@({1}[{6}:{6}])), 0bin00@({1}[{5}:{5}])));".format(
                    3, s, Out, In1, In2, i + 1, i
                )
            ]
            constraint = constraint + [
                "ASSERT(BVGE(BVPLUS({0}, 0bin00@({1}[{5}:{5}]),0bin00@({2}[{6}:{6}]),0bin00@({3}[{6}:{6}])), BVPLUS({0},0bin00@({4}[{6}:{6}]),0bin00@({1}[{6}:{6}]))));".format(
                    3, s, Out, In1, In2, i + 1, i
                )
            ]
            constraint = constraint + [
                "ASSERT(BVGE(BVPLUS({0}, 0bin00@({1}[{5}:{5}]),0bin00@({3}[{6}:{6}]),0bin00@({1}[{6}:{6}])), BVPLUS({0},0bin00@({2}[{6}:{6}]),0bin00@({4}[{6}:{6}]))));".format(
                    3, s, Out, In1, In2, i + 1, i
                )
            ]
            constraint = constraint + [
                "ASSERT(BVGE(BVPLUS({0}, 0bin00@({1}[{5}:{5}]),0bin00@({3}[{6}:{6}]),0bin00@({4}[{6}:{6}])), BVPLUS({0},0bin00@({2}[{6}:{6}]),0bin00@({1}[{6}:{6}]))));".format(
                    3, s, Out, In1, In2, i + 1, i
                )
            ]
            constraint = constraint + [
                "ASSERT(BVLE(BVPLUS({0}, 0bin00@({1}[{5}:{5}]),0bin00@({2}[{6}:{6}]),0bin00@({3}[{6}:{6}]),0bin00@({4}[{6}:{6}]),0bin00@({1}[{6}:{6}])), 0bin100));".format(
                    3, s, Out, In1, In2, i + 1, i
                )
            ]

        constraint = constraint + [
            "ASSERT({0}[{1}:{1}] = 0bin0);".format(
                s, self.Blocksize // self.Branch_number
            )
        ]  # 最高位等于0
        return constraint

    def shift(self, A, num):
        if num != 0:
            return "({0} << {1})[{2}:0]".format(
                A, num, int(self.Blocksize / self.Branch_number - 1)
            )
        else:
            return "{0}".format(A)

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

    def S_box_Layer(self, inS, outS):
        if self.Sbox_bit != 8:
            constraint = [  # 问题：Sbox_bit不能超过8吗？懂了
                f"ASSERT(NOT(S["
                f"{'0bin{0}@{1}@'.format('0' * (8 - self.Sbox_bit), inS) + '0bin{0}@{1}'.format('0' * (8 - self.Sbox_bit), outS)}] = 0bin0));"
            ]
            self.sum.append(
                "|".join(["{0}[{1}:{1}]".format(inS, i) for i in range(self.Sbox_bit)])
            )  # sum是干什么用的？
        else:
            eqn = [
                f"ASSERT(NOT(S[{'{0}@'.format(inS) + '{0}'.format(outS)}] = 0bin0));"
            ]
            self.sum.append(
                "|".join(["{0}[{1}:{1}]".format(inS, i) for i in range(self.Sbox_bit)])
            )
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

    def Function_Sbox(self, InF, OutF):
        constraint = []
        i = self.Blocksize // self.Branch_number // self.Sbox_bit
        for num in range(i):
            constraint += self.S_box_Layer(
                InF
                + "[{0}:{1}]".format(
                    self.Blocksize // self.Branch_number - 1 - num * self.Sbox_bit,
                    self.Blocksize // self.Branch_number
                    - self.Sbox_bit
                    - num * self.Sbox_bit,
                ),
                OutF
                + "[{0}:{1}]".format(
                    self.Blocksize // self.Branch_number - 1 - num * self.Sbox_bit,
                    self.Blocksize // self.Branch_number
                    - self.Sbox_bit
                    - num * self.Sbox_bit,
                ),
            )
        return constraint

    def Function_OR(self, input1, input2, output, r):
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

    def genEncryptSubjection(self, totalRound):
        constraint = []
        for i in range(1, totalRound + 1):
            constraint += self.RoundFunctionConstraint(i)
        return constraint

    def getVars(self, r):
        constraint = []

        for i in range(1, r + 1):
            constraint.append(self.S_in_At_Round(i))
            constraint.append(self.S_out_At_Round(i))
            constraint.append(self.input1_At_Round(i))
            constraint.append(self.input2_At_Round(i))
            constraint.append(self.input3_At_Round(i))
            constraint.append(self.input4_At_Round(i))

            constraint.append(self.output1_At_Round(i))
            constraint.append(self.output2_At_Round(i))
            constraint.append(self.output3_At_Round(i))
            constraint.append(self.output4_At_Round(i))

            constraint.append(self.OR_input1_At_Round(i))
            constraint.append(self.OR_input2_At_Round(i))
            constraint.append(self.OR_output_At_Round(i))

            constraint.append(self.AND_input1_At_Round(i))
            constraint.append(self.AND_input2_At_Round(i))
            constraint.append(self.AND_output_At_Round(i))

            # 设置这些是为了P-layer
            constraint.append(self.input1_At_Round(i + 1))
            constraint.append(self.input2_At_Round(i + 1))
            constraint.append(self.input3_At_Round(i + 1))
            constraint.append(self.input4_At_Round(i + 1))

            constraint.append(self.XOR_output_At_Round(i))
            constraint.append(self.XOR_input1_At_Round(i))
            constraint.append(self.XOR_input2_At_Round(i))

            constraint.append(self.Split1_input1_At_Round(i))
            constraint.append(self.Split1_input2_At_Round(i))
            constraint.append(self.Split1_output_At_Round(i))

            constraint.append(self.Split2_input1_At_Round(i))
            constraint.append(self.Split2_input2_At_Round(i))
            constraint.append(self.Split2_output_At_Round(i))

            constraint.append(self.permutationIn_At_Round(i))
            constraint.append(self.permutationOut_At_Round(i))
            constraint.append(self.p_layer_Input1_At_Round(i))
            constraint.append(self.p_layer_Input2_At_Round(i))
            constraint.append(self.p_layer_Input3_At_Round(i))
            constraint.append(self.p_layer_Input4_At_Round(i))
            constraint.append(self.p_layer_Output1_At_Round(i))
            constraint.append(self.p_layer_Output2_At_Round(i))
            constraint.append(self.p_layer_Output3_At_Round(i))
            constraint.append(self.p_layer_Output4_At_Round(i))

            constraint.append(self.modulo_input1_At_Round(i))
            constraint.append(self.modulo_input2_At_Round(i))
            constraint.append(self.modulo_output_At_Round(i))

        constraint = list(Counter(constraint))

        constraint = [
            ", ".join(constraint)
            + " : BITVECTOR({0});".format(self.Blocksize // self.Branch_number),
            "zonggeshu : BITVECTOR(8);",
        ]

        # 设置变量s
        constraint1 = []
        for i in range(1, r + 1):
            constraint1.append(self.S_zhi_At_Round(i))

        constraint1 = [
            ",".join(list(Counter(constraint1).keys())) + " : BITVECTOR(33);"
        ]

        for i in range(1, r + 1):
            constraint.append(
                ",".join(
                    [
                        "{0}_{1}".format(self.permutationIn_At_Round(i), j)
                        for j in range(self.Blocksize // self.Branch_number - 1, -1, -1)
                    ]
                )
                + " : BITVECTOR(1);"
            )

        constraint = constraint + constraint1

        return constraint

    def RoundFunctionConstraint(self, r):
        input1_bits = self.input1_At_Round(r)  # 模加的约束条件
        input2_bits = self.input2_At_Round(r)
        output1_bits = self.output1_At_Round(r)
        output2_bits = self.output2_At_Round(r)
        ModuloIn1_bits = self.modulo_input1_At_Round(r)
        ModuloIn2_bits = self.modulo_input2_At_Round(r)
        ModuloOut_bits = self.modulo_output_At_Round(r)
        s_bits = self.S_zhi_At_Round(r)
        XORin1_bits = self.XOR_input1_At_Round(r)
        XORin2_bits = self.XOR_input2_At_Round(r)
        XORout_bits = self.XOR_output_At_Round(r)
        Split1In1_bits = self.Split1_input1_At_Round(r)
        Split1In2_bits = self.Split1_input2_At_Round(r)
        Split1Out_bits = self.Split1_output_At_Round(r)
        Split2In1_bits = self.Split2_input1_At_Round(r)
        Split2In2_bits = self.Split2_input2_At_Round(r)
        Split2Out_bits = self.Split2_output_At_Round(r)
        constraint = []
        constraint += self.equal(
            self.cyclic_right_shift(input1_bits, 8), ModuloIn1_bits
        )
        constraint += self.equal(input2_bits, Split1In1_bits)
        constraint += self.equal(Split1In2_bits, ModuloIn2_bits)
        constraint += self.equal(
            Split1Out_bits, self.cyclic_right_shift(XORin1_bits, 3)
        )
        constraint += self.equal(ModuloOut_bits, Split2In1_bits)
        constraint += self.equal(Split2In2_bits, XORin2_bits)
        constraint += self.equal(Split2Out_bits, output1_bits)
        constraint += self.equal(self.input1_At_Round(r + 1), output1_bits)
        constraint += self.equal(self.input2_At_Round(r + 1), output2_bits)
        constraint += self.equal(XORout_bits, output2_bits)
        constraint += self.BVXOR(XORin1_bits, XORin2_bits, XORout_bits)
        constraint += self.Split(Split1In1_bits, Split1In2_bits, Split1Out_bits)
        constraint += self.Split(Split2In1_bits, Split2In2_bits, Split2Out_bits)
        constraint += self.modulo_addition(
            ModuloIn1_bits, ModuloIn2_bits, ModuloOut_bits, s_bits
        )
    
        constraint += ["\n"]
    
        return constraint

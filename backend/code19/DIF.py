import sys
from Root import Root
from collections import Counter


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
            f"ASSERT({'{0}'.format(outP3) + '= {0}'.format(out[2])});",
            f"ASSERT({'{0}'.format(outP4) + '= {0}'.format(out[3])});",
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

    def genEncryptSubjection(self, totalRound):
        constraint = []
        for i in range(1, totalRound + 1):
            constraint += self.RoundFunctionConstraint(i)
            self.ZonggeshuConstraint(self.S_in_At_Round(i))
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

            constraint.append(self.input1_At_Round(i + 1))
            constraint.append(self.input2_At_Round(i + 1))
            constraint.append(self.input3_At_Round(i + 1))
            constraint.append(self.input4_At_Round(i + 1))

            constraint.append(self.output1_At_Round(i))
            constraint.append(self.output2_At_Round(i))
            constraint.append(self.output3_At_Round(i))
            constraint.append(self.output4_At_Round(i))

            constraint.append(self.XOR_output_At_Round(i))
            constraint.append(self.XOR_input1_At_Round(i))
            constraint.append(self.XOR_input2_At_Round(i))

            constraint.append(self.permutationIn_At_Round(i))
            constraint.append(self.permutationOut_At_Round(i))

            constraint.append(self.modulo_input1_At_Round(i))
            constraint.append(self.modulo_input2_At_Round(i))
            constraint.append(self.modulo_output_At_Round(i))
            constraint.append(self.weight_zhi_At_Round(i))

        constraint = list(Counter(constraint))

        constraint = [
            ", ".join(constraint)
            + " : BITVECTOR({0});".format(self.Blocksize // self.Branch_number),
            "zonggeshu : BITVECTOR(8);",
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

    

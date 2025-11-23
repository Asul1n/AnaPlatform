from .Root import Root
from collections import Counter


class Integral(Root):
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

    def input1_1_At_Round(self, r):
        assert r >= 1
        return "input1_1_r" + str(r)

    def input1_2_At_Round(self, r):
        assert r >= 1
        return "input1_2_r" + str(r)

    def input1_3_At_Round(self, r):
        assert r >= 1
        return "input1_3_r" + str(r)

    def input1_4_At_Round(self, r):
        assert r >= 1
        return "input1_4_r" + str(r)

    def input1_5_At_Round(self, r):
        assert r >= 1
        return "input1_5_r" + str(r)

    def input1_6_At_Round(self, r):
        assert r >= 1
        return "input1_6_r" + str(r)

    def input1_7_At_Round(self, r):
        assert r >= 1
        return "input1_7_r" + str(r)

    def input1_8_At_Round(self, r):
        assert r >= 1
        return "input1_8_r" + str(r)

    def input2_At_Round(self, r):
        assert r >= 1
        return "input2_r" + str(r)

    def input2_1_At_Round(self, r):
        assert r >= 1
        return "input2_1_r" + str(r)

    def input2_2_At_Round(self, r):
        assert r >= 1
        return "input2_2_r" + str(r)

    def input2_3_At_Round(self, r):
        assert r >= 1
        return "input2_3_r" + str(r)

    def input2_4_At_Round(self, r):
        assert r >= 1
        return "input2_4_r" + str(r)

    def input2_5_At_Round(self, r):
        assert r >= 1
        return "input2_5_r" + str(r)

    def input2_6_At_Round(self, r):
        assert r >= 1
        return "input2_6_r" + str(r)

    def input2_7_At_Round(self, r):
        assert r >= 1
        return "input2_7_r" + str(r)

    def input2_8_At_Round(self, r):
        assert r >= 1
        return "input2_8_r" + str(r)

    def input3_At_Round(self, r):
        assert r >= 1
        return "input3_r" + str(r)

    def input4_At_Round(self, r):
        assert r >= 1
        return "input4_r" + str(r)

    def output1_At_Round(self, r):
        assert r >= 1
        return "output1_r" + str(r)

    def output1_1_At_Round(self, r):
        assert r >= 1
        return "output1_1_r" + str(r)

    def output1_2_At_Round(self, r):
        assert r >= 1
        return "output1_2_r" + str(r)

    def output1_3_At_Round(self, r):
        assert r >= 1
        return "output1_3_r" + str(r)

    def output1_4_At_Round(self, r):
        assert r >= 1
        return "output1_4_r" + str(r)

    def output1_5_At_Round(self, r):
        assert r >= 1
        return "output1_5_r" + str(r)

    def output1_6_At_Round(self, r):
        assert r >= 1
        return "output1_6_r" + str(r)

    def output1_7_At_Round(self, r):
        assert r >= 1
        return "output1_7_r" + str(r)

    def output1_8_At_Round(self, r):
        assert r >= 1
        return "output1_8_r" + str(r)

    def output2_At_Round(self, r):
        assert r >= 1
        return "output2_r" + str(r)

    def output2_1_At_Round(self, r):
        assert r >= 1
        return "output2_1_r" + str(r)

    def output2_2_At_Round(self, r):
        assert r >= 1
        return "output2_2_r" + str(r)

    def output2_3_At_Round(self, r):
        assert r >= 1
        return "output2_3_r" + str(r)

    def output2_4_At_Round(self, r):
        assert r >= 1
        return "output2_4_r" + str(r)

    def output2_5_At_Round(self, r):
        assert r >= 1
        return "output2_5_r" + str(r)

    def output2_6_At_Round(self, r):
        assert r >= 1
        return "output2_6_r" + str(r)

    def output2_7_At_Round(self, r):
        assert r >= 1
        return "output2_7_r" + str(r)

    def output2_8_At_Round(self, r):
        assert r >= 1
        return "output2_8_r" + str(r)

    def output3_At_Round(self, r):
        assert r >= 1
        return "output3_r" + str(r)

    def output4_At_Round(self, r):
        assert r >= 1
        return "output4_r" + str(r)

    def S_in_At_Round(self, r):
        assert r >= 1
        return "S_in_r" + str(r)

    def S1_in_At_Round(self, r):
        assert r >= 1
        return "S1_in_r" + str(r)

    def S2_in_At_Round(self, r):
        assert r >= 1
        return "S2_in_r" + str(r)

    def S3_in_At_Round(self, r):
        assert r >= 1
        return "S3_in_r" + str(r)

    def S4_in_At_Round(self, r):
        assert r >= 1
        return "S4_in_r" + str(r)

    def S5_in_At_Round(self, r):
        assert r >= 1
        return "S5_in_r" + str(r)

    def S6_in_At_Round(self, r):
        assert r >= 1
        return "S6_in_r" + str(r)

    def S7_in_At_Round(self, r):
        assert r >= 1
        return "S7_in_r" + str(r)

    def S8_in_At_Round(self, r):
        assert r >= 1
        return "S8_in_r" + str(r)

    def S_out_At_Round(self, r):
        assert r >= 1
        return "S_out_r" + str(r)

    def S1_out_At_Round(self, r):
        assert r >= 1
        return "S1_out_r" + str(r)

    def S2_out_At_Round(self, r):
        assert r >= 1
        return "S2_out_r" + str(r)

    def S3_out_At_Round(self, r):
        assert r >= 1
        return "S3_out_r" + str(r)

    def S4_out_At_Round(self, r):
        assert r >= 1
        return "S4_out_r" + str(r)

    def S5_out_At_Round(self, r):
        assert r >= 1
        return "S5_out_r" + str(r)

    def S6_out_At_Round(self, r):
        assert r >= 1
        return "S6_out_r" + str(r)

    def S7_out_At_Round(self, r):
        assert r >= 1
        return "S7_out_r" + str(r)

    def S8_out_At_Round(self, r):
        assert r >= 1
        return "S8_out_r" + str(r)

    def XOR_input1_At_Round(self, r):
        assert r >= 1
        return "XOR_input1_r" + str(r)

    def XOR_input1_1_At_Round(self, r):
        assert r >= 1
        return "XOR_input1_1_r" + str(r)

    def XOR_input1_2_At_Round(self, r):
        assert r >= 1
        return "XOR_input1_2_r" + str(r)

    def XOR_input1_3_At_Round(self, r):
        assert r >= 1
        return "XOR_input1_3_r" + str(r)

    def XOR_input1_4_At_Round(self, r):
        assert r >= 1
        return "XOR_input1_4_r" + str(r)

    def XOR_input1_5_At_Round(self, r):
        assert r >= 1
        return "XOR_input1_5_r" + str(r)

    def XOR_input1_6_At_Round(self, r):
        assert r >= 1
        return "XOR_input1_6_r" + str(r)

    def XOR_input1_7_At_Round(self, r):
        assert r >= 1
        return "XOR_input1_7_r" + str(r)

    def XOR_input1_8_At_Round(self, r):
        assert r >= 1
        return "XOR_input1_8_r" + str(r)

    def XOR_input2_At_Round(self, r):
        assert r >= 1
        return "XOR_input2_r" + str(r)

    def XOR_input2_1_At_Round(self, r):
        assert r >= 1
        return "XOR_input2_1_r" + str(r)

    def XOR_input2_2_At_Round(self, r):
        assert r >= 1
        return "XOR_input2_2_r" + str(r)

    def XOR_input2_3_At_Round(self, r):
        assert r >= 1
        return "XOR_input2_3_r" + str(r)

    def XOR_input2_4_At_Round(self, r):
        assert r >= 1
        return "XOR_input2_4_r" + str(r)

    def XOR_input2_5_At_Round(self, r):
        assert r >= 1
        return "XOR_input2_5_r" + str(r)

    def XOR_input2_6_At_Round(self, r):
        assert r >= 1
        return "XOR_input2_6_r" + str(r)

    def XOR_input2_7_At_Round(self, r):
        assert r >= 1
        return "XOR_input2_7_r" + str(r)

    def XOR_input2_8_At_Round(self, r):
        assert r >= 1
        return "XOR_input2_8_r" + str(r)

    def XOR_output_At_Round(self, r):
        assert r >= 1
        return "XOR_output_r" + str(r)

    def XOR_output_1_At_Round(self, r):
        assert r >= 1
        return "XOR_output_1_r" + str(r)

    def XOR_output_2_At_Round(self, r):
        assert r >= 1
        return "XOR_output_2_r" + str(r)

    def XOR_output_3_At_Round(self, r):
        assert r >= 1
        return "XOR_output_3_r" + str(r)

    def XOR_output_4_At_Round(self, r):
        assert r >= 1
        return "XOR_output_4_r" + str(r)

    def XOR_output_5_At_Round(self, r):
        assert r >= 1
        return "XOR_output_5_r" + str(r)

    def XOR_output_6_At_Round(self, r):
        assert r >= 1
        return "XOR_output_6_r" + str(r)

    def XOR_output_7_At_Round(self, r):
        assert r >= 1
        return "XOR_output_7_r" + str(r)

    def XOR_output_8_At_Round(self, r):
        assert r >= 1
        return "XOR_output_8_r" + str(r)

    def permutationIn_At_Round(self, r):
        assert r >= 1
        return "permutation_input_r" + str(r)

    def permutationIn_1_At_Round(self, r):
        assert r >= 1
        return "permutation_input_1_r" + str(r)

    def permutationIn_2_At_Round(self, r):
        assert r >= 1
        return "permutation_input_2_r" + str(r)

    def permutationIn_3_At_Round(self, r):
        assert r >= 1
        return "permutation_input_3_r" + str(r)

    def permutationIn_4_At_Round(self, r):
        assert r >= 1
        return "permutation_input_4_r" + str(r)

    def permutationIn_5_At_Round(self, r):
        assert r >= 1
        return "permutation_input_5_r" + str(r)

    def permutationIn_6_At_Round(self, r):
        assert r >= 1
        return "permutation_input_6_r" + str(r)

    def permutationIn_7_At_Round(self, r):
        assert r >= 1
        return "permutation_input_7_r" + str(r)

    def permutationIn_8_At_Round(self, r):
        assert r >= 1
        return "permutation_input_8_r" + str(r)

    def permutationOut_At_Round(self, r):
        assert r >= 1
        return "permutation_output_r" + str(r)

    def permutationOut_1_At_Round(self, r):
        assert r >= 1
        return "permutation_output_1_r" + str(r)

    def permutationOut_2_At_Round(self, r):
        assert r >= 1
        return "permutation_output_2_r" + str(r)

    def permutationOut_3_At_Round(self, r):
        assert r >= 1
        return "permutation_output_3_r" + str(r)

    def permutationOut_4_At_Round(self, r):
        assert r >= 1
        return "permutation_output_4_r" + str(r)

    def permutationOut_5_At_Round(self, r):
        assert r >= 1
        return "permutation_output_5_r" + str(r)

    def permutationOut_6_At_Round(self, r):
        assert r >= 1
        return "permutation_output_6_r" + str(r)

    def permutationOut_7_At_Round(self, r):
        assert r >= 1
        return "permutation_output_7_r" + str(r)

    def permutationOut_8_At_Round(self, r):
        assert r >= 1
        return "permutation_output_8_r" + str(r)

    def BVXOR(self, input1, input2, output):
        constraint = []
        constraint += [
            f"ASSERT(IF("
            f"{'{0}@{1}'.format(input1, input2) + ' = 0bin0101' + ')THEN({0}'.format(output) + ' = 0bin10)ELSE(A=B)ENDIF);'}"
        ]
        constraint += [
            f"ASSERT(IF("
            f"{'{0}@{1}'.format(input1, input2) + ' = 0bin0111' + ')THEN({0}'.format(output) + ' = 0bin01)ELSE(A=B)ENDIF);'}"
        ]
        constraint += [
            f"ASSERT(IF("
            f"{'{0}@{1}'.format(input1, input2) + ' = 0bin1010' + ')THEN({0}'.format(output) + ' = 0bin10)ELSE(A=B)ENDIF);'}"
        ]
        constraint += [
            f"ASSERT(IF("
            f"{'{0}@{1}'.format(input1, input2) + ' = 0bin1101' + ')THEN({0}'.format(output) + ' = 0bin01)ELSE(A=B)ENDIF);'}"
        ]
        constraint += [
            f"ASSERT(IF("
            f"{'{0}@{1}'.format(input1, input2) + ' = 0bin1111' + ')THEN({0}'.format(output) + ' = 0bin11)ELSE(A=B)ENDIF);'}"
        ]
        constraint += [
            f"ASSERT(IF("
            f"{'{0}'.format(input1) + ' = 0bin00)THEN({0} = 0bin00)ELSE(A=B)ENDIF);'.format(output)}"
        ]
        constraint += [
            f"ASSERT(IF("
            f"{'{0}'.format(input2) + ' = 0bin00)THEN({0} = 0bin00)ELSE(A=B)ENDIF);'.format(output)}"
        ]
        constraint += [
            f"ASSERT(IF("
            f"{'{0}@{1}'.format(input1, input2) + ' = 0bin0110' + ')THEN({0}'.format(output) + ' = 0bin00)ELSE(A=B)ENDIF);'}"
        ]
        constraint += [
            f"ASSERT(IF("
            f"{'{0}@{1}'.format(input1, input2) + ' = 0bin1001' + ')THEN({0}'.format(output) + ' = 0bin00)ELSE(A=B)ENDIF);'}"
        ]
        constraint += [
            f"ASSERT(IF("
            f"{'{0}@{1}'.format(input1, input2) + ' = 0bin1011' + ')THEN({0}'.format(output) + ' = 0bin00)ELSE(A=B)ENDIF);'}"
        ]
        constraint += [
            f"ASSERT(IF("
            f"{'{0}@{1}'.format(input1, input2) + ' = 0bin1110' + ')THEN({0}'.format(output) + ' = 0bin00)ELSE(A=B)ENDIF);'}"
        ]

        return constraint

    def equal(self, inEqual, outEqual):
        constraint = [f"ASSERT({'{0}'.format(outEqual) + ' = {0}'.format(inEqual)});"]

        return constraint

    def Permutation(self, inP, outP):  # nibble级置换
        inP_array = [
            "{0}_{1}".format(inP, i)
            for i in range(
                self.Blocksize // self.Branch_number // self.Sbox_bit - 1, -1, -1
            )
        ]  # 这些在DESL_Feistel_Linear类里的getVars函数里面都设置为了1bit的变量
        outP_array = super().DIF_Matrix_mul(inP_array)
        inP_cascade = "@".join(inP_array)
        outP_cascade = "@".join(outP_array)

        constraint = [f"ASSERT({'{0}'.format(inP) + '= {0}'.format(inP_cascade)});"]
        constraint += [f"ASSERT({'{0}'.format(outP) + '= {0}'.format(outP_cascade)});"]

        return constraint

    def S_box_Layer(self, inS, outS):
        constraint = []
        constraint += [
            f"ASSERT(IF({'{0} = 0bin00)THEN({1} = 0bin00)ELSE(A=B)ENDIF);'.format(inS, outS)}"
        ]
        constraint += [
            f"ASSERT(IF({'{0} = 0bin01)THEN({1} = 0bin01)ELSE(A=B)ENDIF);'.format(inS, outS)}"
        ]
        constraint += [
            f"ASSERT(IF({'{0} = 0bin10)THEN({1} = 0bin00)ELSE(A=B)ENDIF);'.format(inS, outS)}"
        ]
        constraint += [
            f"ASSERT(IF({'{0} = 0bin11)THEN({1} = 0bin11)ELSE(A=B)ENDIF);'.format(inS, outS)}"
        ]

        return constraint

    def Separate(
        self,
        input,
        output1,
        output2,
        output3,
        output4,
        output5,
        output6,
        output7,
        output8,
    ):
        constraint = []
        constraint += [
            f"ASSERT("
            f"{'{0} = {1}@{2}@{3}@{4}@{5}@{6}@{7}@{8});'.format(input, output1, output2, output3, output4, output5, output6, output7, output8)}"
        ]

        return constraint

    def Combine(
        self, input1, input2, input3, input4, input5, input6, input7, input8, output
    ):
        constraint = []
        constraint += [
            f"ASSERT("
            f"{'{0} = {1}@{2}@{3}@{4}@{5}@{6}@{7}@{8});'.format(output, input1, input2, input3, input4, input5, input6, input7, input8)}"
        ]

        return constraint

    def genEncryptSubjection(self, totalRound):
        constraint = []
        for i in range(1, totalRound + 1):
            constraint += self.RoundFunctionConstraint(i)
        return constraint

    def getVars(self, r):
        constraint = []
        constraint1 = []

        for i in range(1, r + 1):
            constraint1.append(self.S_in_At_Round(i))
            constraint1.append(self.S_out_At_Round(i))
            constraint1.append(self.input1_At_Round(i))
            constraint1.append(self.input2_At_Round(i))
            constraint1.append(self.XOR_input1_At_Round(i))
            constraint1.append(self.XOR_input2_At_Round(i))
            constraint1.append(self.XOR_output_At_Round(i))

            constraint1.append(self.input1_At_Round(i + 1))
            constraint1.append(self.input2_At_Round(i + 1))

            constraint.append(self.input1_1_At_Round(i))
            constraint.append(self.input1_2_At_Round(i))
            constraint.append(self.input1_3_At_Round(i))
            constraint.append(self.input1_4_At_Round(i))
            constraint.append(self.input1_5_At_Round(i))
            constraint.append(self.input1_6_At_Round(i))
            constraint.append(self.input1_7_At_Round(i))
            constraint.append(self.input1_8_At_Round(i))

            constraint.append(self.input2_1_At_Round(i))
            constraint.append(self.input2_2_At_Round(i))
            constraint.append(self.input2_3_At_Round(i))
            constraint.append(self.input2_4_At_Round(i))
            constraint.append(self.input2_5_At_Round(i))
            constraint.append(self.input2_6_At_Round(i))
            constraint.append(self.input2_7_At_Round(i))
            constraint.append(self.input2_8_At_Round(i))

            constraint.append(self.XOR_input1_1_At_Round(i))
            constraint.append(self.XOR_input1_2_At_Round(i))
            constraint.append(self.XOR_input1_3_At_Round(i))
            constraint.append(self.XOR_input1_4_At_Round(i))
            constraint.append(self.XOR_input1_5_At_Round(i))
            constraint.append(self.XOR_input1_6_At_Round(i))
            constraint.append(self.XOR_input1_7_At_Round(i))
            constraint.append(self.XOR_input1_8_At_Round(i))

            constraint.append(self.XOR_input2_1_At_Round(i))
            constraint.append(self.XOR_input2_2_At_Round(i))
            constraint.append(self.XOR_input2_3_At_Round(i))
            constraint.append(self.XOR_input2_4_At_Round(i))
            constraint.append(self.XOR_input2_5_At_Round(i))
            constraint.append(self.XOR_input2_6_At_Round(i))
            constraint.append(self.XOR_input2_7_At_Round(i))
            constraint.append(self.XOR_input2_8_At_Round(i))

            constraint.append(self.XOR_output_1_At_Round(i))
            constraint.append(self.XOR_output_2_At_Round(i))
            constraint.append(self.XOR_output_3_At_Round(i))
            constraint.append(self.XOR_output_4_At_Round(i))
            constraint.append(self.XOR_output_5_At_Round(i))
            constraint.append(self.XOR_output_6_At_Round(i))
            constraint.append(self.XOR_output_7_At_Round(i))
            constraint.append(self.XOR_output_8_At_Round(i))

            constraint.append(self.S1_in_At_Round(i))
            constraint.append(self.S2_in_At_Round(i))
            constraint.append(self.S3_in_At_Round(i))
            constraint.append(self.S4_in_At_Round(i))
            constraint.append(self.S5_in_At_Round(i))
            constraint.append(self.S6_in_At_Round(i))
            constraint.append(self.S7_in_At_Round(i))
            constraint.append(self.S8_in_At_Round(i))

            constraint.append(self.S1_out_At_Round(i))
            constraint.append(self.S2_out_At_Round(i))
            constraint.append(self.S3_out_At_Round(i))
            constraint.append(self.S4_out_At_Round(i))
            constraint.append(self.S5_out_At_Round(i))
            constraint.append(self.S6_out_At_Round(i))
            constraint.append(self.S7_out_At_Round(i))
            constraint.append(self.S8_out_At_Round(i))

            constraint1.append(self.output1_At_Round(i))
            constraint1.append(self.output2_At_Round(i))

            constraint1.append(self.permutationIn_At_Round(i))
            constraint1.append(self.permutationOut_At_Round(i))

        constraint = list(Counter(constraint))
        constraint1 = list(Counter(constraint1))

        constraint = [", ".join(constraint) + " : BITVECTOR(2);", "A,B:BITVECTOR(2);"]

        constraint1 = [", ".join(constraint1) + " : BITVECTOR(16);"]

        for i in range(1, r + 1):
            constraint.append(
                ",".join(
                    [
                        "{0}_{1}".format(self.permutationIn_At_Round(i), j)
                        for j in range(7, -1, -1)
                    ]
                )
                + " : BITVECTOR(2);"
            )

        constraint = constraint + constraint1

        return constraint

    def RoundFunctionConstraint(self, r):
        input_bits = self.input1_At_Round(r)  # 模加的约束条件
    
        output_bits = self.output1_At_Round(r)
    
        s_in = self.S_in_At_Round(r)
        s_out = self.S_out_At_Round(r)
    
        p_in = self.permutationIn_At_Round(r)
        p_out = self.permutationOut_At_Round(r)
    
        constraint = []
        constraint += self.equal(input_bits,s_in)
        constraint += self.equal(s_out, p_in)
        constraint += self.equal(output_bits, p_out)
    
    
        constraint += self.equal(self.input1_At_Round(r+1), p_out)
    
    
    
        constraint += ['\n']
    
        return constraint
    

from DIF import Difference
from Linear import Linear

class test:
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
        self.Blocksize = Blocksize
        self.Round = Round
        self.Branch_number = Branch_number
        self.Sbox_bit = Sbox_bit
        self.NonlinearType = NonlinearType
        self.Matrix = Matrix
        self.HalfofBlocksize = self.Blocksize / 2
        self.QuarterBlocksize = self.Blocksize / 4
        self.HalfofQuarterBlocksize = self.Blocksize / 8

        self.MyDIF = Difference(
            Blocksize,
            Round,
            Branch_number,
            Sbox_bit,
            Sbox_content,
            Matrix,
            NonlinearType,
        )
        self.MyLinear = Linear(
            Blocksize,
            Round,
            Branch_number,
            Sbox_bit,
            Sbox_content,
            Matrix,
            NonlinearType,
        )

    def DIFanalyze(self, S_num):
        DIFresult1 = self.MyDIF.genEncryptSubjection(self.MyDIF.Round)
        DIFresult2 = self.MyDIF.getVars(self.MyDIF.Round)
        DIFlp_file = (
            "/mnt/c/Users/admin/Desktop/密码技术/安全性分析平台源码/backend/static/cvc/DIF.cvc"
        )


        if self.NonlinearType == "modulo":
            with open(DIFlp_file, "a") as OFile:
                OFile.seek(0)
                OFile.truncate()

                for i in DIFresult2:
                    OFile.write(i + "\n")

                for i in DIFresult1:
                    OFile.write(i + "\n")

                OFile.write(
                    "ASSERT(BVGT(input1_r1@input2_r1 , "
                    + "0bin"
                    + "0" * self.Blocksize
                    + "));"
                    + "\n"
                )

                cunjieguo = []
                for i in range(1, self.MyDIF.Round + 1):
                    for j in range(0, self.Blocksize // self.Branch_number - 1):
                        cunjieguo.append("0bin0000000@w_r%s[%s:%s]" % (i, j, j))

                OFile.write(
                    "ASSERT(BVPLUS(8, 0bin00000000, "
                    + ",".join(cunjieguo)
                    + ")"
                    + " = zonggeshu);\n"
                )
                OFile.write(
                    "ASSERT(zonggeshu = 0bin" + bin(S_num)[2:].zfill(8) + ");" + "\n"
                )

                OFile.write("QUERY(FALSE); \n")
                OFile.write("COUNTEREXAMPLE; \n")

                OFile.close()

        else:
            with open(DIFlp_file, "a") as OFile:
                OFile.seek(0)
                OFile.truncate()

                OFile.write("S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n")
                for i in self.MyDIF.DDT:
                    OFile.write(i + "\n")

                for i in DIFresult2:
                    OFile.write(i + "\n")

                for i in DIFresult1:
                    OFile.write(i + "\n")

                OFile.write(
                    "ASSERT(BVPLUS(8, 0bin00000000, "
                    + ",".join(
                        [
                            "0bin0000000@(%s)" % (self.MyDIF.sum1[i])
                            for i in range(
                                self.MyDIF.Round
                                * (
                                    self.Blocksize
                                    // self.Branch_number
                                    // self.Sbox_bit
                                )
                            )
                        ]
                    )
                    + ")"
                    + " = "
                    + "zonggeshu"
                    + ");"
                    + "\n"
                )

                OFile.write(
                    "ASSERT(BVLE(zonggeshu, 0bin" + bin(S_num)[2:].zfill(8) + "));\n"
                )
                OFile.write(
                    "ASSERT(BVGT(input1_r1@input2_r1, "
                    + "0bin"
                    + "0" * (self.Blocksize)
                    + "));\n"
                )

                OFile.write("QUERY(FALSE); \n")
                OFile.write("COUNTEREXAMPLE; \n")

                OFile.close()

    def Linearanalyze(self, S_num):
        Linearresult1 = self.MyLinear.genEncryptSubjection(self.MyLinear.Round)
        Linearresult2 = self.MyLinear.getVars(self.MyLinear.Round)
        Linearlp_file = (
            "/mnt/c/Users/admin/Desktop/密码技术/安全性分析平台源码/backend/static/cvc/Linear.cvc"
        )


        if self.NonlinearType == "modulo":
            with open(Linearlp_file, "a") as OFile:
                OFile.seek(0)
                OFile.truncate()

                for i in Linearresult2:
                    OFile.write(i + "\n")

                for i in Linearresult1:
                    OFile.write(i + "\n")

                OFile.write(
                    "ASSERT(BVGT(input1_r1@input2_r1 , "
                    + "0bin"
                    + "0" * self.Blocksize
                    + "));\n"
                )

                command = "ASSERT(BVPLUS(16,"
                for i in range(1, self.MyLinear.Round + 1):
                    for j in range(1, self.Blocksize // self.Branch_number):
                        if i == self.MyLinear.Round and j == (
                            self.Blocksize // self.Branch_number - 1
                        ):
                            command += (
                                "0bin000000000000000@s_r"
                                + str(i)
                                + "["
                                + str(j)
                                + ":"
                                + str(j)
                                + "]"
                                + ") = 0bin"
                                + bin(S_num)[2:].zfill(16)
                                + ");"
                            )
                        else:
                            command += (
                                "0bin000000000000000@s_r"
                                + str(i)
                                + "["
                                + str(j)
                                + ":"
                                + str(j)
                                + "]"
                                + ","
                            )

                OFile.write(command + "\n")

                OFile.write("QUERY FALSE; \n")
                OFile.write("COUNTEREXAMPLE; \n")

                OFile.close()

        else:
            with open(Linearlp_file, "a") as OFile:
                OFile.seek(0)
                OFile.truncate()

                OFile.write("S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n")

                for i in self.MyLinear.LAT:
                    OFile.write(i + "\n")

                for i in Linearresult2:
                    OFile.write(i + "\n")

                for i in Linearresult1:
                    OFile.write(i + "\n")

                OFile.write(
                    "ASSERT(BVPLUS(8, 0bin00000000, "
                    + ",".join(
                        [
                            "0bin0000000@(%s)" % (self.MyLinear.sum1[i])
                            for i in range(
                                self.MyLinear.Round
                                * (
                                    self.Blocksize
                                    // self.Branch_number
                                    // self.Sbox_bit
                                )
                            )
                        ]
                    )
                    + ")"
                    + " = "
                    + "zonggeshu"
                    + ");"
                    + "\n"
                )

                OFile.write(
                    "ASSERT(BVLE(zonggeshu, 0bin" + bin(S_num)[2:].zfill(8) + "));\n"
                )
                OFile.write(
                    "ASSERT(BVGT(input2_r1, "
                    + "0bin"
                    + "0" * (self.Blocksize // 2)
                    + "));\n"
                )

                OFile.write("QUERY(FALSE); \n")
                OFile.write("COUNTEREXAMPLE; \n")

                OFile.close()



    def DIFgathered(self, power, round, con, input_diff, output_diff):    

        # 十六进制差分转成二进制字符串，宽度与 self.Blocksize 对齐
        def _hex_to_bin(h: str) -> str:
            return bin(int(h, 16))[2:].zfill(self.Blocksize)

        input_diff_bin  = _hex_to_bin(input_diff)
        output_diff_bin = _hex_to_bin(output_diff)

        # 生成变量与加密约束
        DIFresult1 = self.MyDIF.genEncryptSubjection(round)   # 加密约束
        DIFresult2 = self.MyDIF.getVars(round)                # 变量声明

        DIFlp_file = (
            "/mnt/c/Users/admin/Desktop/密码技术/安全性分析平台源码/backend/static/cvc/DIF.cvc"
        )

        if self.NonlinearType == "modulo":
            with open(DIFlp_file, "w") as f:  
                for line in DIFresult2:
                    f.write(line + "\n")
                for line in DIFresult1:
                    f.write(line + "\n")

                # 固定输入差分
                f.write(f"ASSERT(input1_At_Round1@input2_At_Round1@input3_At_Round3@input4_At_Round4 = 0bin{input_diff_bin});\n")

                # 固定输出差分（最后一轮）
                f.write(f"ASSERT(output1_At_Round{round+1}@output2_At_Round{round+1}@output3_At_Round{round+1}@output4_At_Round{round+1} = 0bin{output_diff_bin});\n")

                if con == 1:
                    active_terms = []
                    for i in range(1, round + 1):
                        for j in range(0, self.Blocksize // self.Branch_number - 1):
                            active_terms.append(f"0bin0000000@w_r{i}[{j}:{j}]")

                    f.write("ASSERT(BVPLUS(8, 0bin00000000, " + ",".join(active_terms) + ") = zonggeshu);\n")
                    f.write(f"ASSERT(zonggeshu = 0bin{bin(power)[2:].zfill(8)});\n")


                f.write("QUERY(FALSE);\n")
                f.write("COUNTEREXAMPLE;\n")
        else:
            with open(DIFlp_file, "w") as f:
                f.write("S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n")
                for line in self.MyDIF.DDT:
                    f.write(line + "\n")

                for line in DIFresult2:
                    f.write(line + "\n")
                for line in DIFresult1:
                    f.write(line + "\n")

                # 固定输入/输出差分
                f.write(f"ASSERT(S_in_At_Round1 = 0bin{input_diff_bin});\n")
                f.write(f"ASSERT(S_out_At_Round{round+1} = 0bin{output_diff_bin});\n")

                if con == 1:
                    terms = [
                        f"0bin0000000@({self.MyDIF.sum1[i]})"
                        for i in range(round * (self.Blocksize // self.Branch_number // self.Sbox_bit))
                    ]
                    f.write("ASSERT(BVPLUS(8, 0bin00000000, " + ",".join(terms) + ") = zonggeshu);\n")
                    f.write("ASSERT(BVLE(zonggeshu, 0bin{bin(power)[2:].zfill(8)}));\n")

                f.write("QUERY(FALSE);\n")
                f.write("COUNTEREXAMPLE;\n")


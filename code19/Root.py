import numpy as np


class Root(object):
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
        self.NonlinearType = NonlinearType
        self.HalfofBlocksize = self.Blocksize / 2
        self.QuarterBlocksize = self.Blocksize / 4
        self.HalfofQuarterBlocksize = self.Blocksize / 8
        self.Branch_number = Branch_number
        self.Sbox_bit = Sbox_bit
        self.Sbox_content = Sbox_content  
        self.Matrix = Matrix
        if self.NonlinearType == "OR":
            self.DDT = []
            self.ORDDT()
            self.LAT = []
            self.ORLAT()
        if self.NonlinearType == "AND":
            self.DDT = []
            self.ANDDDT()
            self.LAT = []
            self.ANDLAT()
        if self.NonlinearType == "Sbox":
            self.DDT = []
            self.G_DDT()
            self.LAT = []
            self.G_LAT()
        if self.NonlinearType == "modulo":
            self.DDT = []
            self.G_DDT()
            self.LAT = []
            self.G_LAT()

    def cyclic_left_shift(self, Var, Num):
        if Num == 0 or Num == self.Blocksize // self.Branch_number:
            return "{0}".format(Var)
        else:
            return "({0}[{1}:0] @ {0}[{2}:{3}])".format(
                Var,  
                self.Blocksize // self.Branch_number - Num - 1,
                self.Blocksize // self.Branch_number - 1,
                self.Blocksize // self.Branch_number - Num,
            )

    def cyclic_right_shift(self, Var, Num):
        if Num == 0 or Num == self.Blocksize // self.Branch_number:
            return "{0}".format(Var)
        else:
            return "({0}[{1}:0] @ {0}[{2}:{3}])".format(
                Var, Num - 1, self.Blocksize // self.Branch_number - 1, Num
            )

    def Xor(self, Var1, Var2):
        return "BVXOR({0},{1})".format(Var1, Var2)

    def G_DDT(self):
        if self.NonlinearType != "sbox": 
            # 如果是非 S-box 算法（例如 'modulo'），则不需要计算 DDT
            print(f"INFO: NonlinearType is '{self.NonlinearType}', skipping DDT generation.")
            # 为了防止后续代码依赖 DDT 属性而崩溃，可以设置一个默认值。
            self.DDT = [] 
            return

        DDT = [
            [0 for i in range(pow(2, self.Sbox_bit))]
            for j in range(pow(2, self.Sbox_bit))
        ]

        for dif_x in range(pow(2, self.Sbox_bit)):  # 遍历差分
            for x in range(pow(2, self.Sbox_bit)):  # 遍历第一个明文
                the_other_x = dif_x ^ x  # 找到另一个明文
                y = self.Sbox_content[x]  # 第一个明文的S盒输出
                the_other_y = self.Sbox_content[the_other_x]  # 第二个明文的S盒输出
                dif_y = y ^ the_other_y
                DDT[dif_x][dif_y] += 1


        for i in range(pow(2, self.Sbox_bit)):
            for j in range(pow(2, self.Sbox_bit)):
                if i == 0 and j == 0:
                    self.DDT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin0);"
                    )
                elif DDT[i][j] == 0:
                    self.DDT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin0);"
                    )
                else:
                    self.DDT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin1);"
                    )

    def G_LAT(self):
        if self.NonlinearType != "sbox": 
            # 如果是非 S-box 算法（例如 'modulo'），则不需要计算 LAT
            print(f"INFO: NonlinearType is '{self.NonlinearType}', skipping LAT generation.")
            # 为了防止后续代码依赖 LAT 属性而崩溃，可以设置一个默认值。
            self.LAT = [] 
            return
        
        LAT = [
            [0 for i in range(pow(2, self.Sbox_bit))]
            for j in range(pow(2, self.Sbox_bit))
        ]

        for S_in in range(pow(2, self.Sbox_bit)):
            S_out = self.Sbox_content[S_in]
            for Alpha in range(pow(2, self.Sbox_bit)):
                for Beta in range(pow(2, self.Sbox_bit)):
                    a = self.Bitxor(S_in, Alpha)
                    b = self.Bitxor(S_out, Beta)
                    if a == b:
                        LAT[Alpha][Beta] += 1

        for i in range(pow(2, self.Sbox_bit)):
            for j in range(pow(2, self.Sbox_bit)):
                if i == 0 and j == 0:
                    self.LAT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin0);"
                    )
                elif LAT[i][j] == (pow(2, self.Sbox_bit) / 2):
                    self.LAT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin0);"
                    )
                else:
                    self.LAT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin1);"
                    )

    def ANDDDT(self):
        DDT = [[0 for i in range(pow(2, 1))] for j in range(pow(2, 2))]

        for dif_x in range(pow(2, 2)):
            for x in range(pow(2, 2)):
                the_other_x = dif_x ^ x
                y = self.Sbox_content[x]
                the_other_y = self.Sbox_content[the_other_x]
                dif_y = y ^ the_other_y
                DDT[dif_x][dif_y] += 1

        for i in range(pow(2, 2)):
            for j in range(pow(2, 1)):
                if i == 0 & j == 0:
                    self.DDT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin0);"
                    )
                elif DDT[i][j] == 0:
                    self.DDT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin0);"
                    )

                else:
                    self.DDT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin1);"
                    )

    def ORDDT(self):
        DDT = [[0 for i in range(pow(2, 1))] for j in range(pow(2, 2))]

        for dif_x in range(pow(2, 2)):
            for x in range(pow(2, 2)):
                the_other_x = dif_x ^ x
                y = self.Sbox_content[x]
                the_other_y = self.Sbox_content[the_other_x]
                dif_y = y ^ the_other_y
                DDT[dif_x][dif_y] += 1

        for i in range(pow(2, 2)):
            for j in range(pow(2, 1)):
                if i == 0 & j == 0:
                    self.DDT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin0);"
                    )
                elif DDT[i][j] == 0:
                    self.DDT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin0);"
                    )
                    # 想法：这里可以改成02b和01b，因为是比特级的
                else:
                    self.DDT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin1);"
                    )

    def ANDLAT(self):
        LAT = [[0 for i in range(pow(2, 1))] for j in range(pow(2, 2))]

        for S_in in range(pow(2, 2)):
            S_out = self.Sbox_content[S_in]
            for Alpha in range(pow(2, 2)):
                for Beta in range(pow(2, 1)):
                    a = self.Bitxor(S_in, Alpha)
                    b = self.Bitxor(S_out, Beta)
                    if a == b:
                        LAT[Alpha][Beta] += 1

        for i in range(pow(2, 2)):
            for j in range(pow(2, 1)):
                if i == 0:
                    self.LAT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin0);"
                    )
                elif LAT[i][j] == (pow(2, 2) / 2):
                    self.LAT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin0);"
                    )
                else:
                    self.LAT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin1);"
                    )

    def ORLAT(self):
        LAT = [[0 for i in range(pow(2, 1))] for j in range(pow(2, 2))]

        for S_in in range(pow(2, 2)):
            S_out = self.Sbox_content[S_in]
            for Alpha in range(pow(2, 2)):
                for Beta in range(pow(2, 1)):
                    a = self.Bitxor(S_in, Alpha)

                    b = self.Bitxor(S_out, Beta)
                    if a == b:
                        LAT[Alpha][Beta] += 1

        for i in range(pow(2, 2)):
            for j in range(pow(2, 1)):
                if i == 0:
                    self.LAT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin0);"
                    )
                elif LAT[i][j] == (pow(2, 2) / 2):
                    self.LAT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin0);"
                    )
                else:
                    self.LAT.append(
                        f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin1);"
                    )

    def Bitxor(self, n, mask):
        bitlist = [int(x) for x in bin(n & mask)[2:]]
        # 将二进制字符串中的每个字符x转换为int型数，并将这些整数放入一个列表中，这个列表中的元素将是0和1， 表示了按位与操作的结果

        return bitlist.count(1) % 2  # 这个应该就相当于按位点乘后，再把每一个按位点乘后的值全部异或起来

    def DIF_Matrix_mul(self, Input):  # 差分过线性层
        row = len(self.Matrix)
        col = len(self.Matrix[0])
        Output = []

        for i in range(row):
            for j in range(col):
                if self.Matrix[i][j] == 0:
                    continue
                else:
                    Output.append(Input[j])

        return Output

    def Linear_Matrix_mul(self, Input):  # 这里为什么要对矩阵求逆？
        Matrix = np.linalg.inv(self.Matrix)
        row = len(Matrix)
        col = len(Matrix[0])

        Output = []

        for i in range(row):
            for j in range(col):
                if self.Matrix[i][j] == 0:
                    continue
                else:
                    Output.append(Input[j])

        return Output
    




import sys
from .root import Root
from collections import Counter

class Difference(Root):
    def __init__(
        self,
        Blocksize,
        Round,
        Branch_number,
        Sbox_bit=None,
        Sbox_content=None,
        Matrix=None,
        NonlinearType=None,
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
        self.BranchSize = self.Blocksize // self.Branch_number if self.Branch_number else 0
        self.HalfofBlocksize = self.Blocksize // 2
        self.QuarterBlocksize = self.Blocksize // 4
        self.HalfofQuarterBlocksize = self.Blocksize // 8
        
    """ 变量定义区 """
    # 通用变量定义接口
    """     def define_var(self, name: str, bitwidth: int, vtype="state", round_id=None, branch_id=None):
            key = f"{name}{branch_id}_{round_id}" if branch_id is not None else f"{name}_{round_id}"
            self.variables[key] = {
                "bitwidth": bitwidth,
                "type": vtype,
                "round": round_id,
                "branch": branch_id
            } """
        
    # 通用变量声明接口
    def declare_var(self):
        """ 
        1. 规定输入变量的基命名为X，输出变量的基命名为Y
        2. 其实这里的命名规则是根据轮数和分支数固定的，与前端 json 文件的命名无关"""
        constraint = []
        for r in range(self.Round):
            constraint.append(f"%declare each round variables in differential")
            
            # 定义每轮的输入输出变量
            x_vars = [f"X{i}_{r}" for i in range(self.Branch_number)]
            y_vars = [f"Y{i}_{r}" for i in range(self.Branch_number)]
            
            # 生成声明
            constraint.append(f"{','.join(x_vars + y_vars)} : BITVECTOR({self.BranchSize})")
                
            # 拼接 state
            state_name = f"STATE_{r}"
            state_expr = "@".join(x_vars)
            constraint.append(f"{state_name} : BITVECTOR({self.Blocksize});")
            constraint.append(f"ASSERT({state_name} = {state_expr});")

        return "\n".join(constraint)
    
    """ 基础函数定义区 """
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
    
    
    """ 组件定义区 """
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
            
    
    """ 差分分析函数 """
    def generate_diff_count(self, var_names, bit_length, round, dc_name="DC", bv_width=10, bvplus_width=6):
        """ 
        自动生成 CVC 格式的差分计数表达式
        计算 neq_X1_0 和 neq_X2_0 这两个 32 位向量里，一共有多少个位是 1。
        ------------------------------
        var_names: list[str]   差分变量名列表，例如 ["neq_X1_0", "neq_X2_0"]
        bit_length: int        每个变量的比特长度（如 32）
        dc_name: str           输出变量名（默认 "DC_0"）
        bv_width: int          DC_0 的位宽（默认 10）
        bvplus_width: int      BVPLUS 加法器的内部宽度（默认 6）
        """
        
        # 定义头部
        constraint = [f"{dc_name}_{round}: BITVECTOR({bv_width});",f"ASSERT({dc_name}_{round} = BVPLUS({bvplus_width},"]
        # 拼接每一项
        terms = []
        for var in var_names:
            for i in range(bit_length):
                terms.append(f" 0b{'0'*(bv_width-1)}@{var}[{i}:{i}]")
                
        # 用逗号拼接，并在最后加上括号
        joined_terms = ",\n".join(terms)
        constraint.append(joined_terms + "));")
        
        return "\n".join(constraint)
    
    def generate_diff_relation(self, relations, round_idx=0):
        """
        自动生成 CVC 格式的差分关系约束，例如：
        ASSERT(neq_X1_0 = ~(BVXOR(~Y0_0, Y1_0) & BVXOR(~Y0_0, X1_1)));

        ------------------------------
        relations: list[tuple]
            每个元组格式为：
            (neq_var, Y_left, Y_right, X_next)
            对应上式中的：
            neq_var = ~(BVXOR(~Y_left, Y_right) & BVXOR(~Y_left, X_next))
            
            例如：
            [
                ("neq_X1_0", "Y0_0", "Y1_0", "X1_1"),
                ("neq_X2_0", "Y2_0", "Y3_0", "X2_1"),
            ]

        round_idx: int
            当前轮次编号，用于自动命名。
        ------------------------------
        return: str
            拼接好的多行 CVC 约束字符串。
        neq_X1_0 代表：“在 Y0_0, Y1_0, X1_1 三者之间存在不一致差分的比特掩码”。
        """
        constraint = []
        for neq_var, y_left, y_right, x_next in relations:
            expr = f"~(BVXOR(~{y_left}, {y_right}) & BVXOR(~{y_left}, {x_next}))"
            constraint.append(f"ASSERT({neq_var} = {expr});")
        return "\n".join(constraint)

        

if __name__ == '__main__':
    diff = Difference(
        Blocksize=128,
        Round=3,
        Branch_number=4,
        Sbox_bit=32,
        Sbox_content=[],
        Matrix=[],
        NonlinearType="xor"
    )
    varnames = ["neq_X1_0", "neq_X2_0"]
    print(diff.generate_diff_count(varnames, 32, 0))
    


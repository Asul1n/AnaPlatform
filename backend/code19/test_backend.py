# test_backend.py
from Root import Root
from Run_test import DifferentialAnalyse, LinearAnalyse

# ---------- 配置最小测试参数 ----------
Blocksize = 8          # 小块大小方便快速测试
Round = 1              # 轮数少
Branch_number = 2
Sbox_bit = 3
# 简单的 S-box，例如恒等映射
Sbox_content = [0, 1, 2, 3, 4, 5, 6, 7]
# 简单线性矩阵（单位矩阵）
Matrix = [[1, 0], [0, 1]]
NonlinearType = "Sbox"

# ---------- 创建 Root 对象 ----------
root_obj = Root(Blocksize, Round, Branch_number, Sbox_bit, Sbox_content, Matrix, NonlinearType)
print("Root 对象创建成功。")

# ---------- 差分分析 ----------
print("\n==========差分分析==========")
diff_result = DifferentialAnalyse(Blocksize, Round, Branch_number, Sbox_bit, Sbox_content, Matrix, NonlinearType)
for line in diff_result:
    print(line)

# ---------- 线性分析 ----------
print("\n==========线性分析==========")
linear_result = LinearAnalyse(Blocksize, Round, Branch_number, Sbox_bit, Sbox_content, Matrix, NonlinearType)
for line in linear_result:
    print(line)

print("\n后端最小规模测试完成！请确认打印输出和 DC 文件是否生成。")

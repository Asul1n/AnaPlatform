import json
import os
import sys
from DIF import Difference

def run_analysis_from_file(filename="round.json"):
    # 1. 获取文件的绝对路径（防止在不同目录下运行找不到文件）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)

    print(f"[*] 正在尝试读取文件: {file_path}")

    # 2. 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"[!] 错误: 找不到文件 {filename}")
        return

    # 3. 读取 JSON 文件
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            topology_data = json.load(f)
        print("[*] JSON 读取成功！")
    except json.JSONDecodeError as e:
        print(f"[!] JSON 格式错误: {e}")
        return
    except Exception as e:
        print(f"[!] 读取文件时发生错误: {e}")
        return

    # 4. 提取基本参数
    try:
        basic_params = topology_data.get('basicParams', {})
        block_size = basic_params.get('blockSize', 128)
        round_num = basic_params.get('roundNum', 8)
        branch_num = basic_params.get('branchNum', 4)
        algo_name = basic_params.get('algorithmName', 'Unknown')

        print(f"[*] 算法: {algo_name}")
        print(f"[*] 参数: BlockSize={block_size}, Rounds={round_num}, Branches={branch_num}")

        # 5. 初始化分析器
        # 注意：这里会调用你写好的 Difference 类
        analyzer = Difference(
            Blocksize=block_size,
            Round=round_num,
            Branch_number=branch_num,
            Sbox_bit=8,         # 默认值
            Sbox_content=None,
            Matrix=None,
            NonlinearType='add' # 假设是模加/异或类算法
        )

        # 6. 注入拓扑结构 (这里会自动调用 RoundGraphParser 并过滤 Key)
        print("[*] 正在解析拓扑结构并生成约束...")
        analyzer.set_topology(topology_data)

        # 7. 运行求解
        # 确保 Difference 类里的文件写入路径是合法的
        print("[*] 开始生成 CVC 文件并调用 STP...")
        result = analyzer.analyze_and_solve(S_num=0)
        
        if result:
            print("\n[=] STP 求解器输出结果:")
            print(result)
        else:
            print("\n[!] 未能获取求解结果或求解出错。")

    except Exception as e:
        print(f"[!] 运行分析过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_analysis_from_file("round.json")
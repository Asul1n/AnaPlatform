import sys
import json
from DIF import Difference 


# JSON 数据 
json_data = {
  "basicParams": {
    "algorithmName": "LEA",
    "blockSize": 128,
    "branchNum": 4,
    "roundFunction": "F(x) = ...",
    "roundNum": 8,
    "note": ""
  },
  "roundFunction": {
    "nodes": [
      {
        "id": "N0uCFEThZGUxWgow6Y3s-",
        "name": "X0",
        "type": "plainVar",
        "ports": {
          "inputs": [],
          "outputs": []
        },
        "props": {
          "bitwidth": 128
        }
      },
      {
        "id": "vqyYLjI27mvzBd8zAmiyt",
        "name": "X3",
        "type": "plainVar",
        "ports": {
          "inputs": [],
          "outputs": []
        },
        "props": {
          "bitwidth": 128
        }
      },
      {
        "id": "w7VN285CGO4E7qa1VQMjS",
        "name": "X2",
        "type": "plainVar",
        "ports": {
          "inputs": [],
          "outputs": []
        },
        "props": {
          "bitwidth": 128
        }
      },
      {
        "id": "MCj8PVEtip6RiD3NhZETP",
        "name": "X1",
        "type": "plainVar",
        "ports": {
          "inputs": [],
          "outputs": []
        },
        "props": {
          "bitwidth": 128
        }
      },
      {
        "id": "k3xAp5-gocNraQKTrs5Fb",
        "name": "XOR1",
        "type": "xor",
        "ports": {
          "inputs": [
            "input1"
          ],
          "outputs": [
            "output1"
          ]
        }
      },
      {
        "id": "M_DBXJNbCuKLOvSinXvcC",
        "name": "K0",
        "type": "keyVar",
        "ports": {
          "inputs": [],
          "outputs": []
        },
        "props": {
          "bitwidth": 128
        }
      },
      {
        "id": "Xa1NAuBvk5MQnngIVFo80",
        "name": "K1",
        "type": "keyVar",
        "ports": {
          "inputs": [],
          "outputs": []
        },
        "props": {
          "bitwidth": 128
        }
      },
      {
        "id": "dX1GoNNH7lLH137NJzuIN",
        "name": "XOR2",
        "type": "xor",
        "ports": {
          "inputs": [
            "input1"
          ],
          "outputs": [
            "output1"
          ]
        }
      },
      {
        "id": "kOvH1SY02s0JasZZFQM9N",
        "name": "MODADD1",
        "type": "modadd",
        "ports": {
          "inputs": [
            "input1"
          ],
          "outputs": [
            "output1"
          ]
        }
      },
      {
        "id": "R9wox-OBVEnhfryVNT3N0",
        "name": "ROTATE1",
        "type": "rotate",
        "ports": {
          "inputs": [
            "input1"
          ],
          "outputs": [
            "output1"
          ]
        },
        "props": {
          "direction": "left",
          "offset": 9,
          "bitwidth": 128
        }
      },
      {
        "id": "OZr-ZN4r2XpfVgioC4r2s",
        "name": "Y0",
        "type": "plainVar",
        "ports": {
          "inputs": [],
          "outputs": []
        },
        "props": {
          "bitwidth": 128
        }
      },
      {
        "id": "WXdxuoXaEoQgeAmMYvjVq",
        "name": "XOR3",
        "type": "xor",
        "ports": {
          "inputs": [
            "input1"
          ],
          "outputs": [
            "output1"
          ]
        }
      },
      {
        "id": "NZMtYadFwEkGGAN3zSNWE",
        "name": "K2",
        "type": "keyVar",
        "ports": {
          "inputs": [],
          "outputs": []
        },
        "props": {
          "bitwidth": 128
        }
      },
      {
        "id": "D1DgqmcqRduUz3oNX7lmG",
        "name": "K3",
        "type": "keyVar",
        "ports": {
          "inputs": [],
          "outputs": []
        },
        "props": {
          "bitwidth": 128
        }
      },
      {
        "id": "cuxSFmZq-Y6THQuCs5BEa",
        "name": "XOR4",
        "type": "xor",
        "ports": {
          "inputs": [
            "input1"
          ],
          "outputs": [
            "output1"
          ]
        }
      },
      {
        "id": "iy9fHBmQT_fHr5RqJLdwd",
        "name": "ROTATE2",
        "type": "rotate",
        "ports": {
          "inputs": [
            "input1"
          ],
          "outputs": [
            "output1"
          ]
        },
        "props": {
          "direction": "right",
          "offset": 5,
          "bitwidth": 128
        }
      },
      {
        "id": "I_PFQ3QYuTTGYU_OsNIbb",
        "name": "MODADD2",
        "type": "modadd",
        "ports": {
          "inputs": [
            "input1"
          ],
          "outputs": [
            "output1"
          ]
        }
      },
      {
        "id": "zolnHhEY6qwbOnA4uONGU",
        "name": "Y1",
        "type": "plainVar",
        "ports": {
          "inputs": [],
          "outputs": []
        },
        "props": {
          "bitwidth": 128
        }
      },
      {
        "id": "h_fGVbRIXBr9mu_o5qzUq",
        "name": "Ka",
        "type": "keyVar",
        "ports": {
          "inputs": [],
          "outputs": []
        },
        "props": {
          "bitwidth": 128
        }
      },
      {
        "id": "so6NS51gf5HFuk70B3ahq",
        "name": "K4",
        "type": "keyVar",
        "ports": {
          "inputs": [],
          "outputs": []
        },
        "props": {
          "bitwidth": 128
        }
      },
      {
        "id": "yItIkq4kZNXnQXNo1xv8d",
        "name": "XOR5",
        "type": "xor",
        "ports": {
          "inputs": [
            "input1"
          ],
          "outputs": [
            "output1"
          ]
        }
      },
      {
        "id": "H5lOW1mxBBb6hVqDbdvWo",
        "name": "XOR6",
        "type": "xor",
        "ports": {
          "inputs": [
            "input1"
          ],
          "outputs": [
            "output1"
          ]
        }
      },
      {
        "id": "HOhcUV3_nVeKNVTuNRgpC",
        "name": "MODADD3",
        "type": "modadd",
        "ports": {
          "inputs": [
            "input1"
          ],
          "outputs": [
            "output1"
          ]
        }
      },
      {
        "id": "R_Bmat8QbjubX4ureVqG3",
        "name": "ROTATE3",
        "type": "rotate",
        "ports": {
          "inputs": [
            "input1"
          ],
          "outputs": [
            "output1"
          ]
        },
        "props": {
          "direction": "right",
          "offset": 3,
          "bitwidth": 128
        }
      },
      {
        "id": "JMG7sHpvvXYc4FwxMmsR1",
        "name": "Y2",
        "type": "plainVar",
        "ports": {
          "inputs": [],
          "outputs": []
        },
        "props": {
          "bitwidth": 128
        }
      },
      {
        "id": "-Ueae4TwJt3KvdHaa-jtU",
        "name": "Y3",
        "type": "plainVar",
        "ports": {
          "inputs": [],
          "outputs": []
        },
        "props": {
          "bitwidth": 128
        }
      }
    ],
    "edges": [
      {
        "source": "X0",
        "target": "XOR1_input1"
      },
      {
        "source": "K0",
        "target": "XOR1_input1"
      },
      {
        "source": "K1",
        "target": "XOR2_input1"
      },
      {
        "source": "X1",
        "target": "XOR2_input1"
      },
      {
        "source": "XOR1_output1",
        "target": "MODADD1_input1"
      },
      {
        "source": "XOR2_output1",
        "target": "MODADD1_input1"
      },
      {
        "source": "MODADD1_output1",
        "target": "ROTATE1_input1"
      },
      {
        "source": "ROTATE1_output1",
        "target": "Y0"
      },
      {
        "source": "X1",
        "target": "XOR3_input1"
      },
      {
        "source": "K2",
        "target": "XOR3_input1"
      },
      {
        "source": "K3",
        "target": "XOR4_input1"
      },
      {
        "source": "X2",
        "target": "XOR4_input1"
      },
      {
        "source": "XOR3_output1",
        "target": "MODADD2_input1"
      },
      {
        "source": "XOR4_output1",
        "target": "MODADD2_input1"
      },
      {
        "source": "MODADD2_output1",
        "target": "ROTATE2_input1"
      },
      {
        "source": "ROTATE2_output1",
        "target": "Y1"
      },
      {
        "source": "X2",
        "target": "XOR5_input1"
      },
      {
        "source": "K4",
        "target": "XOR5_input1"
      },
      {
        "source": "Ka",
        "target": "XOR6_input1"
      },
      {
        "source": "X3",
        "target": "XOR6_input1"
      },
      {
        "source": "XOR5_output1",
        "target": "MODADD3_input1"
      },
      {
        "source": "XOR6_output1",
        "target": "MODADD3_input1"
      },
      {
        "source": "MODADD3_output1",
        "target": "ROTATE3_input1"
      },
      {
        "source": "ROTATE3_output1",
        "target": "Y2"
      },
      {
        "source": "X0",
        "target": "Y3"
      }
    ]
  },
  "isLastRoundDifferent": False,
  "lastRoundFunction": None
}


def main():
    """主测试函数，用于实例化 Difference 类并生成约束。"""
    
    print("--- 🔬 开始 Difference 类测试运行 ---")
    
    # --- 1. 解析基本参数 ---
    basic_params = json_data.get('basicParams', {})
    block_size_per_branch = basic_params.get('blockSize') # 128
    branch_num = basic_params.get('branchNum')           # 4
    total_rounds = basic_params.get('roundNum')          # 8
    block_size_total = block_size_per_branch * branch_num # 512

    print(f"1. 解析基本参数: 总位宽={block_size_total} bits, 分支数={branch_num}, 总轮数={total_rounds}")
    print("-" * 30)

    # --- 2. 实例化 Difference 类 ---
    try:
        cipher = Difference(
            Blocksize=block_size_total, 
            Round=total_rounds, 
            Branch_number=branch_num, 
            # 假设 Sbox_bit, Sbox_content, Matrix, NonlinearType 都有默认值或被正确处理
            Sbox_bit=8, 
            Sbox_content=[], 
            Matrix=[], 
            NonlinearType='add' 
        )
    except ImportError as e:
        print(f"❌ 导入错误: 请确保您的 `DIF.py` (包含 Difference 类) 和其依赖项 (如 Root) 存在且可导入。错误信息: {e}")
        return
    except Exception as e:
        print(f"❌ 实例化 Difference 时出错: {e}")
        return

    print("2. 实例化 Difference 类... 成功")

    # --- 3. 注入拓扑结构 ---
    try:
        cipher.set_topology(json_data) 
    except Exception as e:
        print(f"❌ 设置拓扑 (set_topology) 时出错: 请检查您的 RoundGraphParser 实现是否正确。错误信息: {e}")
        return
    
    print("3. 注入拓扑结构... 成功")

    # --- 4. 生成约束 ---
    try:
        constraints = cipher.genEncryptSubjection(total_rounds) 
        vars_decl = cipher.getVars(total_rounds) # 必须在 genEncryptSubjection 之后调用
    except Exception as e:
        print(f"❌ 生成约束 (genEncryptSubjection/getVars) 时出错: 请检查约束生成逻辑。错误信息: {e}")
        return
    
    print(f"4. 生成约束和变量声明... 成功生成 {len(constraints)} 条约束。")
    print("-" * 30)
    
    # --- 5. 打印结果摘要 ---
    
    print("## 变量声明 (Variables Declaration) 📝")
    print(f"总变量声明块数: {len(vars_decl)}")
    print("\n--- 变量示例 (前 2 个声明块) ---")
    for v in vars_decl[:2]:
        print(f"VAR\n  {v}")
    
    print("\n" + "=" * 40)
    
    print(f"## 约束 (Constraints) 🔗")
    print(f"总约束条数: {len(constraints)}")
    print("\n--- 约束示例 (第 1 轮的前 10 条) ---")
    
    # 打印前 10 条约束
    for i, c in enumerate(constraints):
        if i < 10:
            print(f"  {c}")
    
    # 查找并打印一条轮间连接约束
    round_conn_example = next((c for c in constraints if "_r1" in c and "_r2" in c), None)
    if round_conn_example:
        print("\n--- 轮间连接约束示例 (Round 1 -> Round 2) ---")
        print(f"  {round_conn_example}")
    
    print("\n--- ✅ 测试执行完毕 ---")


if __name__ == "__main__":
    main()
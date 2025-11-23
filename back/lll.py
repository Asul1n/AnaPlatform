from NodeDispatcher import IRBuilder
from NodeDispatcher.dispatcher import NodeDispatcher
from NodeDispatcher.registry import NodeRegistry
from core.dif import Difference

json = {
  "algorithm": "Ballet",
  "block_size": 128,
  "word_size": 32,
  "rounds": 2,
  "branch_number": 4,

  "nodes": [
    { "id": "X0", "type": "INPUT", "bits": 16 },
    { "id": "X1", "type": "INPUT", "bits": 16 },
    { "id": "X2", "type": "INPUT", "bits": 16 },
    { "id": "X3", "type": "INPUT", "bits": 16 },

    { "id": "r0", "type": "ROTATE_LEFT", "params": { "amount": 6 } },
    { "id": "r1", "type": "ROTATE_LEFT", "params": { "amount": 15 } },
    { "id": "sum0", "type": "ADD_MOD", "params": { "mod": "2^16" } },
    { "id": "sum1", "type": "ADD_MOD", "params": { "mod": "2^16" } },
    { "id": "xor0", "type": "XOR" },
    { "id": "xor1", "type": "XOR" },
    { "id": "rot0", "type": "ROTATE_LEFT", "params": { "amount": 9 } },
    { "id": "rot1", "type": "ROTATE_LEFT", "params": { "amount": 14 } },
    { "id": "swapL", "type": "SWAP" },
    { "id": "swapR", "type": "SWAP" },

    { "id": "Y0", "type": "OUTPUT", "bits": 16 },
    { "id": "Y1", "type": "OUTPUT", "bits": 16 },
    { "id": "Y2", "type": "OUTPUT", "bits": 16 },
    { "id": "Y3", "type": "OUTPUT", "bits": 16 }
  ],

  "edges": [
    { "source": "X0", "target": "r0" },
    { "source": "X2", "target": "r1" },

    { "source": "r0", "target": "sum0" },
    { "source": "X1", "target": "sum0" },
    { "source": "r1", "target": "sum1" },
    { "source": "X3", "target": "sum1" },

    { "source": "sum0", "target": "xor0" },
    { "source": "sum1", "target": "xor1" },
    { "source": "subkey_L", "target": "xor0" },
    { "source": "subkey_R", "target": "xor1" },

    { "source": "xor0", "target": "rot0" },
    { "source": "xor1", "target": "rot1" },

    { "source": "rot0", "target": "swapL" },
    { "source": "rot1", "target": "swapR" },
    { "source": "X1", "target": "swapL" },
    { "source": "X3", "target": "swapR" },

    { "source": "swapL_out0", "target": "Y0" },
    { "source": "swapL_out1", "target": "Y1" },
    { "source": "swapR_out0", "target": "Y2" },
    { "source": "swapR_out1", "target": "Y3" }
  ],

  "variables": {
    "subkey_L": { "type": "KEY_PART", "bits": 16 },
    "subkey_R": { "type": "KEY_PART", "bits": 16 }
  }
}

if __name__ == '__main__':
    
  dif_parser = Difference(json["block_size"],json["rounds"],json["branch_number"])

  # print(dif_parser.declare_var())

  # registry = NodeRegistry(json)

  # registry.summary()
  # 初始化注册表
  registry = NodeRegistry(json)
  registry.summary()

  # 初始化分发器
  dispatcher = NodeDispatcher(dif_parser)

  # 一键运行
  dispatcher.run(registry)
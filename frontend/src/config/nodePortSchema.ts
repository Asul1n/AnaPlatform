export type PortList = string[]

// pattern: base name + count -> base1, base2, ...
export type PortPattern = {
  pattern: string       // e.g. "input" 或 "output"
  count: number         // e.g. 4 -> input1..input4
  startIndex?: number   // 默认 1
  pad?: number          // 可选数字位数填充 e.g. pad=2 => 01,02
}

// alias: 引用其他节点类型的 ports
export type PortAlias = {
  aliasOf: string
}

// factory: 根据节点 props 动态生成 ports
export type PortFactory = (props?: Record<string, any>) => { inputs: PortList, outputs: PortList }

// 单一声明可以是任意一种，或数组混合
export type PortSpec = PortList | PortPattern | PortAlias | PortFactory

export type NodePortSchemaItem = {
  inputs?: PortSpec | PortSpec[]
  outputs?: PortSpec | PortSpec[]
}

export type NodePortSchema = Record<string, NodePortSchemaItem | ((props?: any) => NodePortSchemaItem)>

export const nodePortSchema: NodePortSchema = {
  // 固定 list（最简单）
  Sbox: {
    inputs: ["S_in"],
    outputs: ["S_out"]
  },

  // pattern + count（更通用）
  Shift: {
    inputs: { pattern: "input", count: 4 },
    outputs: { pattern: "output", count: 4 }
  },

  // 别名：直接复用其他类型定义
  MyShiftAlias: { inputs: [{ aliasOf: "Shift" }], outputs: [{ aliasOf: "Shift" }] },

  // 工厂函数：根据 props（例如 width/size/ports）动态生成
  NarrowBlock: (props?: any) => {
    const n = (props?.numPorts ?? 2)
    return {
      inputs: { pattern: "in", count: n },
      outputs: { pattern: "out", count: n }
    }
  },

  // 混合写法：固定 + pattern
  Xor: {
    inputs: ["XOR_input1", "XOR_input2"],
    outputs: ["XOR_output"]
  },

  // 默认可省略，使用回退策略生成 input1/output1
}
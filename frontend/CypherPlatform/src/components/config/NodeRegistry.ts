import type { ShiftProps } from "../panels/type"

export interface NodePropertyPanel<P extends object = object> {
  /** 对应属性编辑 Vue 组件名（注册在 /components/property-panels 下） */
  component: string
  /** 属性定义（用于动态渲染或默认值初始化） */
  schema: P
}

export interface NodeConfig<P extends object = Record<string, unknown>> {
  type: string                       // 节点类型
  label: string                      // UI  显示名称
  icon: string                       // svg 文件路径
  bitvector: number                  // 位宽（对应 Blocksize / Branchsize）
  inputs: string[]                   // 输入变量
  outputs: string[]                  // 输出变量
  props?: P                          // 自定义属性
  vueRender: string                  // 拖拽到画板上的对应渲染视图
  /** 可选：如果节点有可配置属性面板，则定义它 */
  propertyPanel?: NodePropertyPanel<P>
}

// 节点注册表，用于注册或描述平台中的可用节点类型
export const nodeRegistry: NodeConfig[] = [
  // ----------------- 输入节点 -----------------
  {
    type: 'plainVar',
    label: 'Input模块',
    icon: '/icons/input.svg',
    bitvector: 8,
    inputs: [],
    outputs: ['X1'],
    vueRender: "PlainVarNode",
    propertyPanel: {
      component: 'PlainVarPropertyPanel',
      schema: { name: 'X1', width: 8 }
    }
  },
  {
    type: 'keyVar',
    label: '密钥输入',
    icon: '/icons/keyword.svg',
    bitvector: 8,
    inputs: [],
    outputs: ['K1'],
    vueRender: "KeyVarNode",
    propertyPanel: {
      component: 'KeyVarPropertyPanel',
      schema: { name: 'K1', width: 8 }
    }
  },
  // ----------------- 线性操作 -----------------
  {
    type: 'xor',
    label: 'XOR 模块',
    icon: '/icons/xor.svg',
    bitvector: 8,
    inputs: ['in1', 'in2'],
    outputs: ['out'],
    vueRender: "XorNode"
  },{
    type: 'rotate',
    label: 'Rotate 模块',
    icon: '/icons/rotate.svg',
    bitvector: 8,
    inputs: ['in1', 'in2'],
    outputs: ['out'],
    vueRender: "RotateNode"
    ,
    propertyPanel: {
      component: 'RotatePropertyPanel',
      schema: {                         // 定义默认属性
        direction: 'left',
        shift: 1,
        width: 8,
      } satisfies ShiftProps, // ✅ 类型约束更安全
    }
  },
  // ----------------- 非线性操作 -----------------
  {
    type: 'Sbox',
    label: 'S盒',
    icon: '/icons/sbox.svg',
    bitvector: 8,
    inputs: ['in'],
    outputs: ['out'],
    vueRender: "SboxNode",
    propertyPanel: {
       component: 'SboxPropertyPanel',
       schema: {
        sboxId: 1,
        sboxBit: 8,
        sboxTabel: []
      }
    }
  },{
    type: 'modadd',
    label: '模加',
    icon: '/icons/mod_plus.svg', // 请自行放置或替换图标路径
    bitvector: 8,
    inputs: ['A', 'B'],
    outputs: ['SUM'],
    vueRender: "ModAddNode",
    propertyPanel: {
      component: 'ModAddPropertyPanel',
      schema: {
        modulus: 256,
        width: 8,
        signed: false
      }
    }
  },
  // ----------------- 常用辅助节点 -----------------
  {
    type: 'constant',
    label: '常量',
    icon: '/icons/constant.svg',
    bitvector: 8,
    inputs: [],
    outputs: ['out'],
    vueRender: "ConstantNode",
    propertyPanel: {
      component: 'ConstPropertyPanel',
      schema: { value: 0x0F, width: 8 }
    }
  }
]

/* 节点与边的全局状态管理（Pinia 版本）
 * --------------------------------------------------------
 * 负责管理：
 *   - nodes
 *   - edges
 *   - selectedNodeId
 *   - updateNodeProps
 *   - resolveNodeComponent
 *   - getDefaultProps
 */

import { defineStore } from 'pinia'
import type { Edge } from '@vue-flow/core'
import type { SBoxProps, ShiftProps, PlainVarProps, KeyVarProps } from '@/components/panels/type'
import { nodeRegistry } from '@/components/config/NodeRegistry'
import { nodeComponentMap } from '@/components/config/nodeComponentMap'

/**
 * NodeTypeMap
 * --------------------------------------------------------
 * 定义画布上不同类型节点的 "props"（属性面板） 类型映射表。
 */
export type NodeTypeMap = {
  Sbox: SBoxProps,
  Shift: ShiftProps,
  PlainVar: PlainVarProps,
  KeyVar: KeyVarProps
}



/**
 * CanvasNode 接口
 * --------------------------------------------------------
 * 定义单个画布节点的数据结构。
 * 泛型 <T> 限定了节点类型及其 props 类型。
 */
export interface CanvasNode<T extends keyof NodeTypeMap = keyof NodeTypeMap> {
  id: string               // 节点唯一标识
  type: string             // 节点类型（如 'Sbox', 'Shift'）
  position: { x: number, y: number }   // 节点在画布上的 X,Y 坐标
  data: {
    label?: string                     // 可选标签，用于显示节点名
    props: NodeTypeMap[T]              // 该节点对应的属性对象（根据类型映射）
  }
}

/**
 * useNodeStore
 * --------------------------------------------------------
 * 封装对 state 的增删改操作，暴露给组件使用。
 * 类似一个简单的 Pinia/Vuex 状态模块，但更轻量。
 */
export const useNodeStore = defineStore('nodeStore', {
  /**
   * 全局 state
   * --------------------------------------------------------
   * 使用 Vue 的 reactive() 创建响应式全局状态。
   * 包含：
   *   - nodes：当前画布中所有节点的数组
   *   - edges：当前画布中所有连线的数组
   *   - selectedNodeId：当前选中节点的 ID
   */
  state: () => ({
    nodes: [] as CanvasNode[],
    edges: [] as Edge[],
    selectedNodeId: '' as string
  }),

  // getters：计算属性
  getters: {
    selectedNode(state) {
      return state.nodes.find(n => n.id === state.selectedNodeId) || null
    }
  },

  // actions：对 state 的操作
  actions: {
    // 自动找到某类型对应的渲染组件
    resolveNodeComponent(type: string) {
      const comp = nodeComponentMap[type]
      if (!comp) console.warn(`[useNodeStore] 未找到渲染组件: ${type}`)
      return comp
    },

    // 自动找到默认属性
    getDefaultProps(type: string) {
      const config = nodeRegistry.find(n => n.type === type)
      return config?.propertyPanel?.schema
        ? structuredClone(config.propertyPanel.schema)
        : {}
    },

    // 添加节点
    addNode<T extends keyof NodeTypeMap>(node: CanvasNode<T>) {
      this.nodes.push(node)
    },

    // 更新 props
    updateNodeProps<T extends keyof NodeTypeMap>(nodeId: string, props: NodeTypeMap[T]) {
      const node = this.nodes.find(n => n.id === nodeId)
      if (node) Object.assign(node.data.props, props)
    },

    // 设置选中节点
    setSelected(nodeId: string | null) {
      this.selectedNodeId = nodeId ?? ''
    }
  }
})


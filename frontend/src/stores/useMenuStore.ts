// stores/useMenuStore.ts
import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'
import { useNodeStore } from './useNodeStore'
import { useEdgeStore } from './useEdgeStore'

interface MenuTarget {
  type: 'node' | 'edge'
  id: string
}

interface MenuPosition {
  x: number
  y: number
}

export const useMenuStore = defineStore('menuStore', () => {
  const nodeStore = useNodeStore()
  const edgeStore = useEdgeStore()

  /** 右键菜单显示状态 */
  const visible = ref(false)
  
  /** 菜单位置 */
  const position = reactive<MenuPosition>({ x: 0, y: 0 })
  
  /** 菜单目标：节点或边 */
  const target = ref<MenuTarget | null>(null)

  /** 显示右键菜单 */
  function showMenu(x: number, y: number, type: MenuTarget['type'], id: string) {
    visible.value = true
    position.x = x
    position.y = y
    target.value = { type, id }
    
    // 确保菜单位置在可视区域内
    adjustMenuPosition()
  }

  /** 隐藏右键菜单 */
  function hideMenu() {
    visible.value = false
    target.value = null
  }

  /** 调整菜单位置，确保在可视区域内 */
  function adjustMenuPosition() {
    const menuWidth = 120
    const menuHeight = 40
    const viewportWidth = window.innerWidth
    const viewportHeight = window.innerHeight

    if (position.x + menuWidth > viewportWidth) {
      position.x = viewportWidth - menuWidth - 10
    }
    if (position.y + menuHeight > viewportHeight) {
      position.y = viewportHeight - menuHeight - 10
    }
  }

  /** 删除目标节点或边 */
  function deleteTarget() {
    if (!target.value) return

    const { type, id } = target.value
    
    if (type === 'node') {
      // 删除节点及相关边
      edgeStore.removeNodeEdges(id)
      nodeStore.removeNode(id)
    } else if (type === 'edge') {
      // 删除边
      edgeStore.removeEdges(id)
    }

    hideMenu()
  }

  /** 获取当前目标信息（用于调试） */
  function getTargetInfo() {
    if (!target.value) return null
    
    const { type, id } = target.value
    if (type === 'node') {
      const node = nodeStore.nodes.find(n => n.id === id)
      return { type, id, label: node?.data.label }
    } else {
      const edge = edgeStore.edges.find(e => e.id === id)
      return { type, id, source: edge?.source, target: edge?.target }
    }
  }

  return {
    // 状态
    visible,
    position,
    target,
    
    // 方法
    showMenu,
    hideMenu,
    deleteTarget,
    getTargetInfo
  }
})
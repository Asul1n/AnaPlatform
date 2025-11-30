// src/composables/useDeleteHandler.ts
import { onMounted, onBeforeUnmount } from 'vue'
import { useVueFlow } from '@vue-flow/core'

export function useDeleteHandler() {
  const { getSelectedNodes, getSelectedEdges, removeNodes, removeEdges } = useVueFlow()

  // 键盘 Delete / Backspace 删除
  const onKey = (e: KeyboardEvent) => {
    if (e.key !== 'Delete' && e.key !== 'Backspace') return

    // 避免在输入框中误删
    const target = e.target as HTMLElement
    if (['INPUT', 'TEXTAREA'].includes(target.tagName) || target.isContentEditable) {
      return
    }

    const nodes = getSelectedNodes()
    const edges = getSelectedEdges()

    if (nodes.length) removeNodes(nodes.map(n => n.id))
    if (edges.length) removeEdges(edges.map(e => e.id))
  }

  // 右键删除菜单（简单直接：监听 contextmenu 事件）
  const onContextMenu = (e: MouseEvent) => {
    const el = e.target as HTMLElement

    // 找最近的 node 或 edge
    const nodeEl = el.closest('.vue-flow__node')
    const edgeEl = el.closest('.vue-flow__edge')

    if (nodeEl) {
      const id = nodeEl.getAttribute('data-id')
      if (id) removeNodes([id])
    }

    if (edgeEl) {
      const id = edgeEl.getAttribute('data-id')
      if (id) removeEdges([id])
    }
  }

  onMounted(() => {
    window.addEventListener('keydown', onKey)
    window.addEventListener('contextmenu', onContextMenu)
  })
  onBeforeUnmount(() => {
    window.removeEventListener('keydown', onKey)
    window.removeEventListener('contextmenu', onContextMenu)
  })
}

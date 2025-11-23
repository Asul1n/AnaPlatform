/* useUIStore — 专门管理 UI 状态（面板、选中状态）
  处理：
  * activePanel（显示哪个页面）
  * selectedMode（自动 / 固定 / 受限）
  * 是否显示属性面板 showPropPanel
  * 当前应该显示的 panelComponent */

/* useUIStore — 管理 UI 面板状态 + VueFlow 双向绑定代理 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useNodeStore } from './useNodeStore'
import { nodeRegistry } from '@/components/config/NodeRegistry'

export const useUIStore = defineStore('uiStore', () => {
  const nodeStore = useNodeStore()

  /** 页面面板 */
  const activePanel = ref<'editor' | 'params' | 'results' | 'mode'>('editor')
  const selectedMode = ref<'auto' | 'fixed' | 'constraint'>('auto')

  function setActive(panel: typeof activePanel.value) {
    activePanel.value = panel
  }

  /** 属性面板 */
  const showPropPanel = ref(false)
  function openPropPanel() { showPropPanel.value = true }
  function closePropPanel() { showPropPanel.value = false }

  /** 当前选中节点 */
  const selectedNode = computed(() => nodeStore.selectedNode)

  /** 自动加载 panels */
  const modules = import.meta.glob('@/components/panels/*.vue', { eager: true })
  const panelMap: Record<string, any> = {}
  for (const path in modules) {
    const name = path.split('/').pop()!.replace('.vue', '')
    panelMap[name] = (modules[path] as any).default
  }

  /** 当前节点对应的 panel 组件 */
  const panelComponent = computed(() => {
    const node = selectedNode.value
    if (!node) return null
    const entry = nodeRegistry.find(r => r.type === node.type)
    const name = entry?.propertyPanel?.component
    return name ? panelMap[name] : null
  })

  /** 属性面板 v-model 代理 */
  const selectedNodeModel = computed({
    get: () => selectedNode.value ? JSON.parse(JSON.stringify(selectedNode.value.data.props))
 : null,
    set: (v) => {
      const n = selectedNode.value
      if (!n || !v) return
      nodeStore.updateNodeProps(n.id, v)
    }
  })

  /** VueFlow v-model:selected-nodes 代理 */
  const selectedNodeIds = computed({
    get: () => nodeStore.selectedNodeId ? [nodeStore.selectedNodeId] : [],
    set: (arr: string[]) => nodeStore.setSelected(arr[0] ?? '')
  })

  return {
    activePanel,
    setActive,
    selectedMode,

    showPropPanel,
    openPropPanel,
    closePropPanel,

    selectedNode,
    panelComponent,
    selectedNodeModel,
    selectedNodeIds
  }
})

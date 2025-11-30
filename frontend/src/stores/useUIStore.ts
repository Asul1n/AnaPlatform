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
import { useEdgeStore } from './useEdgeStore'
import { nodeRegistry } from '@/config/NodeRegistry'
import { useResultStore } from './useResultStore'

export const useUIStore = defineStore('uiStore', () => {
  const nodeStore = useNodeStore()
  const edgeStore = useEdgeStore()

  /** 流程阶段状态 */
  const analysisStep = ref<'build' | 'mode_select' | 'analyzing' | 'results'>('build')

  /** 页面面板 */
  const activePanel = ref<'editor' | 'params' | 'results' | 'mode'>('editor')
  const selectedMode = ref<'auto' | 'fixed' | 'constraint'>('auto')

  const showSnapshotPanel = ref(false);    // 控制快照管理面板的显示

  function setStep(step: typeof analysisStep.value) {
      analysisStep.value = step
      // 当退出结果展示时，确保画布是可见的
      if (step !== 'results') {
          setActive('editor')
      }
  }

  function setActive(panel: typeof activePanel.value) {
    // 强制流程：如果不是 'build' 或 'mode_select' 阶段，不允许修改参数
    if (panel === 'params' && analysisStep.value === 'results') {
        console.warn('Analysis is complete. Cannot change basic parameters now.')
        return
    }
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

  /** VueFlow v-model:selected-edges 代理 */
  const selectedEdgeIds = computed({
    get: () => edgeStore.selectedEdgeIds,
    set: (arr: string[]) => edgeStore.selectedEdgeIds = arr
  })

  /** 删除节点和边 */
  function deleteSelected() {
    // 删除选中边
    edgeStore.removeEdges(selectedEdgeIds.value)
    selectedEdgeIds.value = []

    // 删除选中节点及其相关边
    selectedNodeIds.value.forEach(id => {
      edgeStore.removeNodeEdges(id)
      nodeStore.removeNode(id)
    })
    selectedNodeIds.value = []
  }

  async function runAnalysis() {
      // 0. 前置检查 (可以保留)
      if (analysisStep.value !== 'mode_select') {
          console.warn('请先完成模式选择！')
          return
      }
      
      // 1. 设置状态为 'analyzing'
      setStep('analyzing')
      
      try {
          // 2. 准备数据
          const graphData = { 
              nodes: useNodeStore().nodes, 
              edges: useEdgeStore().edges, 
              mode: selectedMode.value,
              // ... 其他参数如轮数等
          }
          console.log("发送数据到后端:", graphData)

          // 3. 实际后端调用 (这里仍然用 setTimeout 模拟)
          // await apiService.runAnalysis(graphData) 
          await new Promise(resolve => setTimeout(resolve, 3000))


          // 4. 成功完成，将状态推进到 'results'
          setStep('results')
          // 5. 自动跳转到结果展示面板
          setActive('results') 
          
          console.log("分析完成！")

      } catch (error) {
          console.error("分析失败:", error)
          // 失败处理：退回 'mode_select' 阶段，并给出提示
          setStep('mode_select') 
          // 可以在这里显示一个 Element Plus Notification/Message
          alert('分析运行失败，请检查图结构或网络。')

      }

      // 假设这是后端返回的数据
      const mockBackendData = { 
          diffPaths: [/* ... paths data ... */], 
          aggregatedResult: { /* ... summary data ... */ } 
      }
      
      // 4. 成功完成，调用 ResultStore 归档
      const resultStore = useResultStore()
      const nodeStore = useNodeStore()
      // 实际项目中，BasicParamsForm 的数据应该被保存在另一个 Store 中
      const mockBasicParams = { rounds: 10, branches: 2 } 

      resultStore.archiveNewAnalysis(
          selectedMode.value, 
          mockBasicParams, // ⚠️ 替换为实际参数 store 的数据
          { nodes: nodeStore.nodes, edges: useEdgeStore().edges }, // 图快照
          mockBackendData
      )

      // 5. 将流程状态推进到 'results'
      setStep('results')
      setActive('results')
  }

  function toggleSnapshotPanel() {
    console.log('快照面板状态切换前:', showSnapshotPanel.value); // 调试点 A
    showSnapshotPanel.value = !showSnapshotPanel.value;
    console.log('快照面板状态切换后:', showSnapshotPanel.value); // 调试点 B
  }




  return {
    activePanel,
    setActive,
    selectedMode,
    analysisStep,
    setStep,

    showPropPanel,
    openPropPanel,
    closePropPanel,

    selectedNode,
    panelComponent,
    selectedNodeModel,

    selectedNodeIds,
    selectedEdgeIds,

    deleteSelected,
    runAnalysis,
    showSnapshotPanel,
    toggleSnapshotPanel
  }
})

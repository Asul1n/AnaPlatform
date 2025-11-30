<template>
  <div class="layout">
    <!-- 左侧组件库 -->
    <aside class="sidebar">
      <div class="sidebar-top">
        <div class="param-header">
          <el-button
            type="primary"
            size="large"
            class="param-btn"
            @click="ui.setActive('params')"
            :disabled="ui.analysisStep === 'results'"
          >
            ⚙️ 基本参数设置
          </el-button>
          <p class="param-desc">配置轮数、分支数等基础信息</p>
        </div>
      </div>

      <div class="sidebar-top">
        <div class="param-header">
          <el-button
            type="warning"
            size="large"
            class="param-btn"
            @click="ui.setActive('mode')"
            :disabled="ui.analysisStep === 'analyzing'"
          >
            🧩 分析模式
          </el-button>
          <p class="param-desc">
            {{ 
              ui.analysisStep === 'build' 
              ? '第一步：搭建轮函数' 
              : (ui.analysisStep === 'mode_select' 
                ? '模式已选，可点击下方“运行”' 
                : '') 
            }}
          </p>
        </div>
      </div>

      <div class="sidebar-top">
        <div class="param-header">
          <el-button
            type="success"
            size="large"
            class="param-btn"
            :loading="ui.analysisStep === 'analyzing'"
            :disabled="ui.analysisStep !== 'mode_select'" @click="onRunAnalysis" >
            <span v-if="ui.analysisStep === 'analyzing'">⏳ 正在分析...</span>
            <span v-else>🚀 运行分析</span>
          </el-button>
          <p class="param-desc" v-if="ui.analysisStep === 'build'">请先配置模式</p>
        </div>
      </div>

      <div class="sidebar-top">
        <div class="param-header">
          <el-button
            type="info"
            size="large"
            class="param-btn"
            @click="ui.setActive('results')"
            :disabled="ui.analysisStep !== 'results'" >
            📊 结果展示
          </el-button>
          <p class="param-desc" v-if="ui.analysisStep !== 'results'">分析完成后解锁</p>
        </div>
      </div>

      <!-- 组件库 -->
      <div class="node-library-wrapper">
        <NodeLibrary :draggable-nodes="draggableNodes" />
      </div>

      <div>
        <el-button type="info" size="default" @click="onExportClick">
          📤 导出 JSON
        </el-button>
      </div>

      <div class="param-header">
          <el-button
              type="info"
              size="large"
              class="param-btn"
              @click="onSaveSnapshot" >
              💾 保存画布状态
          </el-button>
          <p class="param-desc">保存当前节点/边配置，随时复现</p>
      </div>

      <div class="param-header">
          <el-button
              type="default"
              size="large"
              class="param-btn"
              @click="ui.toggleSnapshotPanel" >
              🖼️ 管理/恢复快照 ({{ Object.keys(analysisStore.savedSnapshots).length }})
          </el-button>
          <p class="param-desc">查看和加载已保存的配置</p>
      </div>

      <div class="param-header">
          <el-button
              type="warning"
              size="large"
              class="param-btn"
              @click="onSaveLastRound" 
          >
              💾 保存为最后一轮函数
          </el-button>
          <p class="param-desc" v-if="analysisStore.isLastRoundDifferent">
              ✅ 最后一轮已配置
          </p>
          <p class="param-desc" v-else>
              配置 Feistel 结构的特殊最后一轮
          </p>
      </div>
    </aside>

  

    <!-- 中间画布 -->
    <main class="canvas-area">
      <!-- 参数面板 -->
      <transition name="fade">
        <div v-if="ui.activePanel === 'params'" class="param-overlay">
          <BasicParamsForm />
          <el-button type="primary" @click="() => { ui.setActive('editor'); ui.setStep('build') }">
            保存并返回画布
          </el-button>
        </div>
      </transition>

      <!-- 结果面板 -->
      <transition name="fade">
        <div v-if="ui.activePanel === 'results'" class="param-overlay">
          <Display />
          <el-button type="primary" @click="ui.setActive('editor')">返回画布</el-button>
        </div>
      </transition>

      <!-- 分析模式面板 -->
      <transition name="fade">
        <div v-if="ui.activePanel === 'mode'" class="param-overlay">
          <AnaModeSelector v-model:selectedMode="ui.selectedMode" />
          <el-button type="primary" 
            @click="() => { ui.setActive('editor'); ui.setStep('mode_select') }"
          >
            确认模式并返回画布
          </el-button>
        </div>
      </transition>

      <!-- VueFlow 画布 -->
      <VueFlow
        class="flow"
        :node-types="nodeTypeMap"
        :default-edge-options="defaultEdgeOptions"
        v-model:selected-nodes="ui.selectedNodeIds"
        v-model:selected-edges="ui.selectedEdgeIds"
        v-model:nodes="nodeStore.nodes"
        v-model:edges="edgeStore.edges"
        @nodes-change="onNodesChange"
        @connect="onConnect"
        @drop="onDrop"
        @node-click="onNodeClick"
        @node-context-menu="onRightClickNode"
        @edge-context-menu="onRightClickEdge"
        @pane-context-menu="onRightClickPane"

        @dragover.prevent
      >
        <Background />

        <!-- 初始引导提示层 -->
         <template v-if="nodeStore.nodes.length === 0 && ui.activePanel === 'editor'">
          <div class="canvas-hint">
            <h3>欢迎来到带条件聚合类路线自动化分析平台</h3>
            <p>👉 从左侧拖入节点以构建分析路径</p>
            <p>⚙️ 点击 <b>分析模式</b> 选择聚合策略</p>
            <p>📊 点击 <b>结果展示</b> 查看差分路径与聚合结果</p>
          </div>
         </template>

        <!-- 自定义节点渲染 -->
        <template #node-default="{ data }">
          <div class="node-wrapper vertical">
            <!-- inputs（左侧或上方）-->
            <div class="handles inputs">
              <template v-for="(port, idx) in (data.ports?.inputs || [])" :key="port">
                <!-- 把 Handle id 设为端口名（不包含节点 id） -->
                <Handle
                  type="target"
                  :id="port"
                  :position="Position.Top"
                  class="node-handle"
                  :style="{ left: ( (idx+1) * 100 / ((data.ports.inputs.length||1) + 1) ) + '%' }"
                />
              </template>
            </div>

            <div class="node-body">
              <component
                v-if="data.type"
                :is="nodeStore.resolveNodeComponent(data.type)"
                v-bind="data.props"
              />
              <template v-else>
                <img :src="data.icon" />
                <span>{{ data.label }}</span>
              </template>
            </div>

            <!-- outputs（右侧或下方）-->
            <div class="handles outputs">
              <template v-for="(port, idx) in (data.ports?.outputs || [])" :key="port">
                <Handle
                  type="source"
                  :id="port"
                  :position="Position.Bottom"
                  class="node-handle"
                  :style="{ left: ( (idx+1) * 100 / ((data.ports.outputs.length||1) + 1) ) + '%' }"
                />
              </template>
            </div>
          </div>
        </template>
      </VueFlow>

      <!-- 右键菜单 -->
      <ContextMenu/>

      <transition name="fade">
          <div v-if="ui.showSnapshotPanel" class="floating-snapshot-panel">
              <header class="floating-header">
                  <h4>画布快照与特殊轮函数管理</h4>
                  <button @click="ui.toggleSnapshotPanel">×</button>
              </header>
              <div class="floating-content">
                  <SnapshotManager 
                      @load-snapshot="onLoadSnapshot" 
                      @delete-snapshot="onDeleteSnapshot" 
                      @load-last-round="onLoadLastRound"
                      @clear-last-round="onClearLastRound"
                  />
              </div>
          </div>
      </transition>
    </main>

    <!-- 属性面板（右上角） -->
    <transition name="fade">
      <div v-if="ui.selectedNode  && ui.showPropPanel" class="floating-prop-panel">
        <header class="floating-header">
          <h4>{{ ui.selectedNode?.data.label || ui.selectedNode?.type }} 属性</h4>
          <button @click="ui.closePropPanel">×</button>
        </header>
        <div class="floating-content">
          <component
            v-if="ui.panelComponent"
            :is="ui.panelComponent"
            v-model="ui.selectedNodeModel"
            :key="ui.selectedNode?.id"
          />
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { VueFlow, Handle, Position, type NodeChange,  type Connection, MarkerType } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { useNodeStore } from '@/stores/useNodeStore'
import { useEdgeStore } from '@/stores/useEdgeStore'
import { useUIStore } from '@/stores/useUIStore'
import NodeLibrary from '@/components/NodeLibrary.vue'
import BasicParamsForm from '@/components/BasicParamsForm.vue'
import AnaModeSelector from '@/components/AnaModeSelector.vue'
import SnapshotManager from '@/components/SnapshotManager.vue'
// import DiffPathDisplay from './DiffPathDisplay.vue'
import Display from './Display.vue'
import ContextMenu from '@/components/panels/ContextMenu.vue'
import { nodeComponentMap } from '@/config/nodeComponentMap'
import { useMenuStore } from '@/stores/useMenuStore'
import { useExportGraph } from "@/composables/useExportGraph"
import { useGraphStateManager } from '@/composables/useGraphStateManager'
import { useAnalysisStore, type GraphSnapshot } from '@/stores/useAnalysisStore'
import '@/styles/editor_layout.scss'    // 导入样式

// -------- stores --------
const { exportGraph } = useExportGraph()
const analysisStore = useAnalysisStore()
const nodeStore = useNodeStore()
const edgeStore = useEdgeStore()
const menu = useMenuStore()
const ui = useUIStore()

// 使用状态管理器，解构所有方法
const {
  onSaveSnapshot,
  onLoadSnapshot,
  onDeleteSnapshot,
  onSaveLastRound,
  onLoadLastRound,
  onClearLastRound,
} = useGraphStateManager()

function onNodeClick({ node }) {
  nodeStore.setSelected(node.id)
  ui.openPropPanel()
}

// ------------------ 删除统一处理 ------------------
function deleteSelected() {
  // 删除节点
  ui.selectedNodeIds.forEach(id => nodeStore.removeNode(id))
  ui.selectedNodeIds = []

  // 删除边
  ui.selectedEdgeIds.forEach(id => edgeStore.removeEdges(id))
  ui.selectedEdgeIds = []
}

// 把删除行为暴露给 UIStore 的按钮一致性
ui.deleteSelected = deleteSelected

// 监听 Delete 键
function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Delete' || e.key === 'Backspace') {
    // 输入框内按 delete 不触发删除
    const tag = (e.target as HTMLElement).tagName.toLowerCase()
    if (tag === 'input' || tag === 'textarea') return

    deleteSelected()
  }
}

// 把监听挂在全局
onMounted(() => {
  document.addEventListener('keydown', onKeydown)
})
onUnmounted(() => {
  document.removeEventListener('keydown', onKeydown)
})

// -------- 默认边配置 --------
const defaultEdgeOptions = {
  type: 'smoothstep',
  markerEnd: { type: MarkerType.ArrowClosed, width: 20, height: 20, color: '#555' }
}

// -------- 节点类型映射 --------
const nodeTypeMap = Object.fromEntries(
  Object.entries(nodeComponentMap).map(([k, v]) => [k, v])
)

// -------- 节点变化事件 --------
function onNodesChange(changes: NodeChange[]) {
  changes.forEach(change => {
    switch (change.type) {
      case 'add': nodeStore.addNode(change.item); break
      case 'remove': 
        change.id && nodeStore.removeNode(change.id) // 自动删除节点及相关边
        break
      case 'position':
        const n = nodeStore.nodes.find(x => x.id === change.id)
        if (n && change.position) n.position = { ...change.position }
        break
      case 'select':
        if (change.selected) nodeStore.setSelected(change.id)
        break
    }
  })
}

// -------- 连接事件 --------
function onConnect(connection: Connection) {
  edgeStore.addEdge({
    id: `${connection.source}-${connection.sourceHandle}__${connection.target}-${connection.targetHandle}`,
    source: connection.source,
    target: connection.target,
    sourceHandle: connection.sourceHandle,
    targetHandle: connection.targetHandle,
    type: 'smoothstep',
    markerEnd: { type: MarkerType.ArrowClosed, width: 20, height: 20, color: '#555' }
  })
}

// -------- 拖拽新增节点 --------
const draggableNodes = Object.keys(nodeComponentMap)  // NodeLibrary 传给可拖拽节点列表

function onDrop(event: DragEvent) {
  const type = event.dataTransfer?.getData('node-type')
  if (!type) return

  const rect = (event.currentTarget as HTMLElement).getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top

  const id = `node-${Date.now()}`
  nodeStore.addNode({
    id,
    type,
    position: { x, y },
    data: {
      label: type,
      props: nodeStore.getDefaultProps(type)
    }
  })
}

// -------- 右键菜单事件 --------
function onRightClickNode({ event, node }: any) {
  event.preventDefault()
  event.stopPropagation()
  menu.showMenu(event.clientX, event.clientY, 'node', node.id)
}

function onRightClickEdge({ event, edge }: any) {
  event.preventDefault()
  event.stopPropagation()
  menu.showMenu(event.clientX, event.clientY, 'edge', edge.id)
}

function onRightClickPane(event: MouseEvent) {
  event.preventDefault()
  event.stopPropagation()
  menu.showMenu(event.clientX, event.clientY, 'canvas', '')
}


// -------- 点击空白处隐藏菜单 --------
function handleClickOutside() {
  menu.hideMenu()
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('contextmenu', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('contextmenu', handleClickOutside)
})

function onExportClick() {
    const json = exportGraph()
    console.log(JSON.stringify(json, null, 2))
}

function onRunAnalysis() {
    // 组件只负责处理 UI 事件，并调用业务逻辑模块
    ui.runAnalysis()
}

</script>

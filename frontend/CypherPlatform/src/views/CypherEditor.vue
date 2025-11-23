<template>
  <div class="layout">
    <!-- 左侧组件库 -->
    <aside class="sidebar">
      <!-- 分组算法基本参数 -->
       <div class="sidebar-top">
        <div class="param-header">
          <el-button
            type="primary"
            size="large"
            class="param-btn"
            @click="ui.setActive('params')"
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
          >
            🧩 分析模式
          </el-button>
        </div>
      </div>

      <div class="sidebar-top">
        <div class="param-header">
          <el-button
            type="success"
            size="large"
            class="param-btn"
            @click="ui.setActive('results')"
          >
            📊 结果展示
          </el-button>
          <p class="param-desc">查看差分路径与分析结果</p>
        </div>
      </div>

      <!-- 组件库 -->
      <div class="node-library-wrapper">
        <NodeLibrary />
      </div>
    </aside>

    <!-- 中间画布 -->
    <main class="canvas-area">
      <!-- 参数输入页面 -->
      <transition name="fade">
        <div v-if="activePanel === 'params'" class="param-overlay">
          <BasicParamsForm />
          <div class="param-actions">
            <el-button type="primary" @click="closeParams">保存并返回画布</el-button>
          </div>
        </div>
      </transition>

      <!-- 结果展示页面 -->
      <transition name="fade">
        <div v-if="activePanel === 'results'" class="param-overlay">
          <DiffPathDisplay />   <!-- ✅ 这里展示你写好的差分路径结果页面 -->
          <div class="param-actions">
            <el-button type="primary" @click="closeParams">返回画布</el-button>
          </div>
        </div>
      </transition>

      <!-- 分析模式覆盖面板 -->
      <transition name="fade">
        <div v-if="activePanel === 'mode'" class="param-overlay">
          <AnaModeSelector
            v-model:selectedMode="selectedMode"
          />
          <div class="param-actions">
            <el-button type="primary" @click="closeParams">返回画布</el-button>
          </div>
        </div>
      </transition>


      <!-- Vue Flow 画布 -->
      <VueFlow
        class="flow"
        :nodes="vfNodes"
        :edges="vfEdges"
        :node-types="nodeTypeMap"
        :default-edge-options="defaultEdgeOptions"
        v-model:selected-nodes="selectedNodeIds"
        @nodes-change="onNodesChange"
        @edges-change="onEdgesChange"
        @connect="onConnect"
      >
        <Background />   <!-- 背景网格 -->

        <!-- 初始引导提示层 -->
         <template v-if="vfNodes.length === 0 && activePanel === 'editor'">
          <div class="canvas-hint">
            <h3>欢迎来到带条件聚合类路线自动化分析平台</h3>
            <p>👉 从左侧拖入节点以构建分析路径</p>
            <p>⚙️ 点击 <b>分析模式</b> 选择聚合策略</p>
            <p>📊 点击 <b>结果展示</b> 查看差分路径与聚合结果</p>
          </div>
         </template>

        <!-- ✅ 自定义节点渲染 -->
          <template #node-default="{ id, data, positon }">
            <div class="node-wrapper vertical">
              <!-- 输入端：上方 -->
              <Handle
                type="target"
                :position="Position.Top"
                :id="id + '-in'"
                class="node-handle"
              />

              <!-- 节点主体 -->
              <div class="node-body">
                <component
                  v-if="data.type"
                  :is="resolveNodeComponent(data.type)"
                  :id="id"
                  :x="data.x ?? position.x"
                  :y="data.y ?? position.y"
                  v-bind="data.props"
                />
                <template v-else>
                  <img :src="data.icon" alt="" class="node-icon" />
                  <span class="node-label">{{ data.label }}</span>
                </template>
              </div>

              <!-- 输出端：下方 -->
              <Handle
                type="source"
                :position="Position.Bottom"
                :id="id + '-out'"
                class="node-handle"
              />
            </div>
          </template>
      </VueFlow>
    </main>

    <!-- 悬浮属性面板（右上角） -->
    <transition name="fade">
      <div
        v-if="selectedNode"
        class="floating-prop-panel"
      >
        <header class="floating-header">
          <h4>
            {{selectedNode.label || selectedNode.type }} 属性
          </h4>
          <button
            v-if="selectedNode"
            class="close-btn"
            @click="closeFloatingPanel"
          >
            ×
          </button>
        </header>

        <div class="floating-content">
          <!-- ✅ 若选中节点 -->
          <template v-if="selectedNode && panelComponent">
            <component
              :is="panelComponent"
              v-model="selectedNodeModel"
              :key="selectedNode.id"
            />
          </template>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
/**
 * 完整、单文件的 CypherEditor.vue（Pinia 驱动，自动面板注册，去深度 watch）
 *
 * 说明：
 *  - Store（useNodeStore）是你已经提供的 Pinia store（见你贴的代码）
 *  - nodeComponentMap、nodeRegistry 保持你原来的配置
 *  - panels 目录会被自动导入（import.meta.glob），按 nodeRegistry 配置决定面板组件名
 *
 * 你只需把该文件替换/覆盖原来的 Editor.vue 即可（确保路径与依赖正确）。
 */

import { ref, computed, watch, type Component, nextTick } from 'vue'
import NodeLibrary from '@/components/NodeLibrary.vue'
import BasicParamsForm from '@/components/BasicParamsForm.vue'
import AnaModeSelector from '@/components/AnaModeSelector.vue'
import { useNodeStore } from '@/stores/useNodeStore'
import { nodeRegistry } from '@/components/config/NodeRegistry'
import { nodeComponentMap } from '@/components/config/nodeComponentMap'
import type { NodeTypeMap } from '@/stores/useNodeStore'

import '@/styles/editor_layout.scss'    // 导入样式
import DiffPathDisplay from './DiffPathDisplay.vue'  // ← 你差分路径可视化的组件

import {
  VueFlow,
  Handle,
  Position,
  type Node as VfNode,
  type Edge as VfEdge,
  type Connection,
  type NodeChange,
  type EdgeChange,
  MarkerType
} from '@vue-flow/core'
import { Background } from '@vue-flow/background'

/* ---------- local UI state (非跨组件共享，仅 Editor 内部 UI) ---------- */
const activePanel = ref<'editor' | 'params' | 'results' | 'mode'>('editor')    // 控制中间画布显示哪个面板
const selectedMode = ref<'auto' | 'fixed' | 'constraint'>('auto')              // 当前分析模式

// 关闭参数面板（回到主画布）
const closeParams = () => (activePanel.value = 'editor')
// store
const nodeStore = useNodeStore()

// 默认边样式
const defaultEdgeOptions = {
  type: 'smoothstep', // 'straight' | 'step' | 'smoothstep' | 'default' (贝塞尔)
  markerEnd: {
    type: MarkerType.ArrowClosed, // 封闭箭头
    width: 10,
    height: 10,
    color: '#555',
  }
}

// nodeTypes 用于告诉 VueFlow 每种 type 应该渲染哪个组件
const nodeTypeMap = Object.fromEntries(
  Object.entries(nodeComponentMap).map(([key, comp]) => [key.toLowerCase(), comp])
)

/* --- store --- */
const { state, updateNodeProps, setSelected, resolveNodeComponent } = useNodeStore()

// 控制属性面板显隐
const showPropPanel = ref(false)

/* --- vue-flow 镜像数据 --- */
const vfNodes = ref<VfNode[]>([])
const vfEdges = ref<VfEdge[]>([])


/* watch 同步逻辑 */

// 当 store 中 nodes 变化时，同步到 VueFlow
watch(
  () => state.nodes,
  (nodes) => {
    vfNodes.value = nodes.map((n) => ({
      id: n.id,
      type: n.type,
      position: { x: n.position.x, y: n.position.y },
      data: { x: n.position.x, y: n.position.y, label: n.data.label, props: n.data.props },
    })) as VfNode[]
  },
  { immediate: true, deep: true }
)

// 当 store 中 edges 变化时，同步到 VueFlow
watch(
  () => state.edges,
  (edges) => {
    vfEdges.value = edges.map((e) => ({
      id: e.id,
      source: e.source,
      target: e.target,
      type: e.type ?? 'default',
      label: e.label,
    })) as VfEdge[]
  },
  { immediate: true, deep: true }
)



/* ---------- 事件: Vue Flow -> store ---------- */

// 处理节点变化事件
function onNodesChange(changes: NodeChange[]) {
  for (const change of changes) {
    switch (change.type) {
      case 'add': {
        const n = change.item
        vfNodes.value.push(n)
        state.nodes.push({
          id: n.id,
          type: n.type,
          position: n.position,
          data: n.data
        })
        break
      }
      case 'remove': {
        vfNodes.value = vfNodes.value.filter((v) => v.id !== change.id)
        state.nodes = state.nodes.filter((n) => n.id !== change.id)
        break
      }
      case 'position': {
        const n = vfNodes.value.find((v) => v.id === change.id)
        const s = state.nodes.find((x) => x.id === change.id)
        if (n && s && change.position) {
          n: n.position = { ...change.position }
          s.position.x = change.position.x
          s.position.y = change.position.y
        }
        break
      }
      case 'select': {
        if (change.selected) {
          // 如果选中同一个节点，也强制刷新属性面板
          if (state.selectedNodeId === change.id) {
            showPropPanel.value = false
            nextTick(() => (showPropPanel.value = true))
          } else {
            setSelected(change.id)
            showPropPanel.value = true
          }
        } else {
          // 取消选中节点时，仅关闭面板但不清空选中状态
          showPropPanel.value = false
        }
        break
      }
    }
  }
}

function onEdgesChange(changes: EdgeChange[]) {
  for (const change of changes) {
    switch (change.type) {
      case 'add': {
        const e = change.item
        vfEdges.value.push(e)
        state.edges.push({
          id: e.id,
          source: e.source,
          target: e.target,
          type: e.type ?? 'default',
          label: e.label
        })
        break
      }
      case 'remove': {
        vfEdges.value = vfEdges.value.filter((v) => v.id !== change.id)
        state.edges = state.edges.filter((e) => e.id !== change.id)
        break
      }
    }
  }
}

function closeFloatingPanel() {
  setSelected(null)
  selectedNodeIds.value = []   // 🔥 手动清空 Vue Flow 的选中状态
}



/* ---------- 新连接 ---------- */
function onConnect(connection: Connection) {
  // 自己生成唯一 id
  const id = `${connection.source}-${connection.target}`

  const newEdge: VfEdge = {
    id,
    source: connection.source,
    target: connection.target,
    type: 'smoothstep',
    markerEnd: {
      type: MarkerType.ArrowClosed,
      width: 10,
      height: 10,
      color: '#555'
    },
    label: '',
  }

  // 更新 Vue Flow 镜像
  vfEdges.value.push(newEdge)

  // 同步到 store.edges
  state.edges.push({
    id: newEdge.id,
    source: newEdge.source,
    target: newEdge.target,
    type: newEdge.type,
    label: newEdge.label,
    markerEnd: newEdge.markerEnd,
  })
}



/* ---------- 双向绑定：选中节点 ---------- */
const selectedNodeIds = computed({
  get: () => (state.selectedNodeId ? [state.selectedNodeId] : []),
  set: (arr: string[]) => setSelected(arr[0] ?? '')
})

/* ---------- 当前选中节点 ---------- */
const selectedNode = computed(() => {
  return state.nodes.find((n) => n.id === state.selectedNodeId) ?? null
})

/* ---------- 动态属性面板 ---------- */
// 自动导入 panels 文件夹下所有 Vue 组件
const modules = import.meta.glob('../components/panels/*.vue', { eager: true })

// 构建 panelMap，类型使用 Vue 的 Component 类型
const panelMap: Record<string, Component> = {}

for (const path in modules) {
  const name = path.split('/').pop()!.replace('.vue', '')
  panelMap[name] = (modules[path] as { default: Component }).default
}

// 计算当前节点对应的面板
const panelComponent = computed<Component | null>(() => {
  const node = selectedNode.value
  if (!node) return null

  const entry = nodeRegistry.find(r => r.type === node.type)
  const name = entry?.propertyPanel?.component
  if (!name) return null

  return panelMap[name] ?? null
})

/* ---------- v-model 代理 ---------- */
const selectedNodeModel = computed({
  // get: 当组件要读取 selectedNode 的值时执行
  get: (): NodeTypeMap[keyof NodeTypeMap] | null =>
    selectedNode.value ? { ...selectedNode.value.data.props } : null,
  // set: 当（比如 <input v-model="selectedNodeModel"）修改它时执行
  set: (v: NodeTypeMap[keyof NodeTypeMap] | null) => {
    if (!selectedNode.value || !v) return
    updateNodeProps(selectedNode.value.id, v)
  }
})

</script>


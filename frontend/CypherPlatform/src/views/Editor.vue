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
        <NodeLibrary :draggable-nodes="draggableNodes" />
      </div>
    </aside>

    <!-- 中间画布 -->
    <main class="canvas-area">
      <!-- 参数面板 -->
      <transition name="fade">
        <div v-if="ui.activePanel === 'params'" class="param-overlay">
          <BasicParamsForm />
          <el-button type="primary" @click="ui.setActive('editor')">保存并返回画布</el-button>
        </div>
      </transition>

      <!-- 结果面板 -->
      <transition name="fade">
        <div v-if="ui.activePanel === 'results'" class="param-overlay">
          <DiffPathDisplay />
          <el-button type="primary" @click="ui.setActive('editor')">返回画布</el-button>
        </div>
      </transition>

      <!-- 分析模式面板 -->
      <transition name="fade">
        <div v-if="ui.activePanel === 'mode'" class="param-overlay">
          <AnaModeSelector v-model:selectedMode="ui.selectedMode" />
          <el-button type="primary" @click="ui.setActive('editor')">返回画布</el-button>
        </div>
      </transition>

      <!-- VueFlow 画布 -->
      <VueFlow
        class="flow"
        :nodes="vfNodes"
        :edges="vfEdges"
        :node-types="nodeTypeMap"
        :default-edge-options="defaultEdgeOptions"
        v-model:selected-nodes="ui.selectedNodeIds"
        @nodes-change="onNodesChange"
        @edges-change="onEdgesChange"
        @connect="onConnect"
        @drop="onDrop"
        @dragover.prevent
        @node-click="onNodeClick"
      >
        <Background />

        <!-- 初始引导提示层 -->
         <template v-if="vfNodes.length === 0 && ui.activePanel === 'editor'">
          <div class="canvas-hint">
            <h3>欢迎来到带条件聚合类路线自动化分析平台</h3>
            <p>👉 从左侧拖入节点以构建分析路径</p>
            <p>⚙️ 点击 <b>分析模式</b> 选择聚合策略</p>
            <p>📊 点击 <b>结果展示</b> 查看差分路径与聚合结果</p>
          </div>
         </template>

        <!-- 自定义节点渲染 -->
        <template #node-default="{ id, data }">
          <div class="node-wrapper vertical">
            <Handle type="target" :position="Position.Top" :id="id+'-in'" class="node-handle" />
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
            <Handle type="source" :position="Position.Bottom" :id="id+'-out'" class="node-handle" />
          </div>
        </template>
      </VueFlow>
    </main>

    <!-- 属性面板（右上角） -->
    <transition name="fade">
      <div v-if="ui.selectedNode" class="floating-prop-panel">
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
import { computed } from 'vue'
import { VueFlow, Handle, Position, type NodeChange, type EdgeChange, type Connection, type Node as VfNode, type Edge as VfEdge, MarkerType } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { useNodeStore } from '@/stores/useNodeStore'
import { useUIStore } from '@/stores/useUIStore'
import NodeLibrary from '@/components/NodeLibrary.vue'
import BasicParamsForm from '@/components/BasicParamsForm.vue'
import AnaModeSelector from '@/components/AnaModeSelector.vue'
import DiffPathDisplay from './DiffPathDisplay.vue'
import { nodeComponentMap } from '@/components/config/nodeComponentMap'

import '@/styles/editor_layout.scss'    // 导入样式

// -------- stores --------
const nodeStore = useNodeStore()
const ui = useUIStore()

function onNodeClick({ node }) {
  nodeStore.setSelected(node.id)
}

// -------- 默认边配置 --------
const defaultEdgeOptions = {
  type: 'smoothstep',
  markerEnd: { type: MarkerType.ArrowClosed, width: 10, height: 10, color: '#555' }
}

// -------- 节点类型映射 --------
const nodeTypeMap = Object.fromEntries(
  Object.entries(nodeComponentMap).map(([k, v]) => [k.toLowerCase(), v])
)

// -------- VueFlow 镜像数据 --------
const vfNodes = computed(() => nodeStore.nodes.map(n => ({
  id: n.id,
  type: n.type,
  position: { ...n.position },
  data: { ...n.data }
})))

const vfEdges = computed(() => nodeStore.edges.map(e => ({ ...e })))

// -------- 节点变化事件 --------
function onNodesChange(changes: NodeChange[]) {
  changes.forEach(change => {
    switch (change.type) {
      case 'add': nodeStore.addNode(change.item); break
      case 'remove': nodeStore.nodes = nodeStore.nodes.filter(n => n.id !== change.id); break
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

// -------- 边变化事件 --------
function onEdgesChange(changes: EdgeChange[]) {
  changes.forEach(change => {
    switch (change.type) {
      case 'add': nodeStore.edges.push(change.item); break
      case 'remove': nodeStore.edges = nodeStore.edges.filter(e => e.id !== change.id); break
    }
  })
}

// -------- 连接事件 --------
function onConnect(connection: Connection) {
  const id = `${connection.source}-${connection.target}`
  const edge: VfEdge = { id, source: connection.source, target: connection.target, type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed, width: 10, height: 10, color: '#555' } }
  nodeStore.edges.push(edge)
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
</script>

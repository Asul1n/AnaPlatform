<template>
  <div class="plain-var-node">
    <div class="name-box">{{ name }}</div>

    <Handle
      :type="handleType"
      :position="handlePosition"
      :id="handleId"
      class="var-handle plain-var-handle"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Handle, Position } from '@vue-flow/core'

interface Props {
  id: string
  data: {
    props?: {
      name?:  string
      mode?:  'input' | 'output'
      bitwidth?: number // 仅用于记录位宽，不参与组件渲染宽度计算
    }
  }
}

const props = defineProps<Props>()

// --- 属性访问优化 ---

// 解构并为 props 提供默认值，使访问更简洁
const nodeProps = computed(() => props.data?.props ?? {})

const name = computed(() => nodeProps.value.name ?? 'Variable')
const mode = computed(() => (nodeProps.value.mode ?? 'output') as 'input' | 'output')

// --- Vue Flow Handle 逻辑 (Input Top / Output Bottom) ---

// 调整 Handle 位置：Input (target) 在 Top，Output (source) 在 Bottom
const handlePosition = computed(() => mode.value === 'input' ? Position.Top : Position.Bottom)

// Handle 的 type：输入为 target、输出为 source
const handleType = computed(() => mode.value === 'input' ? 'target' : 'source')

// 给 handle 分配不同 id，确保唯一性
const handleId = computed(() => (mode.value === 'input' ? `in-${props.id}` : `out-${props.id}`))

</script>

<style scoped>
/* 节点容器样式 (保持不变) */
.plain-var-node {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 36px;
  border: 2px solid #000;
  border-radius: 6px;
  background: #fff;
  font-family: "Times New Roman", serif; /* 还原为您最初的字体 */
  font-size: 16px;
  font-weight: bold;
  position: relative; /* 核心：启用 Handle 的绝对定位 */
}

.name-box {
  text-align: center;
  z-index: 1; 
}

/* --- Handle 外观样式 (还原为您最初的样式) --- */
.var-handle {
  width: 6px;
  height: 6px;
  background: #333;
  border-radius: 50%;
  
  /* 确保这个自定义样式块不包含任何 top/bottom/left/right 属性 */
  z-index: 10; 
}

/* 关键修复：使用 CSS 伪类 `:deep()` 强制 Handle 的定位属性 */
/* 我们不依赖 Vue Flow 的默认样式，而是手动定义 Top 和 Bottom 的绝对定位 */

/* 当 Handle 在顶部时 (Input mode) */
.plain-var-node :deep(.vue-flow__handle.top) {
  /* 强制绝对定位到顶部 */
  top: -4px !important; 
  left: 50% !important;
  transform: translateX(-50%) !important;
}

/* 当 Handle 在底部时 (Output mode) */
.plain-var-node :deep(.vue-flow__handle.bottom) {
  /* 强制绝对定位到底部 */
  bottom: -4px !important; 
  left: 50% !important;
  transform: translateX(-50%) !important;
}

/* 增加 !important 确保这些定位属性具有最高的优先级 */
/* -4px 是根据 Handle 大小 (6px) 调整的，使其突出节点边缘 */
</style>
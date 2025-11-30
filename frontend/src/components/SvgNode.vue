<script setup lang="ts">
import { Handle, Position, type NodeProps } from '@vue-flow/core'
import { computed } from 'vue'

// ✅ 让 VueFlow 知道这是个合法节点组件
const props = defineProps<NodeProps<{ icon?: string }>>()

// ✅ 自动加载 /src/assets/icons 目录下的所有 svg
const modules = import.meta.glob('@/assets/icons/*.svg', { eager: true, as: 'raw' })

// ✅ 根据 data.icon 匹配对应 svg
const svgContent = computed(() => {
  const iconName = props.data?.icon
  if (!iconName) return ''
  const match = Object.entries(modules).find(([path]) =>
    path.endsWith('/' + iconName)
  )
  if (!match) {
    console.warn('SVG not found for:', iconName)
    return `<svg width="32" height="32"><rect width="32" height="32" fill="red"/></svg>`
  }
  return match[1] as string
})
</script>

<template>
  <div class="svg-node">
    <div class="icon" v-html="svgContent"></div>

    <!-- 输入输出端口 -->
    <Handle type="target" :position="Position.Top" />
    <Handle type="source" :position="Position.Bottom" />
  </div>
</template>

<style scoped>
.svg-node {
  width: 64px;
  height: 64px;
  background: #fff;
  border: 2px solid #ccc;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: 0.2s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.15);
}
.svg-node:hover {
  border-color: #0078ff;
  transform: scale(1.05);
}
.icon svg {
  width: 36px;
  height: 36px;
  fill: currentColor;
}
</style>

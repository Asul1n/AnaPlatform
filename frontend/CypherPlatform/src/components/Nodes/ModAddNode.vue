<template>
  <!-- g 是 SVG 的分组容器 -->
  <g
    @click="handleClick"
    @mouseenter="hover = true"
    @mouseleave="hover = false"
    style="cursor: pointer;"
  >
    <!-- 正方形框 -->
    <rect
      :x="x - size / 2"
      :y="y - size / 2"
      :width="size"
      :height="size"
      rx="4"
      ry="4"
      :fill="hover ? '#FFF176' : selected ? '#FFD54F' : '#FFF9C4'"
      stroke="#F57F17"
      stroke-width="2"
    />

    <!-- 十字号 -->
    <line
      :x1="x - crossSize / 2"
      :y1="y"
      :x2="x + crossSize / 2"
      :y2="y"
      stroke="#F57F17"
      stroke-width="2"
      stroke-linecap="round"
    />
    <line
      :x1="x"
      :y1="y - crossSize / 2"
      :x2="x"
      :y2="y + crossSize / 2"
      stroke="#F57F17"
      stroke-width="2"
      stroke-linecap="round"
    />
  </g>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useNodeStore } from '@/stores/useNodeStore'

// ✅ 接收节点位置和参数
const props = defineProps({
  id: { type: String, required: true },
  x: { type: Number, required: true },
  y: { type: Number, required: true },
  size: { type: Number, default: 30 },
  crossSize: { type: Number, default: 14 },
})

// ✅ 获取全局 store
const { state, setSelected } = useNodeStore()

// ✅ 本地 hover 状态
const hover = ref(false)

// ✅ 判断该节点是否被选中
const selected = computed(() => state.selectedNodeId === props.id)

// ✅ 点击事件（更新全局状态）
function handleClick() {
  setSelected(props.id)
}
</script>

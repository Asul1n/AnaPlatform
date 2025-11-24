<template>
  <div class="xor-node-wrapper">
    <!-- 左上角输入 -->
    <Handle
      type="target"
      :position="Position.Left"
      id="in-left"
      class="xor-handle"
      :style="{ top: '20%', left: '0%' }"
    />
    <!-- 右上角输入 -->
    <Handle
      type="target"
      :position="Position.Right"
      id="in-right"
      class="xor-handle"
      :style="{ top: '20%', right: '0%' }"
    />

    <!-- XOR 节点主体 -->
    <div class="xor-node">
      <svg :width="size" :height="size" viewBox="0 0 100 100">
        <!-- 外圆 -->
        <circle
          cx="50"
          cy="50"
          r="45"
          fill="none"
          stroke="#000"
          stroke-width="3"
        />
        <!-- 内圆 -->
        <circle
          cx="50"
          cy="50"
          r="35"
          fill="none"
          stroke="#000"
          stroke-width="2"
        />
        <!-- 中心十字 ⊕ -->
        <line
          x1="35"
          y1="50"
          x2="65"
          y2="50"
          stroke="#000"
          stroke-width="3"
          stroke-linecap="round"
        />
        <line
          x1="50"
          y1="35"
          x2="50"
          y2="65"
          stroke="#000"
          stroke-width="3"
          stroke-linecap="round"
        />
      </svg>
    </div>

    <!-- 下方输出 -->
    <Handle
      type="source"
      :position="Position.Bottom"
      id="out-bottom"
      class="xor-handle"
      :style="{ bottom: '0%', left: '50%' }"
    />
  </div>
</template>

<script setup lang="ts">
import { Handle, Position } from '@vue-flow/core'

interface Props {
  id: string
  data: {
    label?: string
    props?: Record<string, any>
  }
  size?: number
}

const props = defineProps<Props>()
const { size = 80 } = props
</script>

<style scoped>
.xor-node-wrapper {
  width: 80px;
  height: 80px;
  position: relative;
}

/* XOR 节点主体 */
.xor-node {
  width: 80px;
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

/* 标签 */
.label {
  position: absolute;
  bottom: -18px;
  font-size: 12px;
  font-family: "Times New Roman", serif;
  text-align: center;
  width: 100%;
}

/* Handle 样式，小圆点，低干扰 */
.xor-handle {
  width: 6px;
  height: 6px;
  background-color: #333;
  border-radius: 50%;
  position: absolute;
}
</style>

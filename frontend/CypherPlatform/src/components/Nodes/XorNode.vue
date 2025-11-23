<template>
  <g>
    <circle
      :cx="props.node.position.x"
      :cy="props.node.position.y"
      :r="15"
      fill="#F3E5F5"
      stroke="#6A1B9A"
      stroke-width="2"
    />

    <line
      :x1="props.node.position.x - 5"
      :y1="props.node.position.y"
      :x2="props.node.position.x + 5"
      :y2="props.node.position.y"
      stroke="#6A1B9A"
      stroke-width="2"
    />

    <line
      :x1="props.node.position.x"
      :y1="props.node.position.y - 5"
      :x2="props.node.position.x"
      :y2="props.node.position.y + 5"
      stroke="#6A1B9A"
      stroke-width="2"
    />

    <text
      :x="props.node.position.x + 25"
      :y="props.node.position.y + 4"
      font-size="12"
      fill="#6A1B9A"
      font-family="monospace"
    >
      Circle
    </text>
  </g>
</template>

<script setup lang="ts">
import type { NodeProps } from '@vue-flow/core'

// 💡 关键！接收 VueFlow 自动注入的 props
const props = defineProps<NodeProps>()
</script>

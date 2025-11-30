<template>
  <div class="xor-node">
    <!-- 论文风格 XOR（⊕） -->
    <svg width="26" height="26" viewBox="0 0 26 26">
      <!-- 外圈 -->
      <circle
        cx="13"
        cy="13"
        r="11.5"
        stroke="black"
        stroke-width="1.8"
        fill="white"
      />

      <!-- 十字（论文风格，紧凑） -->
      <line x1="6" y1="13" x2="20" y2="13" stroke="black" stroke-width="1.8" />
      <line x1="13" y1="6" x2="13" y2="20" stroke="black" stroke-width="1.8" />
    </svg>

    <!-- 左输入 -->
    <Handle
      type="target"
      :position="Position.Left"
      id="in-left"
      class="handle"
    />

    <!-- 右输入 -->
    <Handle
      type="target"
      :position="Position.Right"
      id="in-right"
      class="handle"
    />

    <!-- 下输出 -->
    <Handle
      type="source"
      :position="Position.Bottom"
      id="out-bottom"
      class="handle"
    />
  </div>
</template>

<script setup lang="ts">
import { Handle, Position } from '@vue-flow/core'
</script>

<style scoped>
.xor-node {
  width: 26px;
  height: 26px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 和你最开始统一的端口样式 */
.handle {
  width: 8px !important;
  height: 8px !important;
  background: #333 !important;
  border-radius: 50% !important;
  position: absolute;
}
</style>

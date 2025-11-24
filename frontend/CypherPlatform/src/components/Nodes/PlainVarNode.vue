<template>
  <div class="plain-var-node">
    <div class="name-box">{{ name }}</div>

    <!-- 输出连线：放到底部居中 -->
    <Handle
      type="source"
      :position="Position.Bottom"
      id="out"
      class="var-handle bottom-handle"
    />
  </div>
</template>

<script setup lang="ts">
import { Handle, Position } from '@vue-flow/core'

interface Props {
  id: string
  data: {
    props?: {
      name?: string
      width?: number
    }
  }
}

const props = defineProps<Props>()
const name = props.data.props?.name ?? 'X?'
</script>

<style scoped>
.plain-var-node {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 36px;
  border: 2px solid #000;
  border-radius: 6px;
  background: #fff;
  font-family: "Times New Roman", serif;
  font-size: 16px;
  font-weight: bold;
  position: relative; /* ← 重点：让 Handle 定位基准 */
}

.name-box {
  text-align: center;
}

.var-handle {
  width: 6px;
  height: 6px;
  background: #333;
  border-radius: 50%;
  position: absolute;
}

/* 底部正中 */
.bottom-handle {
  bottom: -6px;                 /* 垂直贴在下方 */
  left: 50%;
  transform: translateX(-50%);
}
</style>

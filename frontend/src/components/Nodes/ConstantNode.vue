<template>
  <div class="const-node">
    <div class="name-box">{{ value }}</div>

    <!-- 输出连线：底部中心 -->
    <Handle
      type="source"
      :position="Position.Bottom"
      id="out"
      class="var-handle bottom-handle"
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
      value?: string | number   // 常量节点使用 value 字段
      bitwidth?: number         // 可选：支持多少位常量
    }
  }
}

const props = defineProps<Props>()

// 常量的显示值
const value = computed(() => props.data.props?.value ?? 'C')
</script>

<style scoped>
.const-node {
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
  position: relative; /* Handle 定位基准 */
}

.name-box {
  text-align: center;
}

/* Handle 样式保持一致 */
.var-handle {
  width: 6px;
  height: 6px;
  background: #333;
  border-radius: 50%;
  position: absolute;
}

/* 底部正中输出 */
.bottom-handle {
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
}
</style>

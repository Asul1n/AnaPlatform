<template>
  <div class="plain-var-node">
    <div class="name-box">{{ name }}</div>

    <Handle
      :type="handleType"
      :position="handlePosition"
      :id="handleId"
      class="var-handle"
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
      mode?:  'input' | 'output'   // ← 新增字段，默认 output
      width?: number
    }
  }
}

const props = defineProps<Props>()

const name = computed(() => props.data.props?.name ?? '')
const mode = computed(() => (props.data?.props?.mode ?? 'output') as 'input' | 'output')

// Handle 的 position（使用 vue-flow 的 Position 枚举）
const handlePosition = computed(() => mode.value === 'input' ? Position.Bottom : Position.Top)

// Handle 的 type：输入为 target、输出为 source
const handleType = computed(() => mode.value === 'input' ? 'target' : 'source')

// 给 handle 分配不同 id，避免同时存在多个相同 id 的 handle 导致的问题
const handleId = computed(() => (mode.value === 'input' ? `in-${props.id}` : `out-${props.id}`))

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
  position: relative;
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

/* 输出模式：在线上方 */
.top {
  top: -6px;
  left: 50%;
  transform: translateX(-50%);
}

/* 输入模式：在线下方 */
.bottom {
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
}
</style>

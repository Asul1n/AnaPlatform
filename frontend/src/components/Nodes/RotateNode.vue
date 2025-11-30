<template>
  <div class="rotate-node-wrapper">
    <!-- 输入 Handle -->
    <Handle
      type="target"
      :position="Position.Top"
      id="in-top"
      class="rotate-handle"
    />

    <!-- 节点主体 -->
    <div class="rotate-node">
      <div class="arrow-box">{{ arrowString }}</div>
    </div>

    <!-- 输出 Handle -->
    <Handle
      type="source"
      :position="Position.Bottom"
      id="out-bottom"
      class="rotate-handle"
    />
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import { Handle, Position } from '@vue-flow/core'
import { useNodeStore } from '@/stores/useNodeStore'

interface Props {
  id: string
  data: {
    label?: string
    props?: {
      direction?: 'left' | 'right'
      offset?: number
      bitwidth?: number
    }
  }
}

const props = defineProps<Props>()
const nodeStore = useNodeStore()

// 本地响应式 props
const localProps = reactive({
  direction: props.data.props?.direction || 'left',
  offset: props.data.props?.offset || 1,
  bitwidth: props.data.props?.bitwidth || 8
})

// 箭头字符串
const arrowString = computed(() => {
  const base = localProps.direction === 'left' ? '<<<' : '>>>'
  return `${base} ${localProps.offset}`
})

// 将本地修改同步到 store
watch(localProps, (v) => {
  nodeStore.updateNodeProps(props.id, v)
}, { deep: true })

// 外部 props 改变同步到本地
watch(() => props.data.props, (v) => {
  if (v) Object.assign(localProps, v)
}, { deep: true })
</script>

<style scoped>
.rotate-node-wrapper {
  width: 80px;
  height: 50px;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 节点主体：矩形方框 */
.rotate-node {
  width: 80px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 箭头显示矩形 */
.arrow-box {
  width: 100%;
  height: 100%;
  border: 2px solid #000;
  border-radius: 6px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: "Times New Roman", serif;
  font-weight: bold;
  font-size: 18px;
  background-color: #fff;
  text-align: center;
}

/* Handle 样式（低干扰小圆点） */
.rotate-handle {
  width: 6px;
  height: 6px;
  background-color: #333;
  border-radius: 50%;
  position: absolute;
}
</style>

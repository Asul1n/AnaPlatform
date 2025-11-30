<template>
  <div class="add-node-wrapper">
    <!-- 输入 Handle -->
    <Handle
      type="target"
      :position="Position.Left"
      id="in-left"
      class="add-handle"
    />
    <Handle
      type="target"
      :position="Position.Right"
      id="in-right"
      class="add-handle"
    />

    <!-- 节点主体 -->
    <div class="add-node">
      <div class="plus-box">+</div>
    </div>

    <!-- 输出 Handle -->
    <Handle
      type="source"
      :position="Position.Bottom"
      id="out-bottom"
      class="add-handle"
    />
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import { Handle, Position } from '@vue-flow/core'
import { useNodeStore } from '@/stores/useNodeStore'

interface Props {
  id: string
  data: {
    label?: string
    props?: {
      name?: string
    }
  }
}

const props = defineProps<Props>()
const nodeStore = useNodeStore()

// 本地响应式 props
const localProps = reactive({
  name: props.data.props?.name || ''
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
.add-node-wrapper {
  width: 40px;
  height: 40px;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 缩小节点主体 */
.add-node {
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 更紧凑的加号框 */
.plus-box {
  width: 100%;
  height: 100%;
  border: 2px solid #000;
  border-radius: 4px;

  display: flex;
  justify-content: center;
  align-items: center;

  font-family: "Times New Roman", serif;
  font-weight: bold;
  font-size: 32px;         /* 加号变大 */
  line-height: 1;          /* 减少上下间隙 */
  background-color: #fff;
  text-align: center;
}

/* Handle 小圆点仍然保持小巧 */
.add-handle {
  width: 6px;
  height: 6px;
  background-color: #333;
  border-radius: 50%;
  position: absolute;
}

</style>

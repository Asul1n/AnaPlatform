<template>
  <div class="key-var-node">
    <div class="name-box">{{ name }}</div>

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
      name?: string
      bitwidth?: number
    }
  }
}

const props = defineProps<Props>()
const name = computed(() => props.data.props?.name ?? '')

</script>

<style scoped>
.key-var-node {
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
  position: relative; /* Handle 定位参考 */
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
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
}
</style>

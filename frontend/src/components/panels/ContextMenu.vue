<template>
  <div 
    v-if="visible" 
    class="context-menu simple"
    :style="{ top: y + 'px', left: x + 'px' }"
    @click.stop
  >
    <el-button 
      type="danger" 
      size="small" 
      @click="onDelete"
      :icon="Delete"
      class="menu-btn"
    >
      删除
    </el-button>=
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import { Delete } from '@element-plus/icons-vue'

const props = defineProps<{
  visible: boolean
  x: number
  y: number
}>()

const emit = defineEmits<{
  (e: 'delete'): void
}>()

function onDelete() {
  emit('delete')
}
</script>

<style scoped>
.context-menu.simple {
  position: fixed;
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 9999;
  padding: 8px;
}

.menu-btn {
  width: 100%;
  justify-content: flex-start;
}
</style>
<template>
  <div 
    v-if="menu.visible" 
    class="context-menu simple"
    :style="{ top: menu.position.y + 'px', left: menu.position.x + 'px' }"
    @click.stop
  >
    <el-button
      v-if="menu.target?.type === 'node' || menu.target?.type === 'edge'"
      type="danger" 
      size="small" 
      @click="menu.deleteTarget" 
      :icon="Delete"
      class="menu-btn"
    >
      删除 {{ menu.target?.type === 'node' ? '节点' : '边' }}
    </el-button>

    <el-button
      v-if="menu.target?.type === 'canvas'"
      type="primary" 
      size="small" 
      @click="menu.newCanvas"
      :icon="DocumentAdd"
      class="menu-btn"
    >
      ➕ 新建画布
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { Delete, DocumentAdd } from '@element-plus/icons-vue'
import { useMenuStore } from '@/stores/useMenuStore'
import { watch } from 'vue';

// 【修改点 1】: 直接从 Pinia Store 中获取状态和方法
const menu = useMenuStore()

// 【移除】: 移除对 props 和 emits 的依赖，直接通过 store 管理状态和操作
/*
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
*/

// 【可选增强】: 监听 visible 变化，在隐藏时重置目标，虽然 useMenuStore 已经做了，但作为安全措施
watch(
  () => menu.visible,
  (newVisible) => {
    if (!newVisible) {
      // 可以在这里执行一些额外的清理，但主要逻辑已移至 store
    }
  }
);
</script>

<style scoped>
/* 保持样式不变 */
.context-menu.simple {
  position: fixed;
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  /* 【重要】: 使用 store 提供的 position */
  top: v-bind('menu.position.y + "px"'); 
  left: v-bind('menu.position.x + "px"');
  z-index: 2147483647;
  padding: 8px;
  /* 确保菜单不会被意外拉伸 */
  min-width: 100px;
}

.menu-btn {
  width: 100%;
  justify-content: flex-start;
  margin: 0; /* 确保按钮间没有多余的 margin */
}
</style>
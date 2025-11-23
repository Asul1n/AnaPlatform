<template>
  <div class="node rotate-node">
    🔄 Rotate Node
  </div>
</template>

<script setup lang="ts">
// 这里可以定义组件逻辑，比如 props
defineProps<{
  direction?: string
  shift?: number
  width?: number
}>()
</script>

<style scoped>
.node {
  padding: 8px;
  border-radius: 8px;
  background-color: #eef;
  text-align: center;
}
</style>

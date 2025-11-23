<!-- PlainVar.vue -->
<template>
  <div class="node-wrapper">
    <div class="node-box">{{ name }}</div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, watch } from 'vue'

const props = defineProps<{
  name: string  
}>()

</script>

<style scoped>
.node-wrapper {
  display: inline-block;
}

.node-box {
  border: 1px solid black; /* 黑色边框 */
  padding: 8px 12px;
  border-radius: 4px;
  user-select: none;
  background-color: #fff;
}
</style>

<!-- AutoModePanel.vue -->
<template>
  <el-card shadow="hover" class="rounded-xl">
    <template #header>自动机多路线参数</template>
    <p class="text-gray-600 text-sm">
      此模式无需额外参数，将对算法进行全局扫描，生成并评估多条候选路线。
    </p>
  </el-card>
</template>

<script setup lang="ts">
defineProps<{ modelValue: Record<string, unknown> }>()
defineEmits(['update:modelValue'])
</script>

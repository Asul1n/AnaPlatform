<template>
  <g>
    <rect :x="x - 20" :y="y - 15" width="40" height="30" rx="4"
          fill="#E8EAF6" stroke="#283593" stroke-width="2" />
    <text :x="x - 7" :y="y + 5" font-size="16" fill="#283593">S</text>
  </g>
</template>

<script setup lang="ts">
defineProps<{ x: number; y: number }>()
</script>

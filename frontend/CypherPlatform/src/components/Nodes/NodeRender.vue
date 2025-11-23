<!-- src/components/Nodes/NodeRenderer.vue -->
<template>
  <div class="node-canvas">
    <component
      v-for="node in state.nodes"
      :key="node.id"
      :is="nodeComponentMap[node.type]"
      v-bind="node"
    />
  </div>
</template>

<script setup lang="ts">
import { useNodeStore } from '@/stores/useNodeStore'
import { nodeComponentMap } from '../config/nodeComponentMap';

const { state } = useNodeStore()
</script>

<style scoped>
.node-canvas {
  width: 100%;
  height: 100%;
  background: #fff;
  position: relative;
}
</style>

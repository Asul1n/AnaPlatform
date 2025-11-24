<template>
  <el-config-provider>
    <editor />
  </el-config-provider>
</template>

<script setup lang="ts">
  // import TestSBoxPanel from './components/panels/TestSBoxPanel.vue';
  import Editor from './views/Editor.vue';
</script>

<style>
html,
body,
#app {
  height: 100%;
  margin: 0;
  padding: 0;
}
</style>

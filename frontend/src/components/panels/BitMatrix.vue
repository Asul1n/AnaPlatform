<template>
  <div class="bit-matrix">
    <div v-for="(row, i) in size" :key="i" class="bit-row">
      <div
        v-for="(col, j) in size"
        :key="j"
        class="bit-cell"
        :class="{ active: modelValue[i][j] === 1 }"
        @click="toggleBit(i, j)"
      ></div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { defineProps, defineEmits, type PropType } from "vue"

const props = defineProps({
  modelValue: { type: Array as PropType<number[][]>, required: true },
  size: { type: Number, default: 16 },
})

const emit = defineEmits(["update:modelValue"])

const toggleBit = (i: number, j: number) => {
  const newMatrix = props.modelValue.map((r, ri) =>
    r.map((v, cj) => (ri === i && cj === j ? (v ? 0 : 1) : v))
  )
  emit("update:modelValue", newMatrix)
}
</script>

<style scoped>
.bit-matrix {
  display: grid;
  grid-template-rows: repeat(auto, 1fr);
  gap: 2px;
  user-select: none;
}
.bit-row {
  display: grid;
  grid-template-columns: repeat(auto, 1fr);
  gap: 2px;
}
.bit-cell {
  width: 16px;
  height: 16px;
  background: #e5e7eb;
  border-radius: 2px;
  cursor: pointer;
  transition: 0.2s;
}
.bit-cell.active {
  background: #409eff;
}
</style>

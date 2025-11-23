<template>
  <div class="property-panel">
    <h3>循环移位</h3>
    <el-form :model="localProps" label-width="100px">
      <el-form-item label="方向">
        <el-select v-model="localProps.direction">
          <el-option label="左移" value="left" />
          <el-option label="右移" value="right" />
        </el-select>
      </el-form-item>

      <el-form-item label="偏移量">
        <el-input-number
          v-model="localProps.shift"
          :min="0"
          :max="(localProps.width ?? 32)"
        />
      </el-form-item>

      <el-form-item label="位宽">
        <el-input-number
          v-model="localProps.width"
          :min="1"
          :max="256"
        />
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import { ElForm, ElFormItem, ElSelect, ElOption, ElInputNumber } from 'element-plus'
import type { ShiftProps } from './type';


const props = defineProps<{ modelValue: ShiftProps }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: ShiftProps): void }>()

const localProps = reactive<ShiftProps>({
  direction: props.modelValue?.direction ?? 'left',
  shift: props.modelValue?.shift ?? 1,
  width: props.modelValue?.width ?? 8,
})

// 双向绑定监听
watch(localProps, (v) => emit('update:modelValue', JSON.parse(JSON.stringify(v))), { deep: true })
watch(() => props.modelValue, (v) => Object.assign(localProps, v || {}), { deep: true })
</script>

<style scoped>
.property-panel {
  padding: 12px;
}
</style>

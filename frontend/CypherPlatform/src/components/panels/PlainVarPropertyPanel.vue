<template>
  <div class="property-panel">
    <h3>明文输入</h3>
    <el-form :model="localProps" label-width="100px">
      <el-form-item label="变量名">
        <el-input v-model="localProps.name" placeholder="例如 X1" />
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
import { ElForm, ElFormItem, ElInput, ElInputNumber } from 'element-plus'
import type { PlainVarProps } from './type'


const props = defineProps<{ modelValue: PlainVarProps }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: PlainVarProps): void }>()

const localProps = reactive<PlainVarProps>({
  name: props.modelValue?.name ?? 'X1',
  width: props.modelValue?.width ?? 8,
})

// ✅ 双向绑定同步
watch(localProps, (v) => emit('update:modelValue', JSON.parse(JSON.stringify(v))), { deep: true })
watch(() => props.modelValue, (v) => Object.assign(localProps, v || {}), { deep: true })
</script>

<style scoped>
.property-panel {
  padding: 12px;
}
</style>

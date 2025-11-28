<template>
  <div class="property-panel">
    <h3>密钥输入</h3>
    <el-form :model="localProps" label-width="100px">
      <el-form-item label="密钥名">
        <el-input v-model="localProps.name" placeholder="例如 K1" />
      </el-form-item>

      <el-form-item label="位宽">
        <el-input-number
          v-model="localProps.bitwidth"
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
import type { KeyVarProps } from './type';

const props = defineProps<{ modelValue: KeyVarProps }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: KeyVarProps): void }>()

const localProps = reactive<KeyVarProps>({
  name: props.modelValue?.name ?? 'K1',
  bitwidth: props.modelValue?.bitwidth ?? 8,
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

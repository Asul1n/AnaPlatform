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

      <!-- ⭐ 新增：输入 / 输出选择 -->
      <el-form-item label="方向">
        <el-select v-model="localProps.mode">
          <el-option label="输入（Handle 在下面）" value="input" />
          <el-option label="输出（Handle 在上面）" value="output" />
        </el-select>
      </el-form-item>

    </el-form>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import { ElForm, ElFormItem, ElInput, ElInputNumber, ElSelect, ElOption } from 'element-plus'
import type { PlainVarProps } from './type'

const props = defineProps<{ modelValue: PlainVarProps }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: PlainVarProps): void }>()

const localProps = reactive<PlainVarProps>({
  name:  props.modelValue?.name ?? 'X1',
  width: props.modelValue?.width ?? 8,
  mode:  props.modelValue?.mode ?? 'output',    // ⭐ 默认是 output
})

// 同步回外层
watch(localProps, (v) => {
  emit('update:modelValue', JSON.parse(JSON.stringify(v)))
}, { deep: true })

// 外层变 → 内层同步
watch(() => props.modelValue, (v) => {
  Object.assign(localProps, v || {})
}, { deep: true })
</script>

<style scoped>
.property-panel {
  padding: 12px;
}
</style>

<template>
  <div class="property-panel">
    <h3>常量设置</h3>
    <el-form :model="localProps" label-width="100px">
      
      <el-form-item label="常量名">
        <el-input v-model="localProps.name" placeholder="例如 C1" />
      </el-form-item>

      <el-form-item label="常量值">
        <el-input v-model="localProps.value" placeholder="例如 0xFF" />
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

// --- 类型定义 (假设你需要一个单独的 type.ts 文件来定义这些类型) ---
export interface ConstVarProps {
  name: string
  value: string // 常量值，通常用字符串表示 (如 '0xFF', '100', '0b1010')
  bitwidth: number
}
// --------------------------------------------------------------------

const props = defineProps<{ modelValue: ConstVarProps }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: ConstVarProps): void }>()

// 初始化本地状态
const localProps = reactive<ConstVarProps>({
  name: props.modelValue?.name ?? 'C1',
  value: props.modelValue?.value ?? '0x00',
  bitwidth: props.modelValue?.bitwidth ?? 8,
})

// ✅ Watcher 1: 监听本地状态变化，同步到父组件
watch(localProps, (v) => {
  // 使用结构化克隆或深拷贝确保传递的是新对象
  emit('update:modelValue', JSON.parse(JSON.stringify(v))) 
}, { deep: true })

// ✅ Watcher 2: 监听父组件 modelValue 变化，同步到本地状态
// 解决父组件可能动态更新数据的问题
watch(() => props.modelValue, (v) => {
    // 使用 Object.assign 安全地合并属性
    Object.assign(localProps, v || { name: '', value: '', bitwidth: 8 }) 
}, { deep: true })
</script>

<style scoped>
.property-panel {
  padding: 12px;
}
</style>
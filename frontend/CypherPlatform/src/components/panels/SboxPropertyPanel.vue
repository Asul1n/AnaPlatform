<template>
  <div class="property-panel">
    <div class="header">
      <h3>SBox 配置</h3>
      <div class="ops">
        <el-button size="small" @click="randomize">随机</el-button>
        <el-button size="small" @click="resetTable">重置</el-button>
        <el-button size="small" @click="exportJson">导出</el-button>
        <el-upload
          :show-file-list="false"
          :before-upload="importBeforeUpload"
        >
          <el-button size="small">导入</el-button>
        </el-upload>
      </div>
    </div>

    <el-form :model="localProps" label-width="100px" class="form-top">
      <el-form-item label="位宽 (bit)">
        <el-select v-model="localProps.sboxBit">
          <el-option label="4 bit" :value="4" />
          <el-option label="8 bit" :value="8" />
        </el-select>
      </el-form-item>

      <el-form-item label="SBox ID">
        <el-input-number v-model="localProps.sboxId" :min="1" :max="999" />
      </el-form-item>
    </el-form>

    <div class="sbox-wrapper">
      <div
        class="sbox-grid"
        :style="{ gridTemplateColumns: `repeat(${gridSize}, 1fr)`, gridAutoRows: cellSize + 'px' }"
      >
        <div
          v-for="(val, idx) in localProps.sboxTable"
          :key="idx"
          class="sbox-cell"
        >
          <input
            v-model.number="localProps.sboxTable[idx]"
            :min="0"
            :max="maxVal"
            class="cell-input"
          />
          <div class="idx">{{ idx }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import { ElButton, ElForm, ElFormItem, ElSelect, ElOption, ElInputNumber, ElUpload } from 'element-plus'
import type { SBoxProps } from './type'

const props = defineProps<{ modelValue: SBoxProps }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: SBoxProps): void }>()

const localProps = reactive({
  sboxId: props.modelValue?.sboxId ?? 1,
  sboxBit: props.modelValue?.sboxBit ?? 4,
  sboxTable: Array.isArray(props.modelValue?.sboxTable) ? props.modelValue!.sboxTable.slice() : Array.from({ length: 16 }, (_, i) => i)
} as SBoxProps)

// 当 sboxBit 改变，自动调整表长度（保留旧值）
watch(() => localProps.sboxBit, (bit) => {
  const newLen = 1 << bit
  if (localProps.sboxTable.length !== newLen) {
    const old = localProps.sboxTable.slice()
    localProps.sboxTable = Array.from({ length: newLen }, (_, i) => (i < old.length ? old[i]! : i))
  }
}, { immediate: true })

// 双向绑定回父
watch(localProps, (v) => emit('update:modelValue', JSON.parse(JSON.stringify(v))), { deep: true })

const gridSize = computed(() => Math.ceil(Math.sqrt(localProps.sboxTable.length)))
const maxVal = computed(() => (1 << localProps.sboxBit) - 1)

// cellSize 根据表大小自动调整（保证可视化）
const cellSize = computed(() => {
  const n = gridSize.value
  if (n <= 4) return 48
  if (n <= 8) return 40
  if (n <= 16) return 28
  return 18
})

function randomize(): void {
  const arr: number[] = localProps.sboxTable.map((_, i) => i)
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    const tmp = arr[i]!
    arr[i] = arr[j]!
    arr[j] = tmp
  }
  localProps.sboxTable = arr
}


function resetTable() {
  localProps.sboxTable = localProps.sboxTable.map((_, i) => i)
}

function exportJson() {
  const data = JSON.stringify({
    sboxId: localProps.sboxId,
    sboxBit: localProps.sboxBit,
    sboxTable: localProps.sboxTable
  }, null, 2)
  const blob = new Blob([data], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `sbox_${localProps.sboxId}.json`
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
}

function importBeforeUpload(file: File) {
  const reader = new FileReader()
  reader.onload = () => {
    try {
      const parsed = JSON.parse(String(reader.result))
      if (Array.isArray(parsed.sboxTable) && typeof parsed.sboxBit === 'number') {
        localProps.sboxBit = parsed.sboxBit
        localProps.sboxId = parsed.sboxId ?? localProps.sboxId
        localProps.sboxTable = parsed.sboxTable.slice()
      } else {
        // ignore bad file
      }
    } catch {
      // ignore parse error
    }
  }
  reader.readAsText(file)
  return false // prevent auto upload
}
</script>

<style scoped>
.property-panel {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.header {
  display:flex;
  justify-content: space-between;
  align-items:center;
}
.ops { display:flex; gap:8px; }

.form-top { margin-bottom: 6px; }

.sbox-wrapper {
  overflow: auto;
  border: 1px solid #e6e6e6;
  padding: 8px;
  border-radius: 6px;
  background: #fff;
  max-height: 420px;
}

.sbox-grid {
  display: grid;
  gap: 6px;
}

.sbox-cell {
  position: relative;
  display:flex;
  align-items:center;
  justify-content:center;
  border-radius:4px;
  background:#fafafa;
  border:1px solid #ddd;
  overflow: hidden;
}

.cell-input {
  width: 100%;
  height: 100%;
  padding: 4px;
  box-sizing: border-box;
  border: none;
  outline: none;
  text-align:center;
  font-size: 12px;
  background: transparent;
}

.idx {
  position: absolute;
  top: 2px;
  left: 4px;
  font-size: 10px;
  color: #999;
}
</style>

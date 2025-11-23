<template>
  <el-card class="basic-params-card">
    <div class="header">
      <h3>分组算法基本参数</h3>
      <el-tag type="info" effect="plain">用于生成 CVC 与路径挖掘的基础参数</el-tag>
    </div>

    <el-form
      ref="formRef"
      :model="local"
      :rules="rules"
      label-width="140px"
      class="param-form"
    >
      <el-form-item label="分组长度 (bits)" prop="blockSize">
        <el-input-number
          v-model="local.blockSize"
          :min="1"
          :max="4096"
          :step="1"
          controls-position="right"
          @change="syncToStore"
        />
        <div class="hint">例：64、128。单位为比特。</div>
      </el-form-item>

      <el-form-item label="分支数 (branches)" prop="branches">
        <el-input-number
          v-model="local.branches"
          :min="1"
          :max="64"
          :step="1"
          controls-position="right"
          @change="syncToStore"
        />
        <div class="hint">算法的分支/片段数量（如 Feistel 的分支数）。</div>
      </el-form-item>

      <el-form-item label="轮函数描述" prop="roundFunction">
        <el-input
          v-model="local.roundFunction"
          type="textarea"
          :rows="4"
          placeholder="例如：F(x)=S(x ⊕ K) 或 自定义伪代码"
          @input="syncToStore"
        />
        <div class="hint">对轮函数做简要文本描述（会随参数提交到后端）。</div>
      </el-form-item>

      <el-form-item label="默认轮数 (optional)" prop="rounds">
        <el-input-number
          v-model="local.rounds"
          :min="0"
          :max="1000"
          :step="1"
          controls-position="right"
          @change="syncToStore"
        />
        <div class="hint">可不填或填 0 表示由后端/分析模块决定。</div>
      </el-form-item>

      <el-form-item label="备注 / 标签">
        <el-input
          v-model="local.note"
          placeholder="便于区分不同实验配置的简单备注"
          @input="syncToStore"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSave" :loading="saving">保存</el-button>
        <el-button @click="onReset">重置</el-button>
        <el-button type="text" @click="fillExample">示例填充</el-button>
      </el-form-item>
    </el-form>

    <el-divider />

    <div class="preview">
      <h4>当前参数预览</h4>
      <pre>{{ prettyParams }}</pre>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { reactive, ref, toRefs, computed } from 'vue'
import { useAnalysisStore } from '@/stores/useAnalysisStore'
import type { ElForm } from 'element-plus'

const store = useAnalysisStore()

/** 本地拷贝，避免直接绑定 store 导致过早校验或闪烁。
 * 但每次变更会通过 syncToStore() 持久化到 Pinia（实时同步策略）
 */
const local = reactive({
  blockSize: store.basicParams.blockSize ?? 64,
  branches: store.basicParams.branches ?? 4,
  roundFunction: store.basicParams.roundFunction ?? '',
  rounds: (store.basicParams as any).rounds ?? 0,
  note: (store.basicParams as any).note ?? '',
})

const formRef = ref<InstanceType<typeof ElForm> | null>(null)
const saving = ref(false)

// 校验规则
const rules = {
  blockSize: [
    { required: true, message: '请输入分组长度', trigger: 'blur' },
    {
      validator(_: any, value: number) {
        if (!Number.isInteger(value) || value <= 0) {
          return new Error('分组长度必须为正整数')
        }
        return true
      },
      trigger: 'blur',
    },
  ],
  branches: [
    { required: true, message: '请输入分支数', trigger: 'blur' },
    {
      validator(_: any, value: number) {
        if (!Number.isInteger(value) || value <= 0) {
          return new Error('分支数必须为正整数')
        }
        return true
      },
      trigger: 'blur',
    },
  ],
  roundFunction: [
    { required: true, message: '请描述轮函数', trigger: 'blur' },
    { min: 3, message: '轮函数描述过短', trigger: 'blur' },
  ],
  rounds: [
    {
      validator(_: any, value: number) {
        if (value == null) return true
        if (!Number.isInteger(value) || value < 0) {
          return new Error('轮数须为非负整数')
        }
        return true
      },
      trigger: 'blur',
    },
  ],
}

// 将本地数据实时同步到 Pinia store（后端提交时直接使用 store.collectParams()）
function syncToStore() {
  store.basicParams = {
    blockSize: Number(local.blockSize),
    branches: Number(local.branches),
    roundFunction: String(local.roundFunction),
    rounds: Number(local.rounds),
    note: String(local.note ?? ''),
  }
}

// 保存操作（会先校验）
async function onSave() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
  } catch (err) {
    // 验证失败，Element 会展示错误
    return
  }

  saving.value = true
  try {
    // 已经通过 syncToStore 保持同步，这里可以做额外动作（例如触发一个事件或调用 API）
    // 示例：触发 store 内的方法以标记已保存
    store._lastSavedAt = new Date().toISOString() // 非必需，仅示例
  } finally {
    saving.value = false
  }
}

// 重置到 store 中的初始值（而非硬置默认）
function onReset() {
  local.blockSize = store.basicParams.blockSize ?? 64
  local.branches = store.basicParams.branches ?? 4
  local.roundFunction = store.basicParams.roundFunction ?? ''
  ;(local as any).rounds = (store.basicParams as any).rounds ?? 0
  local.note = (store.basicParams as any).note ?? ''
}

// 示例填充（便于演示）
function fillExample() {
  local.blockSize = 64
  local.branches = 4
  local.roundFunction = 'F(x) = S(x ⊕ K); // S 为 8x8 S-box'
  ;(local as any).rounds = 12
  local.note = '示例配置：64-bit, Feistel-like'
  syncToStore()
}

const prettyParams = computed(() => JSON.stringify(store.basicParams, null, 2))

// 首次加载时确保 store 与本地一致
syncToStore()
</script>

<style scoped>
.basic-params-card {
  max-width: 900px;
  margin: 0 auto;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}
.param-form .hint {
  margin-top: 6px;
  font-size: 12px;
  color: #909399;
}
.preview {
  background: #fafafa;
  padding: 12px;
  border-radius: 6px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", "Helvetica Neue", monospace;
}
.preview pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}
</style>

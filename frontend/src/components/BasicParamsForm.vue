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
      <el-form-item label="算法名称" prop="algorithmName">
        <el-input
          v-model="local.algorithmName"
          placeholder="例如：Feistel, LBlock, DES"
          @input="syncToStore"
        />
        <div class="hint">给当前配置一个易于识别的名称。</div>
      </el-form-item>

      <el-form-item label="分组长度" prop="blockSize">
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

      <el-form-item label="分支数" prop="branches">
        <el-input-number
          v-model="local.branchNum"
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

      <el-form-item label="默认轮数" prop="rounds">
        <el-input-number
          v-model="local.roundNum"
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
import { ref, computed } from 'vue'
import type { ElForm } from 'element-plus'
import { useBasicParamsForm } from '@/composables/useBasicParamsForm' // 导入 Composable
import { ElMessage } from 'element-plus'; // 导入提示组件

// 1. 使用 Composable 引入所有逻辑和状态
const { formRef, local, rules, syncToStore, onReset, fillExample, store } = useBasicParamsForm();

const saving = ref(false);

// 2. 预览数据直接从全局 store 中获取 (计算属性确保实时响应)
const prettyParams = computed(() => JSON.stringify(store.basicParams, null, 2));

// 3. 保存操作：执行校验，然后调用 Store Action 提交数据
async function onSave() {
  if (!formRef.value) return;
  try {
    // 校验 (Composable 的功能)
    await formRef.value.validate();
    
    saving.value = true;
    
    // 提交 (Store 的功能)
    // await store.submitToBackend(); 
    
    ElMessage.success('配置已保存并提交！');
  } catch (error) {
    // 可能是验证失败（由 validate 自动处理），或是后端提交失败
    if (error instanceof Error) {
        ElMessage.error(`提交失败: ${error.message}`);
    }
  } finally {
    saving.value = false;
  }
}

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

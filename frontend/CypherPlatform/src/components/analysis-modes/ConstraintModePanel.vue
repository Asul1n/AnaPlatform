<template>
  <div class="analysis-panel">
    <h3 class="panel-title">⚙️ 条件约束挖掘分析</h3>
    <p class="panel-desc">
      该模块支持两类精细化约束策略，可用于定向筛选特定差分/掩码路线。
    </p>

    <el-tabs v-model="activeTab" type="card" class="tab-container">
      <!-- 🌀 1️⃣ 基于轮次的输入差分/掩码约束 -->
      <el-tab-pane label="基于轮次约束" name="round">
        <div class="tab-content">
          <h4>🔁 固定特定轮次的输入差分/掩码</h4>
          <el-form label-width="120px" class="round-form">
            <el-form-item label="目标轮次">
              <el-input-number v-model="targetRound" :min="1" :max="totalRounds" />
            </el-form-item>

            <el-form-item label="输入差分 / 掩码">
              <el-input v-model="inputPattern" placeholder="例如：0x3F / 110010" />
            </el-form-item>

            <el-form-item label="搜索方向">
              <el-radio-group v-model="searchDirection">
                <el-radio label="both">双向（上/下）</el-radio>
                <el-radio label="up">仅向上</el-radio>
                <el-radio label="down">仅向下</el-radio>
              </el-radio-group>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="runRoundAnalysis">开始分析</el-button>
            </el-form-item>
          </el-form>

          <div v-if="roundResult" class="analysis-result">
            <h4>分析结果</h4>
            <pre>{{ roundResult }}</pre>
          </div>
        </div>
      </el-tab-pane>

      <!-- 💡 2️⃣ 基于汉明重量的特征约束 -->
      <el-tab-pane label="基于汉明重量约束" name="hamming">
        <div class="tab-content">
          <h4>⚙️ 设定差分稀疏性（汉明重量）</h4>
          <el-form label-width="120px" class="hamming-form">
            <el-form-item label="汉明重量 n">
              <el-input-number v-model="hammingWeight" :min="1" :max="64" />
            </el-form-item>

            <el-form-item label="差分类型">
              <el-select v-model="diffType" placeholder="请选择类型">
                <el-option label="差分" value="diff" />
                <el-option label="线性掩码" value="mask" />
              </el-select>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="runHammingAnalysis">开始遍历搜索</el-button>
            </el-form-item>
          </el-form>

          <div v-if="hammingResult" class="analysis-result">
            <h4>分析结果</h4>
            <pre>{{ hammingResult }}</pre>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeTab = ref('round')

// === 轮次约束分析 ===
const targetRound = ref(4)
const totalRounds = 12
const inputPattern = ref('')
const searchDirection = ref('both')
const roundResult = ref('')

function runRoundAnalysis() {
  roundResult.value =
    `固定第 ${targetRound.value} 轮输入为 ${inputPattern.value}\n` +
    `搜索方向：${searchDirection.value}\n` +
    `→ 模拟运行中...`
}

// === 汉明重量约束分析 ===
const hammingWeight = ref(4)
const diffType = ref('diff')
const hammingResult = ref('')

function runHammingAnalysis() {
  hammingResult.value =
    `已设定汉明重量 = ${hammingWeight.value}, 类型 = ${diffType.value}\n` +
    `→ 启动全轮次遍历搜索...`
}
</script>

<style scoped>
.analysis-panel {
  padding: 20px;
}
.panel-title {
  font-size: 18px;
  margin-bottom: 6px;
  color: #1e3a8a;
}
.panel-desc {
  font-size: 14px;
  color: #475569;
  margin-bottom: 14px;
}
.tab-container {
  background: #fff;
  border-radius: 10px;
  padding: 10px;
}
.tab-content {
  padding: 16px;
}
.analysis-result {
  margin-top: 20px;
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  white-space: pre-wrap;
}
</style>

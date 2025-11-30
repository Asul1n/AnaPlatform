<template>
  <div class="analysis-panel path-mining-panel">
    <h3 class="panel-title">🔎 路径挖掘与评估模块</h3>
    <p class="panel-desc">
      该模块用于搜索、评估和优化满足约束条件的差分/线性特征路径。
    </p>

    <el-tabs v-model="activePathTab" type="card" class="tab-container">
      <el-tab-pane label="路径搜索配置" name="search">
        <div class="tab-content">
          <h4>🛣️ 路径搜索参数设定</h4>
          <el-form label-width="150px" class="search-form">
            
            <el-form-item label="分析类型">
              <el-select v-model="analysisType" placeholder="选择差分或线性分析" class="small-input">
                <el-option label="差分分析 (Differential)" value="diff" />
                <el-option label="线性分析 (Linear)" value="linear" />
              </el-select>
            </el-form-item>

            <el-form-item label="搜索深度 (轮数)">
              <el-input-number v-model="searchDepth" :min="2" :max="maxRounds" class="small-input-num" />
              <span class="tip-text"> / {{ maxRounds }} 轮</span>
            </el-form-item>

            <el-form-item label="概率 / 偏差阈值">
              <el-input v-model="threshold" placeholder="例如: 2^-32 (差分) 或 2^-8 (线性)" class="medium-input">
                <template #prepend>{{ thresholdLabel }}</template>
              </el-input>
            </el-form-item>

            <el-form-item label="固定输入差分">
              <el-input v-model="inputDiff" placeholder="例如: 0x0001 (十六进制)" class="medium-input" />
            </el-form-item>
            
            <el-form-item label="固定输出差分">
              <el-input v-model="outputDiff" placeholder="例如: 0x1000 (十六进制)" class="medium-input" />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="startPathSearch">🚀 开始路径搜索</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-tab-pane>

      <el-tab-pane label="路径约束与优化" name="optimize">
        <div class="tab-content">
          <h4>💡 路径稀疏性与活跃 S 盒约束</h4>
          <el-form label-width="150px" class="optimize-form">
            <el-form-item label="活跃S盒最大数">
              <el-input-number v-model="maxActiveSBoxes" :min="1" :max="maxSBoxes" class="small-input-num" />
              <span class="tip-text"> (总 S 盒数: {{ maxSBoxes }})</span>
            </el-form-item>

            <el-form-item label="路径位稀疏性">
              <el-radio-group v-model="sparsityConstraint" class="small-radio-group">
                <el-radio label="none">无约束</el-radio>
                <el-radio label="input">仅输入稀疏</el-radio>
                <el-radio label="all">路径全程稀疏</el-radio>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="冲突处理策略">
              <el-switch v-model="ignoreConflicts" active-text="忽略 S 盒冲突" inactive-text="严格检查 S 盒冲突" class="medium-switch" />
            </el-form-item>

            <el-form-item>
              <el-button type="warning" @click="optimizePath">🔁 重新优化路径</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-tab-pane>

    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

// --- 模块状态 ---
const activePathTab = ref('search')
const maxRounds = 16 // 假设总轮数
const maxSBoxes = 12 * maxRounds // 假设每轮有12个S盒

// --- 路径搜索配置 (Tab 1: search) ---
const analysisType = ref('diff') // 'diff' 或 'linear'
const searchDepth = ref(8)
const threshold = ref('2^-32')
const inputDiff = ref('0x0001') 
const outputDiff = ref('0x1000')

// L121 修正：移除未使用的变量 searchAlgorithm
// const searchAlgorithm = ref('astar') 

const lastSearchMessage = ref('')

const thresholdLabel = computed(() => (analysisType.value === 'diff' ? '最小概率 P' : '最小偏差 |ε|'))

// --- 路径约束与优化 (Tab 2: optimize) ---
const maxActiveSBoxes = ref(40)
const sparsityConstraint = ref('all') // 'none', 'input', 'all'
const ignoreConflicts = ref(false)

// --- 结果列表 (Tab 3: results) ---
interface PathResult {
  id: number
  depth: number
  valueType: 'P' | '|ε|'
  value: string
  activeSBoxes: number
  pathSummary: string
}
const pathResultList = ref<PathResult[]>([])


// --- 方法 ---

function startPathSearch() {
  lastSearchMessage.value =
    `开始 ${analysisType.value === 'diff' ? '差分分析' : '线性分析'} 路径搜索...\n` +
    `  > 搜索深度: ${searchDepth.value} 轮\n` +
    `  > 最小 ${thresholdLabel.value}: ${threshold.value}\n` +
    `  > **固定输入差分**: ${inputDiff.value}\n` + 
    `  > **固定输出差分**: ${outputDiff.value}\n` +
    `→ 运行中，请切换到“结果列表”查看进度... (模拟耗时 5s)`
  
  // 模拟搜索结果
  setTimeout(() => {
    pathResultList.value = [
      { id: 1, depth: 8, valueType: analysisType.value === 'diff' ? 'P' : '|ε|', value: analysisType.value === 'diff' ? '2^-35.6' : '2^-8.2', activeSBoxes: 38, pathSummary: `${inputDiff.value} → ... → ${outputDiff.value}` },
      { id: 2, depth: 8, valueType: analysisType.value === 'diff' ? 'P' : '|ε|', value: analysisType.value === 'diff' ? '2^-36.0' : '2^-8.5', activeSBoxes: 40, pathSummary: `${inputDiff.value} → ... → ${outputDiff.value}` },
    ]
    ElMessage.success('路径搜索完成！已找到 ' + pathResultList.value.length + ' 条路径。')
    activePathTab.value = 'results'
  }, 5000)
}

function optimizePath() {
  lastSearchMessage.value =
    `正在根据约束条件重新优化已找到的路径...\n` +
    `  > 活跃S盒上限: ${maxActiveSBoxes.value}\n` +
    `  > 稀疏性策略: ${sparsityConstraint.value}\n` +
    `  > 冲突忽略: ${ignoreConflicts.value ? '是' : '否'}\n` +
    `→ 优化完成，结果列表已更新。 (模拟耗时 2s)`
  
  // 模拟优化后更新结果
  const newCount = Math.max(0, pathResultList.value.length - 1);
  pathResultList.value = pathResultList.value.slice(0, newCount); 
  
  ElMessage.warning(`路径优化完成。筛选后剩余 ${pathResultList.value.length} 条路径。`)
  activePathTab.value = 'results'
}
</script>

<style scoped>
/* 继承自用户提供的样式 */
.analysis-panel {
  padding: 20px;
}
.panel-title {
  font-size: 18px;
  margin-bottom: 6px;
  color: #1e3a8a; /* 深蓝色 */
}
.panel-desc {
  font-size: 14px;
  color: #475569; /* 灰色 */
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

/* 新增样式 */
.tip-text {
  margin-left: 10px;
  color: #94a3b8;
  font-size: 13px;
}

/* 优化后的输入组件宽度样式 */
.small-input {
  width: 150px; /* 较小的选择框/输入框宽度 */
}
.small-input-num {
  width: 150px; /* 较小的数字输入框宽度 */
}
/* el-input 中包含 prepend 的组件需要更大的宽度 */
.medium-input {
  width: 280px; /* 中等宽度，用于包含前缀的输入框 */
}
</style>
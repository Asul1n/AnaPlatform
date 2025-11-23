<template>
  <div class="condition-layout">
    <!-- 左：条件约束面板 -->
    <aside class="constraint-panel">
      <el-card class="panel-card">
        <h3 class="section-title">条件约束设置</h3>

        <el-form label-position="top" :model="constraints" label-width="120px">
          <el-form-item label="轮次范围">
            <el-slider v-model="constraints.roundRange" range :max="20" />
          </el-form-item>

          <el-form-item label="比特位约束">
            <BitMatrix v-model="constraints.bitMask" :size="16" />
          </el-form-item>

          <el-form-item label="S盒输入限制">
            <el-switch v-model="constraints.sboxLimit" />
          </el-form-item>

          <el-form-item label="活动比特上限">
            <el-input-number v-model="constraints.activeLimit" :min="1" :max="64" />
          </el-form-item>

          <div class="panel-actions">
            <el-button type="primary" @click="applyConstraints">应用约束</el-button>
            <el-button @click="resetConstraints">重置</el-button>
          </div>
        </el-form>
      </el-card>
    </aside>

    <!-- 中：可视化展示 -->
    <main class="visualization-area">
      <el-card class="panel-card">
        <h3 class="section-title">约束可视化</h3>
        <DiffPathGraph :constraints="constraints" />
      </el-card>
    </main>

    <!-- 右：结果展示与控制 -->
    <section class="result-panel">
      <el-card class="panel-card">
        <h3 class="section-title">筛选结果</h3>

        <div class="stats">
          <p>符合条件路径：{{ results.length }}</p>
          <p>最高概率：{{ maxProb.toExponential(3) }}</p>
        </div>

        <el-table :data="results" height="400">
          <el-table-column prop="id" label="路径ID" width="90" />
          <el-table-column prop="prob" label="概率" />
          <el-table-column prop="activeBits" label="活动比特数" />
          <el-table-column prop="rounds" label="轮次" />
        </el-table>

        <div class="panel-actions">
          <el-button type="success" @click="startSearch">启动挖掘</el-button>
          <el-button @click="exportResults">导出结果</el-button>
        </div>
      </el-card>
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import BitMatrix from "@/components/BitMatrix.vue"
import DiffPathGraph from "@/components/DiffPathGraph.vue"

// ====== 状态定义 ======
const constraints = ref({
  roundRange: [1, 10],
  bitMask: Array(16).fill(Array(16).fill(0)),
  sboxLimit: false,
  activeLimit: 16,
})

const results = ref([
  { id: 1, prob: 1.23e-6, activeBits: 12, rounds: 8 },
  { id: 2, prob: 4.56e-7, activeBits: 14, rounds: 9 },
])

const maxProb = computed(() =>
  results.value.length ? Math.max(...results.value.map((r) => r.prob)) : 0
)

// ====== 交互逻辑 ======
const applyConstraints = () => {
  console.log("约束已应用：", constraints.value)
  // 后端交互逻辑（axios.post('/api/search/constraints', constraints.value)）
}

const resetConstraints = () => {
  constraints.value = {
    roundRange: [1, 10],
    bitMask: Array(16).fill(Array(16).fill(0)),
    sboxLimit: false,
    activeLimit: 16,
  }
}

const startSearch = () => {
  console.log("启动挖掘任务", constraints.value)
  // 后端调用搜索接口
}

const exportResults = () => {
  const blob = new Blob([JSON.stringify(results.value, null, 2)], {
    type: "application/json",
  })
  const url = URL.createObjectURL(blob)
  const link = document.createElement("a")
  link.href = url
  link.download = "condition_search_results.json"
  link.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped lang="scss">
.condition-layout {
  display: grid;
  grid-template-columns: 280px 1fr 360px;
  height: 100vh;
  gap: 10px;
  padding: 10px;
  background: #f8fafc;
}

.panel-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.section-title {
  font-weight: 600;
  margin-bottom: 8px;
}

.constraint-panel,
.visualization-area,
.result-panel {
  display: flex;
  flex-direction: column;
}

.stats {
  margin-bottom: 10px;
  p {
    margin: 0;
    font-size: 14px;
  }
}

.panel-actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}
</style>

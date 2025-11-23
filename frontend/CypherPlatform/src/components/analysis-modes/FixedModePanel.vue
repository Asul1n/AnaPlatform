<template>
  <div class="analysis-container">
    <!-- 页面标题 -->
    <div class="text-center mb-10">
      <h1 class="text-3xl font-bold text-gray-800 mb-3">固定输入输出场景下聚合路线自动化挖掘</h1>
      <p class="text-gray-600 max-w-3xl mx-auto">在固定初始输入与指定目标轮次输出的场景约束下，对聚合路线开展自动化挖掘，采用聚合分析方法实现量化挖掘与分析。</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 左侧：参数配置面板 -->
      <div class="lg:col-span-1">
        <el-card class="card" shadow="hover">
          <template #header>
            <h2 class="text-xl font-semibold text-gray-800">参数配置</h2>
          </template>

          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">初始输入差分</label>
              <el-input v-model="inputDiff" placeholder="例如: 0x0001" />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">目标输出差分</label>
              <el-input v-model="outputDiff" placeholder="例如: 0x0040" />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">目标轮次</label>
              <el-select v-model="targetRounds" class="w-full">
                <el-option value="3" label="3轮" />
                <el-option value="4" label="4轮" />
                <el-option value="5" label="5轮" />
                <el-option value="6" label="6轮" />
              </el-select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">概率阈值 2<sup>-{{ probabilityThreshold }}</sup></label>
              <el-slider v-model="probabilityThreshold" :min="1" :max="10" />
            </div>

            <el-button
              type="primary"
              class="w-full"
              :loading="isAnalyzing"
              @click="startAnalysis"
            >
              <i class="fas fa-play-circle mr-2"></i>
              {{ isAnalyzing ? '分析中...' : '开始挖掘分析' }}
            </el-button>
          </div>

          <div class="mt-6 pt-4 border-t border-gray-200">
            <h3 class="text-lg font-medium text-gray-800 mb-2">概率赋值规则</h3>
            <p class="text-sm text-gray-600">该方法遵循特定的概率赋值规则，以初始概率值1为起点，按2<sup>-1</sup>、2<sup>-2</sup>……的指数递减规律依次分配后续概率权重。</p>
          </div>
        </el-card>

        <!-- 分析进度 -->
        <el-card v-if="isAnalyzing" class="card mt-6" shadow="hover">
          <template #header>
            <h3 class="text-lg font-medium text-gray-800">分析进度</h3>
          </template>

          <div class="flex items-center justify-center mb-4">
            <el-progress
              type="circle"
              :percentage="analysisProgress"
              :width="120"
              :stroke-width="8"
            />
          </div>
          <p class="text-center text-gray-600">{{ progressStatus }}</p>
        </el-card>
      </div>

      <!-- 中间：挖掘结果展示 -->
      <div class="lg:col-span-2">
        <el-card class="card mb-6" shadow="hover">
          <template #header>
            <div class="flex justify-between items-center">
              <h2 class="text-xl font-semibold text-gray-800">聚合路线挖掘结果</h2>
              <div class="text-sm text-gray-500">
                <i class="fas fa-history mr-1"></i>
                最后更新: {{ lastUpdated }}
              </div>
            </div>
          </template>

          <div v-if="routes.length > 0" class="el-alert el-alert--info mb-6">
            <div class="el-alert__content">
              <p class="el-alert__description">
                已发现 <strong>{{ routes.length }}</strong> 条符合条件的聚合路线。对路线所对应的各概率权重进行累加计算，实现量化挖掘与分析。
              </p>
            </div>
          </div>

          <div v-else class="text-center py-8 text-gray-500">
            <i class="fas fa-search text-4xl mb-3"></i>
            <p>暂无挖掘结果，请配置参数并开始分析</p>
          </div>

          <!-- 概率分布图表 -->
          <div v-if="routes.length > 0" class="mb-6">
            <h3 class="text-lg font-medium text-gray-800 mb-3">概率分布</h3>
            <div class="bg-gray-50 p-4 rounded-lg">
              <canvas ref="probabilityChart" height="120"></canvas>
            </div>
          </div>

          <!-- 聚合路线列表 -->
          <el-table v-if="routes.length > 0" :data="routes" class="w-full">
            <el-table-column prop="id" label="路线ID" width="120" />
            <el-table-column label="概率权重" width="200">
              <template #default="{ row }">
                <div class="flex items-center">
                  <el-progress
                    :percentage="row.probability * 100"
                    :show-text="false"
                    class="flex-1 mr-2"
                  />
                  <span class="text-sm text-gray-700">2<sup>-{{ row.exponent }}</sup></span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag
                  :type="row.status === 'verified' ? 'success' :
                         row.status === 'analyzing' ? 'warning' : 'info'"
                >
                  {{ row.status === 'verified' ? '已验证' :
                     row.status === 'analyzing' ? '分析中' : '待验证' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button link type="primary" @click="showRouteDetails(row)">详情</el-button>
                <el-button link type="primary" @click="exportRoute(row)">导出</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </div>
    </div>

    <!-- 路线详情对话框 -->
    <el-dialog v-model="dialogVisible" :title="`${selectedRoute?.id} 详情`" width="700px">
      <div v-if="selectedRoute" class="space-y-4">
        <div>
          <h4 class="font-medium text-gray-700 mb-2">输入输出差分</h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-600">初始输入差分</p>
              <p class="font-mono text-gray-800">{{ inputDiff }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">目标输出差分</p>
              <p class="font-mono text-gray-800">{{ outputDiff }}</p>
            </div>
          </div>
        </div>

        <div>
          <h4 class="font-medium text-gray-700 mb-2">概率权重</h4>
          <div class="flex items-center">
            <el-progress
              :percentage="selectedRoute.probability * 100"
              class="w-48 mr-2"
            />
            <span class="text-gray-800">2<sup>-{{ selectedRoute.exponent }}</sup></span>
          </div>
        </div>

        <div>
          <h4 class="font-medium text-gray-700 mb-2">轮次分析</h4>
          <div class="space-y-2">
            <div v-for="round in selectedRoute.rounds" :key="round.number" class="flex items-center">
              <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-medium mr-3">
                {{ round.number }}
              </div>
              <div class="flex-1">
                <p class="text-sm text-gray-800">差分状态: <span class="font-mono">{{ round.state }}</span></p>
              </div>
            </div>
          </div>
        </div>

        <div>
          <h4 class="font-medium text-gray-700 mb-2">路线特征</h4>
          <ul class="list-disc pl-5 text-gray-600 space-y-1">
            <li v-for="feature in selectedRoute.features" :key="feature">{{ feature }}</li>
          </ul>
        </div>
      </div>

      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="exportRoute(selectedRoute)">导出路线</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import Chart from 'chart.js/auto'

// 响应式数据
const inputDiff = ref('0x0001')
const outputDiff = ref('0x0040')
const targetRounds = ref('4')
const probabilityThreshold = ref(3)
const isAnalyzing = ref(false)
const analysisProgress = ref(0)
const progressStatus = ref('准备开始分析...')
const routes = ref<any[]>([])
const selectedRoute = ref<any>(null)
const dialogVisible = ref(false)
const lastUpdated = ref('')
const probabilityChart = ref<HTMLCanvasElement>()

// 方法
const startAnalysis = () => {
  isAnalyzing.value = true
  analysisProgress.value = 0
  progressStatus.value = '初始化分析参数...'
  routes.value = []

  // 模拟分析过程
  const interval = setInterval(() => {
    if (analysisProgress.value < 100) {
      analysisProgress.value += 5

      if (analysisProgress.value < 30) {
        progressStatus.value = '扫描初始输入差分...'
      } else if (analysisProgress.value < 60) {
        progressStatus.value = '分析中间轮次状态...'
      } else if (analysisProgress.value < 90) {
        progressStatus.value = '计算概率权重...'
      } else {
        progressStatus.value = '生成聚合路线...'
      }
    } else {
      clearInterval(interval)
      isAnalyzing.value = false
      progressStatus.value = '分析完成'
      lastUpdated.value = new Date().toLocaleString()

      // 生成模拟结果
      generateResults()
    }
  }, 200)
}

const generateResults = () => {
  routes.value = [
    {
      id: 'Route-001',
      probability: 0.95,
      exponent: 1,
      status: 'verified',
      rounds: [
        { number: 1, state: '0x0001' },
        { number: 2, state: '0x0080' },
        { number: 3, state: '0x0020' },
        { number: 4, state: '0x0040' }
      ],
      features: ['高概率路线', '满足目标输出', '符合约束条件']
    },
    {
      id: 'Route-007',
      probability: 0.75,
      exponent: 2,
      status: 'verified',
      rounds: [
        { number: 1, state: '0x0001' },
        { number: 2, state: '0x0040' },
        { number: 3, state: '0x0010' },
        { number: 4, state: '0x0040' }
      ],
      features: ['中等概率路线', '满足目标输出', '路径较长']
    },
    {
      id: 'Route-012',
      probability: 0.5,
      exponent: 3,
      status: 'analyzing',
      rounds: [
        { number: 1, state: '0x0001' },
        { number: 2, state: '0x0200' },
        { number: 3, state: '0x0100' },
        { number: 4, state: '0x0040' }
      ],
      features: ['低概率路线', '满足目标输出', '路径复杂']
    }
  ]

  // 初始化图表
  nextTick(() => {
    initChart()
  })
}

const showRouteDetails = (route: any) => {
  selectedRoute.value = route
  dialogVisible.value = true
}

const exportRoute = (route: any) => {
  ElMessage.success(`导出路线 ${route.id} 的数据`)
  // 在实际应用中，这里会实现导出功能
}

const initChart = () => {
  if (!probabilityChart.value) return

  const ctx = probabilityChart.value.getContext('2d')
  if (!ctx) return

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: routes.value.map(r => r.id),
      datasets: [{
        label: '概率权重',
        data: routes.value.map(r => r.probability),
        backgroundColor: 'rgba(59, 130, 246, 0.7)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          max: 1,
          title: {
            display: true,
            text: '概率值'
          }
        },
        x: {
          title: {
            display: true,
            text: '路线ID'
          }
        }
      }
    }
  })
}

// 生命周期
onMounted(() => {
  lastUpdated.value = new Date().toLocaleString()
})
</script>

<style scoped>
.analysis-container {
  padding: 20px;
  background-color: #f8fafc;
  min-height: 100vh;
}

.card {
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
</style>

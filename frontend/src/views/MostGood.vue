<template>
  <div class="diff-path">
    <h3 class="title">差分路径展示</h3>
    <p class="summary">
      共 {{ paths.length }} 条路径
    </p>

    <svg :width="svgWidth" :height="svgHeight">
      <defs>
        <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
          <path d="M0,0 L8,4 L0,8 Z" fill="#2563eb" />
        </marker>

        <!-- 渐变背景 -->
        <linearGradient id="boxGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#f8fafc" />
          <stop offset="100%" stop-color="#e2e8f0" />
        </linearGradient>
        <linearGradient id="selectedGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#e3f2fd" />
          <stop offset="100%" stop-color="#bbdefb" />
        </linearGradient>
      </defs>

      <!-- ✅ 顶部统一显示 Round 标签 -->
      <template v-if="paths.length > 0">
        <template v-for="(r, i) in paths[paths.length - 1].rounds" :key="'round'+i">
          <text
            :x="getX(i) + boxW / 2"
            y="30"
            text-anchor="middle"
            font-size="12"
            font-weight="bold"
            fill="#2c3e50"
            class="round-label"
          >
            Round {{ i }}
          </text>
        </template>
      </template>

      <!-- ✅ 遍历多条路径 -->
      <template v-for="(path, tIndex) in paths" :key="tIndex">
        <!-- 路径名称标签 -->
        <text
          :x="getX(-0.8)"
          :y="getY(tIndex) + boxH / 2 + 5"
          text-anchor="end"
          font-size="11"
          font-weight="600"
          :fill="selectedPath === tIndex ? '#1e40af' : '#4b5563'"
          class="path-name"
        >
          {{ path.name }}
        </text>

        <template v-for="(round, i) in path.rounds" :key="i">
          <!-- 差分框 -->
          <rect
            :x="getX(i)"
            :y="getY(tIndex)"
            :width="boxW"
            :height="boxH"
            rx="6"
            ry="6"
            :fill="selectedPath === tIndex ? 'url(#selectedGradient)' : 'url(#boxGradient)'"
            :stroke="selectedPath === tIndex ? '#3b82f6' : '#cbd5e1'"
            stroke-width="1.5"
            class="diff-box fade-in"
            @click="selectPath(tIndex)"
            style="cursor:pointer"
            :class="{ 'selected-box': selectedPath === tIndex }"
          >
            <title>{{ formatRoundData(round) }}</title>
          </rect>

          <!-- 差分文本 -->
          <g @click="selectPath(tIndex)" style="cursor:pointer">
            <text
              :x="getX(i) + boxW / 2"
              :y="getY(tIndex) + 16"
              text-anchor="middle"
              font-family="'Courier New', monospace"
              font-size="10"
              font-weight="600"
              fill="#1e40af"
            >
              xa: {{ round.xa }}
            </text>
            <text
              :x="getX(i) + boxW / 2"
              :y="getY(tIndex) + 28"
              text-anchor="middle"
              font-family="'Courier New', monospace"
              font-size="10"
              font-weight="600"
              fill="#dc2626"
            >
              xb: {{ round.xb }}
            </text>
            <text
              :x="getX(i) + boxW / 2"
              :y="getY(tIndex) + 40"
              text-anchor="middle"
              font-family="'Courier New', monospace"
              font-size="10"
              font-weight="600"
              fill="#16a34a"
            >
              xc: {{ round.xc }}
            </text>
            <text
              :x="getX(i) + boxW / 2"
              :y="getY(tIndex) + 52"
              text-anchor="middle"
              font-family="'Courier New', monospace"
              font-size="10"
              font-weight="600"
              fill="#9333ea"
            >
              xd: {{ round.xd }}
            </text>
          </g>

          <!-- 箭头线 - 只在相邻轮次之间绘制 -->
          <template v-if="i < path.rounds.length - 1">
            <line
              :x1="getX(i) + boxW"
              :y1="getY(tIndex) + boxH / 2"
              :x2="getX(i + 1)"
              :y2="getY(tIndex) + boxH / 2"
              :stroke="selectedPath === tIndex ? '#2563eb' : 'rgba(148,163,184,0.6)'"
              stroke-width="1.6"
              stroke-linecap="round"
              marker-end="url(#arrow)"
              class="arrow-line"
            />

          </template>
        </template>

        <!-- 总概率显示在路径末尾 -->
        <text
          :x="getX(path.rounds.length) + 10"
          :y="getY(tIndex) + boxH / 2 + 5"
          text-anchor="start"
          font-size="11"
          font-weight="600"
          :fill="selectedPath === tIndex ? '#1e40af' : '#64748b'"
          class="total-prob"
        >
          {{ path.totalProb }}
        </text>
      </template>
    </svg>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'

interface DiffRound {
  xa: string
  xb: string
  xc: string
  xd: string
}

interface DiffPath {
  name: string
  totalProb: string
  rounds: DiffRound[]
}

/* ✅ 从文档中录入的真实数据 */
const paths = ref<DiffPath[]>([
    {
    name: "四轮路线",
    totalProb: "2^(-6)",
    rounds: [
      { xa: "0x00000000", xb: "0x00000000", xc: "0x00000000", xd: "0x80000000" },
      { xa: "0x00000000", xb: "0x00000000", xc: "0x10000000", xd: "0x00000000" }
    ]
  },
  {
    name: "二轮路线",
    totalProb: "2⁻⁰",
    rounds: [
      { xa: "0x80000000", xb: "0x80000000", xc: "0x80000000", xd: "0x80000000" },
      { xa: "0x00000000", xb: "0x00000000", xc: "0x00000000", xd: "0x80000000" },
      { xa: "0x00000000", xb: "0x00000000", xc: "0x10000000", xd: "0x00000000" }
    ]
  },
  {
    name: "三轮路线",
    totalProb: "2⁻²",
    rounds: [
      { xa: "0x80000000", xb: "0x80000000", xc: "0x80000000", xd: "0x80000000" },
      { xa: "0x00000000", xb: "0x00000000", xc: "0x00000000", xd: "0x80000000" },
      { xa: "0x00000000", xb: "0x00000000", xc: "0x10000000", xd: "0x00000000" },
      { xa: "0x00000000", xb: "0x00800000", xc: "0x02000000", xd: "0x00000000" }
    ]
  },
  {
    name: "四轮路线",
    totalProb: "2⁻⁶",
    rounds: [
      { xa: "0x80000000", xb: "0x80000000", xc: "0x80000000", xd: "0x80000000" },
      { xa: "0x00000000", xb: "0x00000000", xc: "0x00000000", xd: "0x80000000" },
      { xa: "0x00000000", xb: "0x00000000", xc: "0x10000000", xd: "0x00000000" },
      { xa: "0x00000000", xb: "0x00800000", xc: "0x02000000", xd: "0x00000000" },
      { xa: "0x00000001", xb: "0x00140000", xc: "0x00400000", xd: "0x00000000" }
    ]
  },
  {
    name: "五轮路线",
    totalProb: "2⁻¹⁰",
    rounds: [
      { xa: "0x80000000", xb: "0x80000000", xc: "0x80000010", xd: "0x80000014" },
      { xa: "0x00000000", xb: "0x80000000", xc: "0x80000000", xd: "0x80000000" },
      { xa: "0x00000100", xb: "0x00000000", xc: "0x00000000", xd: "0x00000000" },
      { xa: "0x00020000", xb: "0x00000000", xc: "0x00000000", xd: "0x00000100" },
      { xa: "0x04000000", xb: "0x00000000", xc: "0x00000020", xd: "0x00020000" },
      { xa: "0x00000008", xb: "0x00000001", xc: "0x00004004", xd: "0x04000000" }
    ]
  },
  {
    name: "六轮路线",
    totalProb: "2⁻¹⁸",
    rounds: [
      { xa: "0x80000000", xb: "0x80000000", xc: "0x80000010", xd: "0x80000014" },
      { xa: "0x00000000", xb: "0x80000000", xc: "0x80000000", xd: "0x80000000" },
      { xa: "0x00000100", xb: "0x00000000", xc: "0x00000000", xd: "0x00000000" },
      { xa: "0x00020000", xb: "0x00000000", xc: "0x00000000", xd: "0x00000100" },
      { xa: "0x04000000", xb: "0x00000000", xc: "0x00000020", xd: "0x00020000" },
      { xa: "0x00000008", xb: "0x00000001", xc: "0x00004004", xd: "0x04000000" },
      { xa: "0x00001200", xb: "0x28000200", xc: "0x80800800", xd: "0x00000008" }
    ]
  },
  {
    name: "七轮路线",
    totalProb: "2⁻²⁷",
    rounds: [
      { xa: "0x80000014", xb: "0x80400014", xc: "0x80400004", xd: "0x80400080" },
      { xa: "0x80000000", xb: "0x80000000", xc: "0x80000010", xd: "0x80000014" },
      { xa: "0x00000000", xb: "0x80000000", xc: "0x80000000", xd: "0x80000000" },
      { xa: "0x00000100", xb: "0x00000000", xc: "0x00000000", xd: "0x00000000" },
      { xa: "0x00020000", xb: "0x00000000", xc: "0x00000000", xd: "0x00000100" },
      { xa: "0x04000000", xb: "0x00000000", xc: "0x00000020", xd: "0x00020000" },
      { xa: "0x00000008", xb: "0x00000001", xc: "0x00004004", xd: "0x04000000" },
      { xa: "0x00001200", xb: "0x28000200", xc: "0x80800800", xd: "0x00000008" }
    ]
  },
  {
    name: "八轮路线",
    totalProb: "2⁻³⁹",
    rounds: [
      { xa: "0x80000014", xb: "0x80400014", xc: "0x80400004", xd: "0x80400080" },
      { xa: "0x80000000", xb: "0x80000000", xc: "0x80000010", xd: "0x80000014" },
      { xa: "0x00000000", xb: "0x80000000", xc: "0x80000000", xd: "0x80000000" },
      { xa: "0x00000100", xb: "0x00000000", xc: "0x00000000", xd: "0x00000000" },
      { xa: "0x00020000", xb: "0x00000000", xc: "0x00000000", xd: "0x00000100" },
      { xa: "0x04000000", xb: "0x00000000", xc: "0x00000020", xd: "0x00020000" },
      { xa: "0x00000008", xb: "0x00000001", xc: "0x00004004", xd: "0x04000000" },
      { xa: "0x00001200", xb: "0x28000200", xc: "0x80800800", xd: "0x00000008" },
      { xa: "0x00200050", xb: "0x05440050", xc: "0x10100101", xd: "0x00001200" }
    ]
  }
])

// ---- 布局参数 ----
const svgWidth = ref(window.innerWidth - 100)
const svgHeight = ref(600)
const boxW = ref(140)
const boxH = 60
const rowGap = 120
const step = ref(160)
const selectedPath = ref<number | null>(null)

function resizeLayout() {
  const available = window.innerWidth - 100
  const maxLen = Math.max(...paths.value.map((p) => p.rounds.length))
  step.value = Math.max(160, available / (maxLen + 2)) // 动态调整步长
  boxW.value = Math.max(120, step.value - 20) // 根据步长调整框宽
  svgWidth.value = Math.max(maxLen * step.value + 300, available) // 增加右边距
  svgHeight.value = paths.value.length * rowGap + 100
}

function selectPath(index: number) {
  selectedPath.value = selectedPath.value === index ? null : index
}

function formatRoundData(round: DiffRound): string {
  return `xa: ${round.xa}\nxb: ${round.xb}\nxc: ${round.xc}\nxd: ${round.xd}`
}

onMounted(() => {
  resizeLayout()
  window.addEventListener('resize', resizeLayout)
})
onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeLayout)
})

function getX(i: number) {
  return i * step.value + 120 // 增加左边距
}
function getY(pathIndex: number) {
  return 60 + pathIndex * rowGap
}
</script>

<style scoped>
.diff-path {
  width: 100%;
  overflow-x: auto;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  user-select: none;
  min-height: 700px; /* 确保有足够高度 */
}

.title {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  text-align: center;
}

.summary {
  margin: 6px 0 16px;
  font-size: 14px;
  color: #475569;
  text-align: center;
}

.highlight-info {
  color: #1e40af;
  font-weight: 600;
}

.fade-in {
  opacity: 0;
  animation: fadeIn 0.8s ease forwards;
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}

.arrow-line {
  stroke-dasharray: 300;
  stroke-dashoffset: 300;
  animation: drawArrow 1s ease forwards;
  animation-delay: 0.2s;
}

@keyframes drawArrow {
  to {
    stroke-dashoffset: 0;
  }
}

.round-label {
  font-size: 13px;
  fill: #1e40af;
  background: #eff6ff;
  padding: 4px 10px;
  border-radius: 6px;
}


.path-name {
  opacity: 0;
  animation: fadeIn 0.8s ease forwards 0.6s;
}

.diff-box {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.08));
  transition: all 0.3s ease;
  stroke-dasharray: none;
}
.diff-box:hover {
  transform: translateY(-3px);
  filter: drop-shadow(0 6px 10px rgba(37, 99, 235, 0.25));
}

.selected-box {
  filter: drop-shadow(0 4px 12px rgba(59, 130, 246, 0.4));
}

.prob-text {
  opacity: 0;
  animation: fadeIn 0.8s ease forwards 0.8s;
}

.total-prob {
  opacity: 0;
  animation: fadeIn 0.8s ease forwards 1s;
  font-family: 'Courier New', monospace;
}

/* 确保SVG内容居中显示 */
svg {
  display: block;
  margin: 0 auto;
}
</style>

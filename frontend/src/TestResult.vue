<template>
  <div class="diff-path">
    <h3 class="title">差分路径展示</h3>
    <p class="summary">
      共 {{ paths.length }} 条路径
      <span v-if="selectedPath !== null" class="highlight-info">
        ｜选中路径 #{{ selectedPath + 1 }} 累计概率：{{ totalProb(selectedPath) }}
      </span>
    </p>

    <svg :width="svgWidth" :height="svgHeight">
      <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
          <path d="M0,0 L10,5 L0,10 Z" fill="#444" />
        </marker>
      </defs>

      <!-- ✅ 顶部统一显示 Round 标签 -->
      <template v-if="paths.length > 0">
        <template v-for="(r, i) in paths[0]" :key="'round'+i">
          <text
            :x="getX(i) + boxW / 2"
            y="30"
            text-anchor="middle"
            font-size="12"
            fill="#777"
          >
            Round {{ i }}
          </text>
        </template>
      </template>

      <!-- ✅ 遍历多条路径 -->
      <template v-for="(trail, tIndex) in paths" :key="tIndex">
        <template v-for="(r, i) in trail" :key="i">
          <!-- 差分框 -->
          <rect
            :x="getX(i)"
            :y="getY(tIndex)"
            :width="boxW"
            :height="boxH"
            rx="8"
            ry="8"
            :fill="selectedPath === tIndex ? '#dceeff' : '#e8f3ff'"
            :stroke="selectedPath === tIndex ? '#3b82f6' : '#4b9ce2'"
            stroke-width="1.4"
            class="fade-in"
            @click="selectPath(tIndex)"
            style="cursor:pointer"
          >
            <title>{{ r.input }}</title>
          </rect>

          <!-- 差分文本 -->
          <text
            :x="getX(i) + boxW / 2"
            :y="getY(tIndex) + boxH / 2 + 4"
            text-anchor="middle"
            font-family="monospace"
            font-size="13"
            fill="#000"
            @click="selectPath(tIndex)"
            style="cursor:pointer"
          >
            {{ r.input }}
          </text>

          <!-- 箭头线 -->
          <line
            v-if="i < trail.length - 1"
            :x1="getX(i) + boxW"
            :y1="getY(tIndex) + boxH / 2"
            :x2="getX(i + 1)"
            :y2="getY(tIndex) + boxH / 2"
            :stroke="selectedPath === tIndex ? '#2563eb' : '#444'"
            stroke-width="1.4"
            marker-end="url(#arrow)"
            class="arrow-line"
          />

          <!-- 概率文字：自动居中在箭头上方 -->
          <text
            v-if="i < trail.length - 1 && r.prob"
            :x="(getX(i) + boxW + getX(i + 1)) / 2"
            :y="getY(tIndex) + boxH / 2 - 10"
            text-anchor="middle"
            font-size="12"
            font-family="monospace"
            :fill="selectedPath === tIndex ? '#1e40af' : '#222'"
            class="fade-in"
          >
            {{ r.prob }}
          </text>
        </template>
      </template>
    </svg>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'

interface DiffRound {
  input: string
  prob: string
}

type DiffPath = DiffRound[]

/* ✅ 示例数据 */
const paths = ref<DiffPath[]>([
  [
    { input: 'ΔX₀=0x20', prob: 'p=1/4' },
    { input: 'ΔX₁=0x40', prob: 'p=1/8' },
    { input: 'ΔX₂=0x80', prob: 'p=1/16' },
    { input: 'ΔX₃=0xC0', prob: '' },
  ],
  [
    { input: 'ΔX₀=0x10', prob: 'p=1/2' },
    { input: 'ΔX₁=0x30', prob: 'p=1/4' },
    { input: 'ΔX₂=0x70', prob: '' },
  ],
  [
    { input: 'ΔX₀=0x05', prob: 'p=1/8' },
    { input: 'ΔX₁=0x0A', prob: 'p=1/16' },
    { input: 'ΔX₂=0x14', prob: 'p=1/8' },
    { input: 'ΔX₃=0x28', prob: '' },
  ],
])

// ---- 布局参数 ----
const svgWidth = ref(window.innerWidth - 100)
const svgHeight = ref(300)
const boxW = ref(120)
const boxH = 46
const rowGap = 100
const step = ref(240)
const selectedPath = ref<number | null>(null)

function resizeLayout() {
  const available = window.innerWidth - 100
  const maxLen = Math.max(...paths.value.map((p) => p.length))
  step.value = 180  // 每轮固定间距
  boxW.value = 120  // 固定宽度
  svgWidth.value = Math.max(maxLen * step.value, available)
  svgHeight.value = paths.value.length * rowGap + 120
}


function selectPath(index: number) {
  selectedPath.value = selectedPath.value === index ? null : index
}

/* ✅ 累计概率（自动相乘） */
function totalProb(idx: number | null): string {
  if (idx === null) return ''
  const probs = paths.value[idx]
    .map((r) => r.prob.match(/1\/(\d+)/)?.[1])
    .filter(Boolean)
    .map(Number)
  if (probs.length === 0) return '1'
  const total = probs.reduce((a, b) => a * b, 1)
  return `1/${total}`
}

onMounted(() => {
  resizeLayout()
  window.addEventListener('resize', resizeLayout)
})
onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeLayout)
})

function getX(i: number) {
  return i * step.value
}
function getY(pathIndex: number) {
  return 60 + pathIndex * rowGap
}
</script>

<style scoped>
.diff-path {
  width: 100%;
  overflow-x: auto;
  background: #fafafa;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  box-shadow: inset 0 0 6px #eee;
  user-select: none;
}

.title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.summary {
  margin: 6px 0 12px;
  font-size: 13px;
  color: #555;
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
</style>

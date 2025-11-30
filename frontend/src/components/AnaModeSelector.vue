<template>
  <div class="analysis-mode">
    <!-- 三种模式卡片 左中右排列 -->
    <div class="mode-select-container">
      <div class="mode-select">
        <div
          v-for="mode in modes"
          :key="mode.key"
          class="mode-card cursor-pointer rounded-xl border p-6 transition-all"
          :class="selectedMode === mode.key ? 'selected' : ''"
          @click="selectMode(mode.key)"
        >
          <div class="flex flex-col items-center gap-2 mb-2">
            <component :is="mode.icon" class="w-8 h-8 text-blue-500" />
            <span class="font-semibold text-center">{{ mode.label }}</span>
          </div>
          <p class="text-sm text-gray-600 text-center">{{ mode.desc }}</p>
        </div>
      </div>
    </div>

    <!-- 当前模式面板 -->
    <transition name="fade">
      <div v-if="selectedMode" class="mode-settings">
        <component
          :is="modeComponents[selectedMode]"
          v-model:modelValue="modeParams[selectedMode]"
        />
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { Cpu, Search, Filter } from 'lucide-vue-next'
import AutoModePanel from './panels/AutoModePanel.vue'
import FixedModePanel from './analysis-modes/FixedModePanel.vue'
import ConstraintModePanel from './analysis-modes/ConstraintModePanel.vue'

const props = defineProps({
  selectedMode: String
})
const emits = defineEmits(['update:selectedMode'])

const selectedMode = ref(props.selectedMode || 'auto')

// 父组件 v-model 联动
watch(selectedMode, (v) => emits('update:selectedMode', v))

function selectMode(key: string) {
  selectedMode.value = key
}

const modes = [
  { key: 'auto', label: '自动机多路线挖掘', desc: '全局扫描多条候选路线。', icon: Cpu },
  { key: 'fixed', label: '固定场景挖掘', desc: '固定输入输出差分条件进行分析。', icon: Search },
  { key: 'constraint', label: '条件约束挖掘', desc: '可限制比特位、轮次或特征汉明重量。', icon: Filter }
]

const modeParams = ref({
  auto: {},
  fixed: { inDiff: '', outDiff: '' },
  constraint: { conditions: [] }
})

const modeComponents = {
  auto: AutoModePanel,
  fixed: FixedModePanel,
  constraint: ConstraintModePanel
}
</script>

<style scoped>
.analysis-mode {
  width: 100%;
}

/* 容器居中，限制最大宽度 */
.mode-select-container {
  display: flex;
  justify-content: center;
  width: 100%;
}

/* 三个卡片等分布局 */
.mode-select {
  display: flex;
  justify-content: space-between;
  align-items: stretch;
  width: 100%;
  max-width: 600px; /* 可根据需要调整 */
  gap: 16px; /* 卡片间距 */
}

/* 卡片基础样式 */
.mode-card {
  flex: 1; /* 等分宽度 */
  min-width: 0; /* 防止内容溢出 */
  min-height: 120px; /* 统一高度 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  transition: all 0.25s ease-in-out;
  border: 2px solid #e5e7eb; /* 默认边框 */
}

/* 鼠标悬浮效果 */
.mode-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

/* 选中样式 */
.mode-card.selected {
  border-color: #3b82f6;
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.15);
  background-color: #eff6ff;
}

/* 渐隐过渡 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.mode-settings {
  margin-top: 24px;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .mode-select {
    flex-direction: column;
    max-width: 100%;
  }

  .mode-card {
    min-height: 100px;
  }
}
</style>

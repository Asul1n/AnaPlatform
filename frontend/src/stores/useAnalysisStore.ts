// src/stores/useAnalysisStore.ts
import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'

/* 定义算法基本参数类型 */
export interface BasicAlgorithmParams {
  algorithmName: string;
  blockSize: number;
  branchNum: number;
  roundFunction: string;
  roundNum: number;
  note: string;
}

/* 定义视图结构 */
export interface GraphSnapshot {
  nodes: any[];
  edges: any[];
  // 可以添加其他视图信息，如缩放、平移位置
}

export const useAnalysisStore = defineStore('analysis', () => {
  // 🧭 当前中间区域显示内容（画布 / 参数输入）
  const activeTab = ref<'canvas' | 'params'>('canvas')

  // 🧩 基本参数（算法输入区）
  const basicParams = reactive({
    algorithmName: '未命名算法',
    blockSize: 64, // 默认值
    branchNum: 4,   // 默认值
    roundFunction: 'F(x) = ...', 
    roundNum: 0,     
    note: '',
  })

  const lastRoundFunctionSnapshot = ref<GraphSnapshot | null>(null)
  const isLastRoundDifferent = ref(false)

  // 储存快照
  const savedSnapshots = reactive<Record<string, GraphSnapshot>>({})

  // 保存快照
  function saveSnapshot(key: string, snapshot: GraphSnapshot) {
    savedSnapshots[key] = snapshot;
  }

  // 加载快照
  function loadSnapshot(key: string) {
    return savedSnapshots[key];
  }

  // 🧠 设置参数
  function setBasicParams(params: Partial<typeof basicParams>) {
    Object.assign(basicParams, params)
  }

  // 🧩 设置当前显示的界面
  function setActiveTab(tab: 'canvas' | 'params') {
    activeTab.value = tab
  }

  // 📦 导出为 JSON
  function exportConfig() {
    return JSON.parse(JSON.stringify(basicParams))
  }

  return {
    // 状态
    activeTab,
    basicParams,
    savedSnapshots,
    lastRoundFunctionSnapshot,
    isLastRoundDifferent,

    // 方法
    setActiveTab,
    setBasicParams,
    exportConfig,
    saveSnapshot,
    loadSnapshot
  }
})

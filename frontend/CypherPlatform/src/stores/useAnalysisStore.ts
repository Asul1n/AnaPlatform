// src/stores/useAnalysisStore.ts
import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'

export const useAnalysisStore = defineStore('analysis', () => {
  // 🧭 当前中间区域显示内容（画布 / 参数输入）
  const activeTab = ref<'canvas' | 'params'>('canvas')

  // 🧩 基本参数（算法输入区）
  const basicParams = reactive({
    algorithmName: 'MyCipher', // 算法名称
    blockSize: 64,             // 分组长度
    branchNum: 4,              // 分支数
    roundNum: 10,              // 轮数
    mode: 'differential',      // 分析模式：differential | linear | conditional
    description: '',           // 算法简要说明
  })

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

    // 方法
    setActiveTab,
    setBasicParams,
    exportConfig,
  }
})

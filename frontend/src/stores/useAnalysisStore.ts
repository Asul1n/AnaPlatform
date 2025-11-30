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

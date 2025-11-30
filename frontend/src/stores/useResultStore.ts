// src/stores/useResultStore.ts

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { AnalysisResult } from "@/types/analysis"
export const useResultStore = defineStore('resultStore', () => {
    // 存储所有历史和当前结果
    const resultsArchive = ref<AnalysisResult[]>([])
    
    // 当前在结果展示页面中激活的结果 ID
    const activeResultId = ref<string | null>(null)

    // 计算属性：当前激活的结果对象
    const activeResult = computed(() => {
        return resultsArchive.value.find(r => r.resultId === activeResultId.value) || null
    })

    /**
     * 归档新的分析结果
     * @param result 完整的分析结果对象
     */
    function saveResult(result: AnalysisResult) {
        resultsArchive.value.push(result)
        // 默认激活最新结果
        activeResultId.value = result.resultId
    }
    
    /**
     * 切换当前激活的结果
     */
    function setActiveResult(id: string) {
        activeResultId.value = id
    }

    /**
     * 假设后端计算成功后，调用此函数将结果存入 Store
     * @param mode 当前的分析模式
     * @param graphSnapshot 图结构快照
     * @param rawData 后端返回的差分路径和聚合数据
     */
    function archiveNewAnalysis(mode: string, basicParams: any, graphSnapshot: any, rawData: { diffPaths: any[], aggregatedResult: any }) {
        const newResult: AnalysisResult = {
            resultId: `res-${Date.now()}`,
            timestamp: Date.now(),
            mode: mode as any, // 确保类型匹配
            basicParams,
            graphSnapshot,
            diffPaths: rawData.diffPaths,
            aggregatedResult: rawData.aggregatedResult,
            // 默认布局
            layout: { 
                displayType: 'PathList',
                config: { sortBy: 'cost', order: 'desc' } 
            }
        }
        saveResult(newResult)
    }

    function clearResults() {
        if (confirm('确定清空所有分析历史记录吗？')) {
            resultsArchive.value = [];
            activeResultId.value = null;
        }
    }

    return {
        resultsArchive,
        activeResultId,
        activeResult,
        saveResult,
        setActiveResult,
        archiveNewAnalysis,
        clearResults
    }
})
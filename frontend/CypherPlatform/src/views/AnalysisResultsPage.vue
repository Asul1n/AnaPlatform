<template>
    <div class="results-page-layout">
        <aside class="results-sidebar">
            <h3>📜 分析历史</h3>
            <ul class="results-list">
                <li 
                    v-for="res in resultStore.resultsArchive" 
                    :key="res.resultId"
                    :class="{ active: res.resultId === resultId }"
                    @click="switchToResult(res.resultId)" >
                    </li>
            </ul>
        </aside>

        <main class="results-content">
            <el-button 
                type="info" 
                link 
                class="exit-results-btn"
                @click="router.push({ name: 'Editor' })"
            >
                ← 返回画布
            </el-button>

            <div v-if="currentResult">
                <component 
                    :is="resolveResultComponent(currentResult.layout.displayType)"
                    :result-data="currentResult"
                    :key="resultId"
                />
            </div>
            <div v-else class="empty-state">
                <el-empty description="无法找到该分析结果" />
            </div>
        </main>
    </div>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useResultStore } from '@/stores/useResultStore';
// ... 导入 resolveResultComponent 等辅助函数

const props = defineProps<{
    resultId: string; // 从路由接收的参数
}>();

const resultStore = useResultStore();
const router = useRouter();

// 核心逻辑：计算当前激活的结果对象
const currentResult = computed(() => {
    return resultStore.resultsArchive.find(r => r.resultId === props.resultId);
});

// 监听路由参数变化，并同步 Store 的 activeResultId (可选，但推荐)
watch(() => props.resultId, (newId) => {
    if (newId) {
        resultStore.setActiveResult(newId); // 更新 Store 中的当前激活状态
    }
}, { immediate: true });

// 切换结果时，使用路由跳转
function switchToResult(id: string) {
    router.push({ name: 'AnalysisResults', params: { resultId: id } });
}
</script>
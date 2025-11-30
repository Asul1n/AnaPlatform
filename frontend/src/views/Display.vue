<template>
  <div class="results-layout">
    <aside class="results-sidebar">
      <h3>📜 分析历史</h3>
      <p class="sidebar-tip">（点击切换结果快照）</p>
      
      <ul class="results-list">
        <li 
          v-for="res in resultStore.resultsArchive" 
          :key="res.resultId"
          :class="{ active: res.resultId === resultStore.activeResultId }"
          @click="resultStore.setActiveResult(res.resultId)"
        >
          <div class="result-info">
            <span class="mode-tag">{{ modeLabel[res.mode] || res.mode }}</span>
            <small>{{ formatTimestamp(res.timestamp) }}</small>
          </div>
          <el-icon v-if="res.resultId === resultStore.activeResultId">
            <Check />
          </el-icon>
        </li>
      </ul>
      
      <el-button 
        v-if="resultStore.resultsArchive.length > 0"
        type="danger" 
        link 
        @click="resultStore.clearResults"
        class="clear-btn"
      >
        清空历史
      </el-button>
    </aside>

    <main class="results-content">
      <div v-if="resultStore.activeResult">
        <header class="content-header">
          <h2>📊 结果详情：{{ modeLabel[resultStore.activeResult.mode] }}</h2>
          <p>
            分析时间：{{ new Date(resultStore.activeResult.timestamp).toLocaleString() }}
          </p>
          <el-tag size="small" type="info">ID: {{ resultStore.activeResult.resultId.slice(-4) }}</el-tag>
        </header>

        <div class="result-display-area">
          <component 
            :is="resolveResultComponent(resultStore.activeResult.layout.displayType)"
            :result-data="resultStore.activeResult"
            :key="resultStore.activeResultId" />
        </div>

      </div>
      <div v-else class="empty-state">
        <el-empty description="请先运行分析以查看结果" />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useResultStore } from '@/stores/useResultStore';
import { resolveResultComponent } from '@/config/resultComponentMap';
import { Check } from '@element-plus/icons-vue';
// 引入 Element Plus 的样式以便正确渲染，如果您的项目已全局引入则忽略

const resultStore = useResultStore();

// 模式标签映射（为了更好的显示效果）
const modeLabel = {
    auto: '自动聚合模式',
    fixed: '固定分支模式',
    constraint: '受限分析模式',
};

/**
 * 辅助函数：格式化时间戳 (例如：Today 11:05 AM)
 */
function formatTimestamp(timestamp: number): string {
    const date = new Date(timestamp);
    const now = new Date();
    
    const isToday = date.toDateString() === now.toDateString();
    
    if (isToday) {
        return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    }
    
    const isYesterday = new Date(now.setDate(now.getDate() - 1)).toDateString() === date.toDateString();

    if (isYesterday) {
        return '昨天 ' + date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    }

    return date.toLocaleDateString('zh-CN'); // 否则显示日期
}

</script>

<style scoped>
/* 结果页面的基本布局样式，建议放入 editor_layout.scss 或单独的 style 文件 */
.results-layout {
    display: flex;
    height: 100%;
    width: 100%;
    background-color: var(--el-bg-color-page);
    position: absolute; /* 因为它在 VueFlow 上层 */
    z-index: 10;
    top: 0;
    left: 0;
}

.results-sidebar {
    width: 250px;
    padding: 20px 10px;
    background-color: var(--el-bg-color);
    border-right: 1px solid var(--el-border-color-light);
    display: flex;
    flex-direction: column;
}

.sidebar-tip {
    font-size: 0.8em;
    color: var(--el-text-color-secondary);
    margin-bottom: 15px;
    padding: 0 10px;
}

.results-list {
    list-style: none;
    padding: 0;
    margin: 0;
    overflow-y: auto;
    flex-grow: 1;
}

.results-list li {
    padding: 10px;
    border-radius: 4px;
    cursor: pointer;
    margin-bottom: 5px;
    transition: background-color 0.2s;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.results-list li:hover {
    background-color: var(--el-fill-color-light);
}

.results-list li.active {
    background-color: var(--el-color-primary-light-9);
    color: var(--el-color-primary);
    border-left: 3px solid var(--el-color-primary);
    font-weight: bold;
}

.mode-tag {
    font-weight: bold;
    margin-right: 10px;
}

.results-content {
    flex-grow: 1;
    padding: 20px;
    overflow-y: auto;
}

.content-header {
    border-bottom: 1px dashed var(--el-border-color-lighter);
    padding-bottom: 15px;
    margin-bottom: 20px;
}

.result-display-area {
    /* 结果组件的容器 */
}

.empty-state {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80%;
}
.clear-btn {
    margin-top: 15px;
    text-align: center;
}
</style>
<template>
  <div class="snapshot-manager">
    <el-tabs type="border-card">
        <el-tab-pane label="💾 已存快照">
            <el-empty v-if="!hasSnapshots" description="暂无快照"></el-empty>
            <div v-else class="snapshot-list"> <el-card 
                    v-for="(snapshot, key) in analysisStore.savedSnapshots" 
                    :key="key" 
                    shadow="hover"
                    class="snapshot-item"
                >
                    <span>{{ key }}</span>
                    <el-button-group>
                        <el-button size="small" type="primary" @click="$emit('loadSnapshot', key)">加载</el-button>
                        <el-button size="small" type="danger" @click="$emit('deleteSnapshot', key)">删除</el-button>
                    </el-button-group>
                </el-card>
            </div>
        </el-tab-pane>

        <el-tab-pane label="🔄 最后一轮函数">
            <el-alert
                v-if="analysisStore.isLastRoundDifferent"
                title="已保存特殊最后一轮配置"
                type="success"
                :description="`节点数: ${analysisStore.lastRoundFunctionSnapshot?.nodes.length || 0} 个`"
                show-icon
                :closable="false"
            />
            <el-empty v-else description="尚未保存特殊最后一轮结构"></el-empty>

            <div style="margin-top: 15px;">
                <el-button 
                    type="primary" 
                    :disabled="!analysisStore.isLastRoundDifferent"
                    @click="$emit('loadLastRound')"
                >
                    加载到画布 (编辑)
                </el-button>
                <el-button 
                    type="danger" 
                    :disabled="!analysisStore.isLastRoundDifferent"
                    @click="$emit('clearLastRound')"
                >
                    清除配置
                </el-button>
            </div>
        </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAnalysisStore } from '@/stores/useAnalysisStore'
// 【修正】移除 ElList 和 ElListItem
import { 
    ElTabs, 
    ElTabPane, 
    ElEmpty, 
    ElButton, 
    ElButtonGroup, 
    ElAlert,
    ElCard // <-- 引入 ElCard 用于列表项包装
} from 'element-plus'

const analysisStore = useAnalysisStore()

const hasSnapshots = computed(() => Object.keys(analysisStore.savedSnapshots).length > 0)

defineEmits<{
  (e: 'loadSnapshot', key: string): void
  (e: 'deleteSnapshot', key: string): void
  (e: 'loadLastRound'): void
  (e: 'clearLastRound'): void
}>()
</script>

<style scoped>
/* 确保列表项分隔清晰，并使用 flex 布局 */
.snapshot-list {
    display: flex;
    flex-direction: column;
    gap: 10px; /* 列表项之间的间距 */
    max-height: 300px; /* 限制列表高度，防止溢出 */
    overflow-y: auto;
}

.snapshot-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 15px;
    /* 覆盖 ElCard 默认的 padding */
    --el-card-padding: 10px; 
}

.snapshot-info {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.node-count {
    font-size: 0.8em;
    color: #909399; /* 灰色提示文字 */
    margin-top: 2px;
}
</style>
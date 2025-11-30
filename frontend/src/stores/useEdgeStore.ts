import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Edge as VfEdge } from '@vue-flow/core'
import { useExportGraph } from '@/composables/useExportGraph'


export const useEdgeStore = defineStore('edgeStore', () => {
    const { exportGraph } = useExportGraph()

    const edges = ref<VfEdge[]>([])              // 所有边
    const selectedEdgeIds = ref<string[]>([])    // 选中的边

    /* 获取选中边对象 */
    const selectedEdges = computed(() =>
        edges.value.filter(e => selectedEdgeIds.value.includes(e.id))
    )
    
    /* 添加一条边 */
    function addEdge(edge: VfEdge) {
        edges.value.push(edge)
    }

    /* 删除边（可单条，也可批量） */
    function removeEdges(ids: string[] | string) {
        const idSet = new Set(Array.isArray(ids) ? ids : [ids])
        edges.value = edges.value.filter(e => !idSet.has(e.id))
    }

    /* 删除节点相关边 */
    function removeNodeEdges(nodeId: string) {
        edges.value = edges.value.filter(e => e.source !== nodeId && e.target !== nodeId)
    }

    /* 清空所有边 */
    function clearEdges() {
        edges.value = []
    }

    /* 根据 VueFlow edgeChange 事件同步 */
    function onEdgesChange(changes: { type: string, id: string, item?: VfEdge }[]) {
        changes.forEach(change => {
        switch (change.type) {
            case 'add':
            if (change.item) addEdge(change.item)
            break
            case 'remove':
            removeEdges(change.id)
            break
        }
        })
    }

    function onExportClick() {
        const json = exportGraph()
        console.log(json)
    }




    return {
        edges,
        selectedEdgeIds,
        selectedEdges,
        addEdge,
        removeEdges,
        removeNodeEdges,
        clearEdges,
        onEdgesChange,
        onExportClick
    }

})
// src/composables/useGraphStateManager.ts

import { useAnalysisStore, type GraphSnapshot } from "@/stores/useAnalysisStore";
import { useNodeStore } from "@/stores/useNodeStore";
import { useEdgeStore } from "@/stores/useEdgeStore";
import { useUIStore } from "@/stores/useUIStore";
import { useExportGraph } from "./useExportGraph";

export function useGraphStateManager() {
    const analysisStore = useAnalysisStore();
    const nodeStore = useNodeStore();
    const edgeStore = useEdgeStore();
    const ui = useUIStore();
    const { exportGraph } = useExportGraph();

    // --- 辅助函数：将快照数据加载到画布 ---
    function _loadSnapshotToCanvas(snapshot: GraphSnapshot) {
        // 1. 清空当前画布 (使用 splice 变异，保持数组引用不变)
        nodeStore.nodes.splice(0, nodeStore.nodes.length);
        edgeStore.edges.splice(0, edgeStore.edges.length);

        // 2. 加载快照数据 (深度复制并使用 push 变异)
        const newNodes = JSON.parse(JSON.stringify(snapshot.nodes));
        const newEdges = JSON.parse(JSON.stringify(snapshot.edges));

        nodeStore.nodes.push(...newNodes);
        edgeStore.edges.push(...newEdges);
    }

    // --- 1. 保存快照 ---
    function onSaveSnapshot() {
        // 1. 获取当前画布的结构数据
        const exportedData = exportGraph(); 

        const snapshot: GraphSnapshot = {
            nodes: exportedData.roundFunction.nodes,
            edges: exportedData.roundFunction.edges,
        };

        // 2. 存储到 Store
        const snapshotName = prompt('请输入快照名称:', `Snapshot_${Date.now()}`);
        if (snapshotName) {
            analysisStore.saveSnapshot(snapshotName, snapshot);
            ui.toggleSnapshotPanel(); // 保存后打开面板方便查看
            alert(`状态 "${snapshotName}" 已保存！`);
        }
    }

    // --- 2. 加载快照 ---
    function onLoadSnapshot(key: string) {
        const snapshot = analysisStore.loadSnapshot(key);
        if (snapshot && confirm(`确定加载快照 "${key}" 吗？当前画布将被覆盖！`)) {
            _loadSnapshotToCanvas(snapshot);
            ui.toggleSnapshotPanel(); // 加载后关闭面板
            alert(`快照 "${key}" 已加载！`);
        }
    }

    // --- 3. 删除快照 ---
    function onDeleteSnapshot(key: string) {
        if (confirm(`确定删除快照 "${key}" 吗？`)) {
            delete analysisStore.savedSnapshots[key];
        }
    }

    // --- 4. 保存为最后一轮函数 ---
    function onSaveLastRound() {
        if (nodeStore.nodes.length === 0) {
            alert('画布为空，无法保存为特殊轮函数！请先搭建结构。');
            return;
        }

        // 1. 获取当前画布的结构数据
        const exportedData = exportGraph();
        const snapshot: GraphSnapshot = {
            nodes: exportedData.roundFunction.nodes,
            edges: exportedData.roundFunction.edges,
        };

        // 2. 存储到指定的字段
        analysisStore.lastRoundFunctionSnapshot = snapshot;
        analysisStore.isLastRoundDifferent = true;
        
        alert('当前画布结构已保存为特殊的“最后一轮轮函数”。');
    }

    // --- 5. 加载特殊最后一轮函数 ---
    function onLoadLastRound() {
        const snapshot = analysisStore.lastRoundFunctionSnapshot;
        if (snapshot) {
            if (confirm("确定要加载 '特殊最后一轮函数' 到画布吗？当前画布将被覆盖！")) {
                _loadSnapshotToCanvas(snapshot);
                ui.toggleSnapshotPanel();
                alert('特殊最后一轮函数结构已加载！');
            }
        } else {
            alert('没有保存的特殊最后一轮函数。');
        }
    }

    // --- 6. 清除特殊最后一轮函数配置 ---
    function onClearLastRound() {
        if (confirm("确定要清除保存的 '特殊最后一轮函数' 配置吗？")) {
            analysisStore.lastRoundFunctionSnapshot = null;
            analysisStore.isLastRoundDifferent = false;
            alert('特殊最后一轮函数配置已清除。');
        }
    }

    return {
        onSaveSnapshot,
        onLoadSnapshot,
        onDeleteSnapshot,
        onSaveLastRound,
        onLoadLastRound,
        onClearLastRound,
    };
}
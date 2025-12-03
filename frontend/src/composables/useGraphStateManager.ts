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
        const newNodes = JSON.parse(JSON.stringify(snapshot.nodes)).map(node => {
            // 🌟 容错处理：确保至少有 position 和 type
            if (!node.position) {
                console.warn(`节点 ${node.id} 缺少位置信息，使用默认位置。`);
                node.position = { x: 50, y: 50 }; // 设置默认位置
            }
            if (!node.type) {
                console.error(`节点 ${node.id} 缺少 type 属性，无法渲染！`);
            }
            // 确保 data 对象存在，即使它在保存时被优化掉了
            if (!node.data) {
                node.data = {};
            }
            
            return node;
        });
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
            analysisStore.addSnapshot(snapshotName, snapshot);
            ui.toggleSnapshotPanel(); // 保存后打开面板方便查看
            alert(`状态 "${snapshotName}" 已保存并持久化！`);
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
    function onDeleteSnapshot(name: string) {
        if (confirm(`确定删除快照 "${name}" 吗？`)) {
            analysisStore.deleteSnapshot(name); 
            alert(`快照 "${name}" 已删除并从本地存储中移除!`);
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
        analysisStore.setLastRound(snapshot);
        analysisStore.isLastRoundDifferent = true;
        
        alert('最后一轮函数已保存并持久化!');
    }

    // --- 5. 加载特殊最后一轮函数 ---
    function onLoadLastRound() {
        const snapshot = analysisStore.lastRoundSnapshot;
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
            analysisStore.clearLastRound();
            analysisStore.isLastRoundDifferent = false;
            alert('最后一轮函数已清除并从本地存储中移除!');
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
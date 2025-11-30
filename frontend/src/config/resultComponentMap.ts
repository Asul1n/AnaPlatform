// // src/config/resultComponentMap.ts (新增文件)
// import PathListDisplay from '@/components/results/PathListDisplay.vue';
// // 假设您有其他展示组件，例如热力图和拓扑图
// import HeatmapDisplay from '@/components/results/HeatmapDisplay.vue'; 
// import TopologyDisplay from '@/components/results/TopologyDisplay.vue';
import DiffPathDisplay from "@/views/DiffPathDisplay.vue";
// 映射表：将 ResultLayout.displayType 字符串映射到实际的 Vue 组件
export const resultComponentMap: Record<string, any> = {
    // PathList: PathListDisplay,
    // Heatmap: HeatmapDisplay,
    // Topology: TopologyDisplay,
    DiffPath: DiffPathDisplay
    // ... 可以继续添加其他结果展示类型
};

/**
 * 根据 displayType 字符串解析对应的 Vue 组件
 * @param type 
 * @returns Vue 组件或 null
 */
export function resolveResultComponent(type: string): any {
    return resultComponentMap[type] || null;
}
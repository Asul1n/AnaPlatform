// src/types/analysis.ts

/** 定义结果数据的通用接口 */
interface AnalysisResult {
  // 核心标识信息
  resultId: string;           // 唯一的 ID，用于缓存和 URL
  timestamp: number;          // 分析运行时间

  // 溯源信息 (用于识别配置)
  mode: 'auto' | 'fixed' | 'constraint'; // 分析模式
  basicParams: any;           // 运行时的基本参数快照 (轮数, 分支数等)
  graphSnapshot: any;         // 运行时的图结构快照 (节点和边)

  // 实际结果数据
  diffPaths: any[];           // 差分路径列表 (DiffPathDisplay 组件需要的数据)
  aggregatedResult: any;      // 聚合结果数据 (例如：最终复杂度估计)

  // 布局信息
  layout: ResultLayout;       // 针对该结果集的布局配置（见下方）
}

/** 布局配置：如果需要自定义结果展示页面的布局 */
interface ResultLayout {
    displayType: 'PathList' | 'Heatmap' | 'Topology', // 结果组件的选择
    config: any // 传给该展示组件的配置，例如排序方式
}
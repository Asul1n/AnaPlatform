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

/* 定义视图结构 */
export interface GraphSnapshot {
  nodes: any[];
  edges: any[];
  // 可以添加其他视图信息，如缩放、平移位置
}

// 定义 localStorage 的 key
const LOCAL_STORAGE_KEY = 'analysis_tool_snapshots';
const LAST_ROUND_KEY = 'analysis_tool_last_round';

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

  // const lastRoundFunctionSnapshot = ref<GraphSnapshot | null>(null)
  const isLastRoundDifferent = ref(false)

  // 储存快照
  const savedSnapshots = ref<Record<string, GraphSnapshot>>({})
  const lastRoundSnapshot = ref<GraphSnapshot | null>(null)

  function loadSnapshot(key: string) {
    return savedSnapshots.value[key];
  }

  // 从本地加载数据
  function loadFromLocalStorage() {
    try {
        const snapshotsJson = localStorage.getItem(LOCAL_STORAGE_KEY);
        if (snapshotsJson) {
            const parsedSnapshots = JSON.parse(snapshotsJson);
            
            // 🌟 关键：使用 Object.assign 或直接赋值覆盖，确保响应性
            savedSnapshots.value = parsedSnapshots;
            
            // 调试输出，检查加载结果
            console.log("快照已加载:", Object.keys(savedSnapshots.value).length, "个");
        }
        
        const lastRoundJson = localStorage.getItem(LAST_ROUND_KEY);
        if (lastRoundJson) {
            const parsedLastRound = JSON.parse(lastRoundJson);
            
            // 🌟 关键：直接赋值
            lastRoundSnapshot.value = parsedLastRound;
            
            // 🌟 关键：如果加载了特殊轮函数，则将 isLastRoundDifferent 设为 true
            isLastRoundDifferent.value = true;
            
            // 调试输出
            console.log("特殊最后一轮已加载:", !!lastRoundSnapshot.value);
        }
    } catch (e) {
        console.error("Error loading analysis state from localStorage:", e);
        // 失败时清空或保持默认值
        savedSnapshots.value = {};
        lastRoundSnapshot.value = null;
    }
  }

  // 保存快照到本地
  function persistSnapshots() {
    try {
        const jsonString = JSON.stringify(savedSnapshots.value);
        
        // 🌟 1. 检查序列化后的字符串是否为空或无效
        console.log('快照序列化结果:', jsonString.length > 50 ? jsonString.substring(0, 50) + '...' : jsonString);

        localStorage.setItem(LOCAL_STORAGE_KEY, jsonString);
        
        // 🌟 2. 检查写入后是否能立即读取（验证写入是否成功）
        console.log('LocalStorage 写入成功，验证读取:', localStorage.getItem(LOCAL_STORAGE_KEY));

    } catch (e) {
        // 🌟 3. 如果 JSON.stringify 失败，错误会在这里捕获
        console.error("Error saving snapshots to localStorage (可能是循环引用!):", e);
    }
  }

  // 保存最后一轮函数到本地
  function persistLastRound() {
      try {
          localStorage.setItem(LAST_ROUND_KEY, JSON.stringify(lastRoundSnapshot.value));
      } catch (e) {
          console.error("Error saving last round to localStorage:", e);
      }
  }

  // 示例：保存快照的 action (假设在你的 store 中)
  function addSnapshot(name: string, snapshot: GraphSnapshot) {
      savedSnapshots.value[name] = snapshot;
      persistSnapshots(); // 立即保存
  }
  
  // 示例：删除快照的 action
  function deleteSnapshot(name: string) {
      delete savedSnapshots.value[name];
      persistSnapshots(); // 立即保存
  }

  // 示例：设置最后一轮的 action
  function setLastRound(snapshot: GraphSnapshot) {
      lastRoundSnapshot.value = snapshot;
      persistLastRound(); // 立即保存
  }
  
  // 示例：清除最后一轮的 action
  function clearLastRound() {
      lastRoundSnapshot.value = null;
      persistLastRound(); // 立即保存
  }

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
    savedSnapshots,
    lastRoundSnapshot, // ⚠️ 之前返回的是 lastRoundFunctionSnapshot，这里应返回 lastRoundSnapshot
    isLastRoundDifferent,

    // 方法
    setActiveTab,
    setBasicParams,
    exportConfig,
    
    // 暴露快照和持久化相关方法 (核心修改)
    addSnapshot,        // 外部用于保存快照 (会自动调用持久化)
    deleteSnapshot,     // 外部用于删除快照 (会自动调用持久化)
    setLastRound,       // 外部用于设置最后一轮函数 (会自动调用持久化)
    clearLastRound,     // 外部用于清除最后一轮函数 (会自动调用持久化)
    loadFromLocalStorage, // 外部用于应用启动时加载数据
    loadSnapshot,

  }
})

import axios from 'axios'
import type { GraphData } from '@/composables/useExportGraph'

// ⚠️ 根据你的实际后端地址进行配置
const API_BASE_URL = 'http://localhost:8080/api'; 

// 创建一个 Axios 实例，用于集中管理配置
const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 300000, // 5分钟超时
    headers: {
        'Content-Type': 'application/json',
    }
});

/**
 * 调用后端分析服务
 * @param graphData 完整的图结构 JSON 数据
 * @returns 后端返回的分析结果数据
 */
export async function runAnalysisService(graphData: GraphData): Promise<any> {
    const endpoint = '/run-analysis'; // 完整的 URL 是 http://localhost:8080/api/run-analysis
    
    try {
        const response = await api.post(endpoint, graphData);
        // 返回后端响应的数据部分
        return response.data; 
    } catch (error) {
        // 集中处理 API 错误，例如日志记录或转换为更友好的应用错误
        console.error("Analysis API 调用失败:", error);
        // 重新抛出错误，以便 Store 可以捕获并处理 UI 状态
        throw error; 
    }
}
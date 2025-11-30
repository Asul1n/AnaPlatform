// src/api/diffPath.ts
import request from './index'

export interface DiffPathsResponse {
  paths: DiffPath[]
  total_probability: number
}

// 获取所有差分路径
export function fetchDiffPaths() {
  return request.get<DiffPathsResponse>('/diff-paths')
}


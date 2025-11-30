// src/api/index.ts
import axios from 'axios'

// ✅ 创建 axios 实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000', // FastAPI 地址
  timeout: 8000,
})

// ✅ 请求拦截器：自动附加 token
service.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {  
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// ✅ 响应拦截器：统一错误处理
service.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const status = error.response?.status
    if (status === 401) {
      console.warn('⚠️ 登录过期，请重新登录')
      localStorage.removeItem('token')
      window.location.href = '/login'
    } else {
      console.error(`❌ 请求错误 (${status}):`, error.response?.data || error.message)
    }
    return Promise.reject(error)
  }
)

export default service


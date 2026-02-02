//Axios 封装 (src/utils/request.ts)

import axios, {
  type InternalAxiosRequestConfig,
  type AxiosResponse,
  type AxiosError,
  type AxiosRequestConfig
} from 'axios'
import { ElMessage } from 'element-plus'
import Cookies from 'js-cookie' // 直接从Cookie读取Token

interface ErrorResponseData {
  detail?: string;
  [key: string]: any;
}

const service = axios.create({
  baseURL: '/',
  timeout: 3600000,
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  }
})

// 请求拦截器：直接从Cookie读Token（避免Pinia依赖问题）
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = Cookies.get('token') // 从Cookie读取
    if (token) {
      config.headers = config.headers || {}
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: AxiosError) => {
    ElMessage.error(error.message || '请求异常')
    return Promise.reject(error)
  }
)

// 响应拦截器：直接返回data
service.interceptors.response.use(
  (response: AxiosResponse) => response.data,
  (error: AxiosError<ErrorResponseData>) => {
    const msg = error.response?.data?.detail || error.message || '请求失败'
    ElMessage.error(msg)
    return Promise.reject(error)
  }
)

// =================================================
// ✅ 关键：类型层封装（这才是 TS 的核心）
// =================================================
const request = <T = any>(config: AxiosRequestConfig): Promise<T> => {
  return service(config) as Promise<T>
}

export default request
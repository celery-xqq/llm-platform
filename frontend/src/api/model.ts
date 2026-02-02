// src/api/model.ts
import request from '@/utils/request'

// 获取模型列表
export const getModels = () => {
  return request({
    url: '/api/v1/llm-models/',
    method: 'get'
  })
}

// 创建模型
export const createModel = (data: any) => {
  return request({
    url: '/api/v1/llm-models/',
    method: 'post',
    data
  })
}

// 获取单个模型
export const getModelDetail = (id: string | number) => {
  return request({
    url: `/api/v1/llm-models/${id}`,
    method: 'get'
  })
}

// 更新模型
export const updateModel = (id: string | number, data: any) => {
  return request({
    url: `/api/v1/llm-models/${id}`,
    method: 'put',
    data
  })
}

// 删除模型
export const deleteModel = (id: string | number) => {
  return request({
    url: `/api/v1/llm-models/${id}`,
    method: 'delete'
  })
}

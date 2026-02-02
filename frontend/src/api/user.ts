// src/api/user.ts
import request from '@/utils/request'

// 获取用户列表
export const getUsers = () => {
  return request({
    url: '/api/v1/users/',
    method: 'get'
  })
}

// 创建用户
export const createUser = (data: any) => {
  return request({
    url: '/api/v1/auth/create-user',
    method: 'post',
    data
  })
}

// 删除用户
export const deleteUser = (id: string) => {
  return request({
    url: `/api/v1/users/${id}`,
    method: 'delete'
  })
}
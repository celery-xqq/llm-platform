// 登录接口 (src/api/auth.ts)

import request from '@/utils/request'
import type { LoginResponse, LoginRequest } from '@/types/auth'

export const login = (data: LoginRequest): Promise<LoginResponse> => {
  return request({
    url: '/api/v1/auth/login',
    method: 'post',
    data
  })
}





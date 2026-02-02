// 类型定义 (src/types/auth.ts)

export interface User {
  id: string
  username: string
  is_admin: boolean
  is_active: boolean
}

export interface LoginResponse {
  access_token: string
  user: User
}

export interface LoginRequest {
  username: string
  password: string
}

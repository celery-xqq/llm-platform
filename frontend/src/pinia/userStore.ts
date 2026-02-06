// Pinia 用户 Store (src/pinia/userStore.ts)
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login } from '@/api/auth'
import { ElMessage } from 'element-plus'
import router from '@/router'
import Cookies from 'js-cookie'

export const useUserStore = defineStore('user', () => {
  // 状态：初始化时从Cookie读取Token和用户名
  const token = ref<string>(Cookies.get('token') || '')
  const userInfo = ref<any>({
    username: Cookies.get('username') || '', // 从Cookie读取用户名，兜底为空
    is_admin: Cookies.get('is_admin') === 'true' || false // 从Cookie读取，默认false
  })

  // 登录操作：调用后端登录接口，成功后更新状态和Cookie
  const loginAction = async (username: string, password: string) => {
    try {
      const res = await login({ username, password })
      if (!res.access_token) {
        throw new Error('登录接口未返回Token')
      }
      token.value = res.access_token
      // 保存Token和用户名到Cookie（核心修改）
      Cookies.set('token', token.value, { expires: 1 })
      Cookies.set('username', username, { expires: 1 }) // 存储登录用户名
      Cookies.set('is_admin', String(res.user.is_admin), { expires: 1 }) // 存储管理员状态
      
      // 同步到状态：用后端返回的真实权限
      userInfo.value.username = res.user.username
      userInfo.value.is_admin = res.user.is_admin
      
      ElMessage.success('登录成功')
      router.push('/dashboard')
    } catch (error) {
      ElMessage.error('登录失败，请检查账号密码')
      throw error
    }
  }

  // 退出登录：清空Cookie中的用户名（核心修改）
  const logoutAction = () => {
    token.value = ''
    userInfo.value = { username: '', is_admin: false }
    Cookies.remove('token')
    Cookies.remove('username') // 清空用户名Cookie
    Cookies.remove('is_admin') // 清空管理员状态Cookie
    router.push('/login')
  }

  return {
    token,
    userInfo,
    loginAction,
    logoutAction
  }
})
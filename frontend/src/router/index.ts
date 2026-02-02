// src/router/index.ts

import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router' // 单独导入类型
import { useUserStore } from '@/pinia/userStore'
import Layout from '@/layouts/index.vue'
import { ElMessage } from 'element-plus'

// 静态路由
export const constantRoutes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { hidden: true }
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '首页', icon: 'HomeFilled' }
      }
    ]
  },
  {
    path: '/user',
    component: Layout,
    children: [
      {
        path: 'list',
        name: 'UserList',
        component: () => import('@/views/user/index.vue'),
        meta: { title: '用户管理', icon: 'User', requiresAdmin: true }
      }
    ]
  },
  {
    path: '/chat',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Chat',
        component: () => import('@/views/chat/index.vue'),
        meta: { title: '对话页面', icon: 'ChatDotRound' }
      }
    ]
  },
  {
    path: '/model',
    component: Layout,
    children: [
      {
        path: 'list',
        name: 'ModelList',
        component: () => import('@/views/model/index.vue'),
        meta: { title: '模型管理', icon: 'Setting', requiresAdmin: true } // 仅管理员可见
      }
    ]
  }
]

// 创建路由
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: constantRoutes
})

// 路由守卫：验证登录和权限
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  // 未登录：跳转到登录页
  if (!userStore.token && to.path !== '/login') {
    next('/login')
    return
  }
  // 已登录：禁止访问登录页
  if (userStore.token && to.path === '/login') {
    next('/dashboard')
    return
  }
  // 管理员权限验证
  if (to.meta.requiresAdmin && !userStore.userInfo.is_admin) {
    next('/dashboard')
    ElMessage.error('无管理员权限')
    return
  }
  next()
})

export default router
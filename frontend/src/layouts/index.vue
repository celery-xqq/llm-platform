<!-- 布局 (src/layouts/index.vue) -->
<template>
  <div style="display: flex; height: 100vh; overflow: hidden;">
    <!-- 侧边栏 -->
    <div style="width: 200px; background: #2e3b4e; color: #fff;">
      <el-menu
        default-active="4"
        class="el-menu-vertical-demo"
        background-color="#2e3b4e"
        text-color="#fff"
        active-text-color="#ffd04b"
        router
        style="border-right: none;">
        <el-menu-item index="/dashboard">
          <el-icon><HomeFilled /></el-icon>
          <template #title>首页</template>
        </el-menu-item>
        <el-menu-item index="/user/list" v-if="userStore.userInfo.is_admin">
          <el-icon><User /></el-icon>
          <template #title>用户管理</template>
        </el-menu-item>
        <el-menu-item index="/model/list" v-if="userStore.userInfo.is_admin">
          <el-icon><Setting /></el-icon>
          <template #title>模型管理</template>
        </el-menu-item>
        <el-menu-item index="/chat/index">
          <el-icon><ChatDotRound /></el-icon>
          <template #title>对话页面</template>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 主内容区 -->
    <div style="flex: 1; display: flex; flex-direction: column;">
      <!-- 右上角用户栏（精准点击版） -->
      <div style="height: 60px; display: flex; justify-content: flex-end; align-items: center; padding: 0 20px; border-bottom: 1px solid #f0f0f0; background-color: #ffffff;">
        <!-- 用户信息展示（仅展示，不可点击） -->
        <div style="display: flex; align-items: center; gap: 8px; padding-right: 12px;">
          <el-icon class="user-icon"><UserFilled /></el-icon>
          <span class="username">{{ userStore.userInfo.username || '未知用户' }}</span>
        </div>
        <!-- 退出登录按钮（仅按钮可点击） -->
        <el-button 
          type="text" 
          @click="handleLogout"
          style="color: #666; padding: 4px 12px; border-radius: 4px;"
        >
          <el-icon><SwitchButton /></el-icon>
          退出登录
        </el-button>
      </div>

      <!-- 页面内容 -->
      <div style="flex: 1; padding: 20px; overflow-y: auto; background-color: #f8f9fa;">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/pinia/userStore'
import { ElMenu, ElMenuItem, ElIcon } from 'element-plus'
import { HomeFilled, User, ChatDotRound, Setting, UserFilled, SwitchButton } from '@element-plus/icons-vue'

const userStore = useUserStore()

// 登出逻辑（保留已验证的强制跳转）
const handleLogout = async () => {
  // 清空状态和Cookie
  userStore.token = ''
  userStore.userInfo = {}
  document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  
  // 强制跳转到登录页
  window.location.href = '/login'
}
</script>

<style scoped>
/* 美化退出登录按钮 */
.logout-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  color: #666666;
  font-size: 14px;
  transition: all 0.2s ease;
  border: 1px solid #e0e0e0;
  background-color: #ffffff;
}

.logout-btn:hover {
  background-color: #f5f5f5;
  color: #409eff;
  border-color: #c6e2ff;
}

.logout-btn:active {
  background-color: #e8f4ff;
}

.user-icon {
  color: #409eff;
  font-size: 16px;
}

.username {
  font-weight: 500;
}

.logout-icon {
  font-size: 14px;
}

.logout-text {
  font-size: 13px;
}
</style>
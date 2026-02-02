<!-- dashboard (src/views/dashboard/index.vue) -->
<template>
  <div class="dashboard-container">
    <el-card class="welcome-card">
      <h2>欢迎使用 LLM 对话平台</h2>
      <p class="welcome-desc">
        当前登录用户：{{ userStore.userInfo.username }}
        <el-tag v-if="userStore.userInfo.is_admin" type="success">管理员</el-tag>
        <el-tag v-else type="info">普通用户</el-tag>
      </p>
      <el-divider />
      <div class="dashboard-stats">
        <el-statistic title="平台功能" :value="1" :formatter="() => '已上线'" />
        <el-statistic
          title="当前时间"
          :value="now"
          :formatter="(val: Dayjs) => val.format('YYYY-MM-DD HH:mm:ss')"/>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElCard, ElDivider, ElTag, ElStatistic } from 'element-plus'
import { useUserStore } from '@/pinia/userStore'
import dayjs, { Dayjs } from 'dayjs'

const userStore = useUserStore()
const now = ref<Dayjs>(dayjs()) // 使用 Dayjs 类型

// 更新当前时间
const updateTime = () => {
  now.value = dayjs()
}

onMounted(() => {
  updateTime()
  setInterval(updateTime, 1000)
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.welcome-card {
  max-width: 800px;
  margin: 0 auto;
}

.welcome-title {
  font-size: 24px;
  margin-bottom: 10px;
  color: #1989fa;
}

.welcome-desc {
  font-size: 16px;
  margin: 10px 0;
}

.dashboard-stats {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}
</style>


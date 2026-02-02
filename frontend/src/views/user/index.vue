<!-- user (src/views/user/index.vue) -->
<template>
  <div class="user-container">
    <el-card>
      <div class="user-header">
        <el-button type="primary" @click="openAddUserDialog">新增用户</el-button>
      </div>
      <el-table :data="userList" border style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="300" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="is_admin" label="是否管理员">
          <template #default="scope">
            <el-tag v-if="scope.row.is_admin" type="success">是</el-tag>
            <el-tag v-else type="info">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="是否激活">
          <template #default="scope">
            <el-tag v-if="scope.row.is_active" type="success">是</el-tag>
            <el-tag v-else type="danger">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editUser(scope.row)">编辑</el-button>
            <!-- 禁用admin账号的删除按钮 -->
            <el-button 
              type="danger" 
              size="small" 
              @click="deleteUserAction(scope.row.id)"
              :disabled="scope.row.username === 'admin'">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 新增/编辑用户弹窗 -->
      <el-dialog v-model="dialogVisible" title="新增用户" width="400px">
        <el-form :model="userForm" :rules="userRules" ref="userFormRef" label-width="80px">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="userForm.username" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="userForm.password" type="password" />
          </el-form-item>
          <el-form-item label="是否管理员" prop="is_admin">
            <el-switch v-model="userForm.is_admin" />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitUser">确定</el-button>
        </template>
      </el-dialog>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
// 新增：导入ElMessage
import { ElTable, ElTableColumn, ElButton, ElCard, ElTag, ElDialog, ElForm, ElFormItem, ElInput, ElSwitch, ElMessage } from 'element-plus'
import { getUsers, createUser, deleteUser } from '@/api/user'


const loading = ref(false)
const userList = ref<any[]>([])
const dialogVisible = ref(false)
const userFormRef = ref<any>(null)

// 用户表单
const userForm = reactive({
  username: '',
  password: '',
  is_admin: false
})

// 表单校验规则
const userRules = reactive({
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
})

// 获取用户列表
const getUserList = async () => {
  loading.value = true
  try {
    const res = await getUsers()
    userList.value = res
  } catch (error) {
    console.error('获取用户列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 打开新增用户弹窗
const openAddUserDialog = () => {
  // 重置表单
  userForm.username = ''
  userForm.password = ''
  userForm.is_admin = false
  dialogVisible.value = true
}

// 提交新增用户
const submitUser = async () => {
  if (!userFormRef.value) return
  try {
    await userFormRef.value.validate()
    await createUser(userForm)
    ElMessage.success('新增用户成功')
    dialogVisible.value = false
    getUserList()
  } catch (error) {
    ElMessage.error('新增用户失败')
    console.error(error)
  }
}

// 删除用户
const deleteUserAction = async (id: string) => {
  try {
    await deleteUser(id)
    ElMessage.success('删除用户成功')
    getUserList()
  } catch (error) {
    ElMessage.error('删除用户失败')
    console.error(error)
  }
}

// 编辑用户（暂未实现，可扩展）
const editUser = (row: any) => {
  // 可扩展编辑逻辑
  ElMessage.info('编辑功能暂未实现')
}

// 初始化
onMounted(() => {
  getUserList()
})
</script>

<style scoped>
.user-container {
  padding: 20px;
}
.user-header {
  margin-bottom: 20px;
}
</style>
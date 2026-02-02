<!-- src/views/model/index.vue -->
<template>
  <div class="model-container">
    <el-card>
      <!-- 顶部操作 -->
      <div class="header">
        <h2>模型管理</h2>
        <el-button type="primary" @click="openCreate">新增模型</el-button>
      </div>

      <!-- 模型表格 -->
      <el-table :data="modelList" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="120" />
        <el-table-column prop="name" label="模型名称" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="type" label="类型" width="100" />
        <el-table-column prop="real_model_name" label="真实模型名" />
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag type="success" v-if="scope.row.is_active">启用</el-tag>
            <el-tag type="danger" v-else>停用</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="scope">
            <el-button size="small" type="primary" @click="openEdit(scope.row)">编辑</el-button>
            <el-popconfirm title="确认删除该模型？" @confirm="handleDelete(scope.row.id)">
              <template #reference>
                <el-button size="small" type="danger" style="margin-left: 8px">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增 / 编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑模型' : '新增模型'" width="560px">
      <el-form :model="form" label-width="110px">
        <el-form-item label="模型名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="模型描述"><el-input v-model="form.description" /></el-form-item>
        <el-form-item label="模型类型">
          <el-select v-model="form.type" style="width: 100%">
            <el-option label="OpenAI" value="openai" />
            <el-option label="百度文心" value="baidu" />
            <el-option label="腾讯混元" value="tencent" />
            <el-option label="本地模型" value="local" />
          </el-select>
        </el-form-item>
        <el-form-item label="真实模型名"><el-input v-model="form.real_model_name" /></el-form-item>
        <el-form-item label="Base URL"><el-input v-model="form.base_url" /></el-form-item>
        <el-form-item label="模型 Key">
          <el-input
            v-model="form.model_key"
            type="password"
            placeholder="编辑时留空表示不修改，创建时空则传空字符串"
          />
        </el-form-item>
        <el-form-item label="是否启用"><el-switch v-model="form.is_active" /></el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getModels, createModel, updateModel, deleteModel } from '@/api/model'

const modelList = ref<any[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)

const form = reactive<any>({
  id: '',
  name: '',
  description: '',
  type: 'openai',
  model_key: '',
  base_url: '',
  real_model_name: '',
  is_active: true
})

const resetForm = () => {
  form.id = ''
  form.name = ''
  form.description = ''
  form.type = 'openai'
  form.model_key = ''
  form.base_url = ''
  form.real_model_name = ''
  form.is_active = true
}

// 加载模型列表
const loadModels = async () => {
  loading.value = true
  try {
    modelList.value = await getModels()
  } finally {
    loading.value = false
  }
}

// 新增
const openCreate = () => {
  resetForm()
  isEdit.value = false
  dialogVisible.value = true
}

// 编辑
const openEdit = (row: any) => {
  Object.assign(form, row)
  // 密钥永不回显
  form.model_key = ''
  isEdit.value = true
  dialogVisible.value = true
}

// 提交逻辑
const handleSubmit = async () => {
  const payload: any = {
    name: form.name,
    description: form.description,
    type: form.type,
    base_url: form.base_url,
    real_model_name: form.real_model_name,
    is_active: form.is_active
  }

  if (isEdit.value) {
    // 编辑时：
    // 留空 → 不修改原 key
    // 用户填写 → 覆盖数据库
    if (form.model_key.trim() !== "") {
      payload.model_key = form.model_key.trim()
    }
    await updateModel(form.id, payload)
    ElMessage.success('更新成功')
  } else {
    // 创建时：保证字段存在，即使为空
    payload.model_key = form.model_key?.trim() || ""
    await createModel(payload)
    ElMessage.success('创建成功')
  }

  dialogVisible.value = false
  loadModels()
}

// 删除
const handleDelete = async (id: string) => {
  await deleteModel(id)
  ElMessage.success('删除成功')
  loadModels()
}

onMounted(loadModels)
</script>

<style scoped>
.model-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
</style>


                 <!-- ┌──────────────┐
                 │ 用户操作模型 │
                 └──────┬──────┘
                        │
                ┌───────┴────────┐
                │ 创建模型？(Yes)│
                └───────┬────────┘
                        │
              ┌─────────┴─────────┐
              │ form.model_key?   │
              │ 是否为空或空格?   │
              └───────┬──────────┘
          Yes          │ No
           │           ▼
  ┌────────▼─────────┐ ┌───────────────┐
  │ payload.model_key │ │ payload.model_key │
  │ = ""              │ │ = trim后的值    │
  └────────┬─────────┘ └───────────────┘
           │
           ▼
      创建模型提交
           │
           ▼
      数据库 key 值保存
           │
           ▼
        完成

──────────────────────────────────

               ┌──────────────┐
               │ 编辑模型？(Yes) │
               └───────┬───────┘
                       │
          ┌────────────┴────────────┐
          │ form.model_key?         │
          │ 是否为空或空格?         │
          └─────────┬─────────────┘
      Yes          │ No
       │           ▼
┌──────▼───────┐ ┌───────────────┐
│ 不传 model_key│ │ payload.model_key │
│ (保持原 key) │ │ = trim后的值    │
└──────────────┘ └───────────────┘
       │                   │
       ▼                   ▼
  更新模型提交         更新模型提交
       │                   │
       ▼                   ▼
数据库原 key 不变      数据库 key 被覆盖
       │                   │
       ▼                   ▼
      完成               完成 -->

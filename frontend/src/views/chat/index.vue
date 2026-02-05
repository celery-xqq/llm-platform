<!-- src/views/chat/index.vue -->
<template>
  <div class="chat-page">
    <!-- 左侧会话栏 -->
    <aside class="sidebar">
      <el-button type="primary" class="new-btn" @click="createConversation">
        + 新对话
      </el-button>

      <div class="conversation-list">
        <div
          v-for="conv in conversations"
          :key="conv.id"
          class="conversation-item"
          :class="{ active: conv.id === activeConversationId }"
        >
          <!-- 重命名状态：在列表项内行内编辑 -->
          <template v-if="renamingConversationId === conv.id">
            <el-input
              v-model="renamingTitleInput"
              size="small"
              class="rename-input"
              @keyup.enter.stop="saveRename(conv.id)"
              @keyup.esc.stop="cancelRename"
            />
            <el-button size="mini" type="primary" @click.stop="saveRename(conv.id)">保存</el-button>
            <el-button size="mini" @click.stop="cancelRename">取消</el-button>
          </template>
          <template v-else>
            <span class="conv-title" @click.stop="selectConversation(conv.id)">{{ conv.title || '新对话' }}</span>

            <!-- 三点菜单：包含重命名、删除等操作 -->
            <el-dropdown @command="(cmd: string) => handleDropdownCommand(conv, cmd)" trigger="click">
              <span class="more-btn">
                ⋯
              </span>
              <template #dropdown>
                <el-dropdown-item command="rename">重命名</el-dropdown-item>
                <el-dropdown-item command="delete"><span style="color: #f56c6c">删除</span></el-dropdown-item>
              </template>
            </el-dropdown>
          </template>
        </div>
      </div>
    </aside>

    <!-- 右侧聊天区 -->
    <section class="chat-container">
      <!-- 新增：模型选择下拉框 -->
      <div class="model-selector">
        <el-select
          v-model="modelId"
          placeholder="请选择对话模型"
          :disabled="!models.length"
          style="width: 200px;"
        >
          <el-option
            v-for="model in models"
            :key="model.id"
            :label="model.name"
            :value="model.id"
          />
        </el-select>
      </div>

        <!-- 对话标题：展示并支持编辑 -->
        <div class="chat-header" v-if="activeConversationId !== null">
          <template v-if="editingTitle">
            <el-input
              v-model="titleInput"
              size="small"
              class="title-input"
              @keyup.enter="saveTitle"
              @keyup.esc="cancelEdit"
              placeholder="编辑会话标题"
              clearable
            />
            <el-button size="small" type="primary" @click="saveTitle">保存</el-button>
            <el-button size="small" @click="cancelEdit">取消</el-button>
          </template>
          <template v-else>
            <div class="title-display">
              <h3 class="title-text">{{ currentConversationTitle || '新对话' }}</h3>
              <el-button type="text" size="small" @click="startEdit">编辑</el-button>
            </div>
          </template>
        </div>

      <div class="message-list">
        <div
          v-for="msg in messages"
          :key="msg.id"
          class="message"
          :class="msg.role"
        >
          <div class="role">
            {{ msg.role === 'user' ? '你' : 'AI' }}
          </div>
          <div class="content">
            {{ msg.content }}
          </div>
        </div>
      </div>

      <div class="input-area">
        <el-input
          v-model="input"
          placeholder="请输入内容"
          clearable
          @keyup.enter="sendMessage"
        />
        <el-button type="primary" @click="sendMessage">
          发送
        </el-button>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus' // 新增：引入Element Plus的消息提示组件与确认框
import {
  getConversations,
  getConversationMessages,
  sendChat,
  updateConversationTitle, // 新增：导入更新标题的接口
  deleteConversation // 新增：导入删除会话的接口
} from '@/api/chat'
import { getModels } from '@/api/model' // 新增：引入获取模型列表的接口

/* ================= types ================= */
interface Conversation {
  id: string
  title: string
}

interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
}

// 新增：定义模型的接口（匹配后端返回的模型数据结构）
interface LLMModel {
  id: string // 模型ID（传给后端的model_id）
  name: string // 模型名称（前端展示用）
  status?: number // 可选：模型状态（1=启用，0=禁用）
}

/* ================= state ================= */
const conversations = ref<Conversation[]>([])
const activeConversationId = ref<string | null>(null)
const messages = ref<ChatMessage[]>([])
const input = ref('')

// 可编辑标题相关
const editingTitle = ref(false)
const titleInput = ref('')

// 修改：不再硬编码，初始化为空字符串，后续从接口获取
const modelId = ref<string>('')
// 新增：存储有效的模型列表
const models = ref<LLMModel[]>([])

/* ================= api ================= */
const loadConversations = async () => {
  try {
    conversations.value = await getConversations()
  } catch (err) {
    ElMessage.error('加载会话列表失败，请稍后重试')
    console.error('加载会话列表失败：', err)
  }
}

const loadMessages = async (conversationId: string) => {
  try {
    messages.value = await getConversationMessages(conversationId)
  } catch (err) {
    ElMessage.error('加载历史消息失败，请稍后重试')
    console.error('加载历史消息失败：', err)
  }
}

// 新增：加载模型列表
const loadModels = async () => {
  try {
    const modelList = await getModels()
    // 修复2：兼容后端不返回status字段的情况（避免过滤掉所有模型）
    models.value = modelList.filter((model: LLMModel) => {
      // 若后端返回status，只保留启用状态（status !== 0）；若不返回status，默认视为可用
      return model.status === undefined || model.status !== 0
    })
    // 自动选中第一个可用模型（非空断言已加，且有长度判断，安全）
    if (models.value.length > 0) {
      modelId.value = models.value[0]!.id
    } else {
      ElMessage.warning('暂无可用的对话模型，请联系管理员配置')
    }
  } catch (err) {
    ElMessage.error('加载模型列表失败，请稍后重试')
    console.error('加载模型列表失败：', err)
  }
}


/* ================= actions ================= */
const createConversation = () => {
  activeConversationId.value = null
  messages.value = []
  // 新对话时清空标题编辑状态
  editingTitle.value = false
  titleInput.value = ''
}

const selectConversation = async (id: string) => {
  activeConversationId.value = id
  await loadMessages(id)
  // 同步当前会话标题到输入框（便于编辑）
  const conv = conversations.value.find(c => c.id === id)
  titleInput.value = conv ? conv.title : ''
  editingTitle.value = false
}

// 计算当前会话标题（用于显示）
const currentConversationTitle = computed(() => {
  if (!activeConversationId.value) return ''
  const conv = conversations.value.find(c => c.id === activeConversationId.value)
  return conv ? conv.title : ''
})

const startEdit = () => {
  if (!activeConversationId.value) {
    ElMessage.warning('请先选择一个已有对话再编辑标题')
    return
  }
  titleInput.value = currentConversationTitle.value || ''
  editingTitle.value = true
}

const cancelEdit = () => {
  editingTitle.value = false
  titleInput.value = currentConversationTitle.value || ''
}

const saveTitle = async () => {
  const id = activeConversationId.value
  if (!id) {
    ElMessage.warning('无效的会话，无法保存标题')
    return
  }
  const newTitle = (titleInput.value || '').trim()
  if (!newTitle) {
    ElMessage.warning('标题不能为空')
    return
  }
  try {
    await updateConversationTitle(id, newTitle)
    // 本地更新（立即生效），再刷新列表以确保一致性
    const idx = conversations.value.findIndex(c => c.id === id)
    if (idx >= 0) conversations.value[idx]!.title = newTitle
    editingTitle.value = false
    ElMessage.success('会话标题已保存')
    await loadConversations()
  } catch (err) {
    ElMessage.error('保存标题失败，请稍后重试')
    console.error('保存标题失败：', err)
  }
}

const sendMessage = async () => {
  const content = input.value.trim()
  // 新增：校验模型是否已选择
  if (!content) {
    ElMessage.warning('请输入要发送的内容')
    return
  }
  if (!modelId.value) {
    ElMessage.warning('请先选择一个可用的对话模型')
    return
  }

    // 记录发送前是否是新对话（activeConversationId为null就是新对话）
  const isNewConversation = activeConversationId.value === null
  input.value = ''

  // 立即显示用户消息
  const userMsg: ChatMessage = {
    id: crypto.randomUUID(),
    role: 'user',
    content
  }
  messages.value.push(userMsg)

  try {
    const res = await sendChat({
      model_id: modelId.value,
      content,
      conversation_id: activeConversationId.value ?? undefined
    })

    // // 更新当前会话ID（新对话时会返回新的conversation_id）
    // activeConversationId.value = res.conversation_id

    // 更新当前会话ID
    const newConversationId = res.conversation_id
    activeConversationId.value = newConversationId

    // 3. 若是新对话，生成标题并更新
    if (isNewConversation && newConversationId) {
      // 截取前20个字作为标题，超出部分用...代替，保证标题简洁
      const newTitle = content.length > 20 ? `${content.slice(0, 20)}...` : content
      try {
        // 调用更新标题接口
        await updateConversationTitle(newConversationId, newTitle)
        ElMessage.success('会话标题已更新')
      } catch (err) {
        ElMessage.warning('会话标题更新失败')
        console.error('更新标题失败：', err)
      }
    }

    // 显示AI回复消息
    const aiMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'assistant',
      content: res.content
    }
    messages.value.push(aiMsg)

    // 刷新会话列表（更新新对话的标题等信息）
    await loadConversations()
  } catch (err) {
    ElMessage.error('发送消息失败，请稍后重试')
    console.error('发送消息失败：', err)
    // 可选：移除用户消息（或保留并标记发送失败）
    // messages.value = messages.value.filter(msg => msg.id !== userMsg.id)
  }
}

// 重命名相关（在列表内行内编辑）
const renamingConversationId = ref<string | null>(null)
const renamingTitleInput = ref<string>('')

const handleDropdownCommand = (conv: Conversation, cmd: string) => {
  if (cmd === 'rename') {
    startRename(conv)
  } else if (cmd === 'delete') {
    confirmDelete(conv.id)
  }
}

const startRename = (conv: Conversation) => {
  renamingConversationId.value = conv.id
  renamingTitleInput.value = conv.title || ''
}

const cancelRename = () => {
  renamingConversationId.value = null
  renamingTitleInput.value = ''
}

const saveRename = async (conversationId: string) => {
  const newTitle = (renamingTitleInput.value || '').trim()
  if (!newTitle) {
    ElMessage.warning('标题不能为空')
    return
  }
  try {
    await updateConversationTitle(conversationId, newTitle)
    // 本地更新并清理状态
    const idx = conversations.value.findIndex(c => c.id === conversationId)
    if (idx >= 0) conversations.value[idx]!.title = newTitle
    renamingConversationId.value = null
    renamingTitleInput.value = ''
    ElMessage.success('重命名成功')
    await loadConversations()
  } catch (err) {
    console.error('重命名失败：', err)
    ElMessage.error('重命名失败，请稍后重试')
  }
}

/* ================= lifecycle ================= */
// 删除会话（前端操作）：带确认
const confirmDelete = async (conversationId: string) => {
  try {
    await ElMessageBox.confirm('确认删除该会话及其所有消息吗？此操作不可恢复。', '删除会话', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })

    // 调用删除 API
    await deleteConversation(conversationId)
    ElMessage.success('会话已删除')

    // 如果当前正在查看该会话，清空视图
    if (activeConversationId.value === conversationId) {
      activeConversationId.value = null
      messages.value = []
      editingTitle.value = false
      titleInput.value = ''
    }

    // 刷新会话列表
    await loadConversations()
  } catch (err: any) {
    // 用户取消会触发 reject，这里忽略取消错误
    if (err === 'cancel' || (err && err.message && err.message.includes('cancel'))) {
      return
    }
    console.error('删除会话失败：', err)
    ElMessage.error('删除会话失败，请稍后重试')
  }
}

onMounted(async () => {
  // 并行加载模型列表和会话列表，提升加载效率
  await Promise.all([
    loadModels(),
    loadConversations()
  ])
})
</script>

<style scoped>
.chat-page {
  display: flex;
  height: 100vh; /* 改为vh，确保占满视口高度 */
  margin: 0;
  padding: 0;
}

/* sidebar */
.sidebar {
  width: 240px;
  border-right: 1px solid #e5e5e5;
  padding: 12px;
  box-sizing: border-box;
}

.new-btn {
  width: 100%;
  margin-bottom: 12px;
}

.conversation-item {
  padding: 8px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 4px;
}

.conversation-item:hover {
  background: #f5f7fa;
}

.conversation-item.active {
  background: #409eff;
  color: white;
}

.conversation-item .conv-title {
  display: inline-block;
  vertical-align: middle;
  margin-right: 8px;
}
.conversation-item .conv-delete {
  float: right;
  color: rgba(0,0,0,0.45);
}

.more-btn {
  display: inline-block;
  width: 28px;
  height: 28px;
  line-height: 28px;
  text-align: center;
  border-radius: 6px;
  cursor: pointer;
  color: rgba(0,0,0,0.6);
}
.more-btn:hover {
  background: rgba(0,0,0,0.03);
}
.conversation-item .rename-input {
  width: calc(100% - 110px);
  display: inline-block;
  vertical-align: middle;
}

/* chat */
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

/* 新增：模型选择器样式 */
.model-selector {
  padding: 12px 20px;
  border-bottom: 1px solid #e5e5e5;
  display: flex;
  align-items: center;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  box-sizing: border-box;
}

.message {
  margin-bottom: 14px;
}

.message.user {
  text-align: right;
}

.message.assistant {
  text-align: left;
}

.role {
  font-size: 12px;
  color: #888;
  margin-bottom: 4px;
}

.content {
  font-size: 14px;
  line-height: 1.6;
  padding: 8px 12px;
  border-radius: 4px;
  display: inline-block;
  max-width: 80%;
}

/* 新增：消息内容背景色，提升区分度 */
.message.user .content {
  background: #409eff;
  color: white;
}

.message.assistant .content {
  background: #f5f7fa;
  color: #333;
}

/* input */
.input-area {
  display: flex;
  gap: 10px;
  padding: 12px;
  border-top: 1px solid #e5e5e5;
  box-sizing: border-box;
}

.input-area el-input {
  flex: 1;
}

/* 对话标题样式 */
.chat-header {
  padding: 12px 20px;
  border-bottom: 1px solid #eaeaea;
  display: flex;
  align-items: center;
  gap: 12px;
}
.title-display {
  display: flex;
  align-items: center;
  gap: 8px;
}
.title-text {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}
.title-input {
  width: 360px;
}
</style>
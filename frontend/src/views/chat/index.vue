<!-- src/views/chat/index.vue -->
<!-- <template>
  <div class="chat-container">
    <el-card class="chat-card">
      <div class="model-select">
        <el-select v-model="selectedModelId" placeholder="选择模型" style="width: 300px;">
          <el-option
            v-for="model in modelList"
            :key="model.id"
            :label="model.name"
            :value="model.id"
          />
        </el-select>
      </div>
      <div class="chat-window" ref="chatWindow">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['chat-message', msg.role]"
        >
          <div class="chat-bubble">{{ msg.content }}</div>
        </div>
        <div v-if="loading" class="chat-loading">助手正在输入...</div>
      </div>
      <div class="chat-input">
        <el-input
          type="textarea"
          v-model="inputMessage"
          :rows="2"
          placeholder="请输入消息，按 Ctrl + Enter 发送"
          @keyup.enter.ctrl.native="sendMessage"
        />
        <el-button
          type="primary"
          :loading="loading"
          @click="sendMessage"
          style="margin-left: 8px"
        >
          发送
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { getModels } from '@/api/model'
import { chatWithModel } from '@/api/chat'
import type { Message } from '@/api/chat' // ✅ 这里改成 import type


const modelList = ref<any[]>([])
const selectedModelId = ref<string>('')

// 聊天记录
const messages = ref<Message[]>([])
const inputMessage = ref('')
const loading = ref(false)

// 聊天窗口ref（滚动到底部用）
const chatWindow = ref<HTMLDivElement | null>(null)

// 加载模型列表
const loadModels = async () => {
  try {
    const list = await getModels()
    modelList.value = list
    if (list.length > 0 && !selectedModelId.value) {
      selectedModelId.value = list[0].id
    }
  } catch (err) {
    console.error(err)
    ElMessage.error('加载模型失败')
  }
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (chatWindow.value) {
      chatWindow.value.scrollTop = chatWindow.value.scrollHeight
    }
  })
}

// 发送消息
const sendMessage = async () => {
  const content = inputMessage.value.trim()
  if (!content) return
  if (!selectedModelId.value) {
    ElMessage.warning('请先选择模型')
    return
  }

  // 添加用户消息
  messages.value.push({ role: 'user', content })
  inputMessage.value = ''
  scrollToBottom()
  loading.value = true

  try {
    const res = await chatWithModel({
      model_id: selectedModelId.value,
      messages: [{ role: 'user', content }],
      temperature: 0.7
    })

    if (res.success) {
      messages.value.push({ role: 'assistant', content: res.content || '' })
    } else {
      messages.value.push({ role: 'assistant', content: `出错啦: ${res.error}` })
    }
  } catch (err: any) {
    console.error(err)
    messages.value.push({ role: 'assistant', content: `请求失败: ${err.message}` })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

onMounted(loadModels)
</script>

<style scoped>
.chat-container {
  padding: 20px;
}

.chat-card {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}

.model-select {
  margin-bottom: 12px;
}

.chat-window {
  flex: 1;
  min-height: 400px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  padding: 12px;
  overflow-y: auto;
  margin-bottom: 12px;
  background-color: #f5f7fa;
}

.chat-message {
  display: flex;
  margin-bottom: 8px;
}

.chat-message.user {
  justify-content: flex-end;
}

.chat-message.assistant {
  justify-content: flex-start;
}

.chat-bubble {
  max-width: 70%;
  padding: 8px 12px;
  border-radius: 12px;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chat-message.user .chat-bubble {
  background-color: #409eff;
  color: #fff;
}

.chat-loading {
  font-style: italic;
  color: #999;
  margin-top: 4px;
}

.chat-input {
  display: flex;
  align-items: center;
}
</style> -->

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
          @click="selectConversation(conv.id)"
        >
          {{ conv.title || '新对话' }}
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
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus' // 新增：引入Element Plus的消息提示组件
import {
  getConversations,
  getConversationMessages,
  sendChat,
  updateConversationTitle // 新增：导入更新标题的接口
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

// // 新增：加载模型列表
// const loadModels = async () => {
//   try {
//     const modelList = await getModels()
//     // 过滤出启用状态的模型（如果后端返回status字段，无则直接使用全部）
//     models.value = modelList.filter((model: LLMModel) => model.status !== 0)
//     // 自动选中第一个可用模型
//     if (models.value.length > 0) {
//       modelId.value = models.value[0]!.id
//     } else {
//       ElMessage.warning('暂无可用的对话模型，请联系管理员配置')
//     }
//   } catch (err) {
//     ElMessage.error('加载模型列表失败，请稍后重试')
//     console.error('加载模型列表失败：', err)
//   }
// }

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
}

const selectConversation = async (id: string) => {
  activeConversationId.value = id
  await loadMessages(id)
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

/* ================= lifecycle ================= */
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
</style>


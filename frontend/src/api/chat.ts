// src/api/chat.ts
// import request from '@/utils/request'

// export interface Message {
//   role: 'user' | 'assistant'
//   content: string
// }

// export interface ChatRequest {
//   model_id: string
//   messages: Message[]
//   temperature?: number
//   max_tokens?: number
// }

// export interface ChatResponse {
//   success: boolean
//   content?: string
//   model_id: string
//   model_name: string
//   error?: string
//   usage?: {
//     prompt_tokens: number
//     completion_tokens: number
//     total_tokens: number
//   }
// }

// // 发起对话
// export const chatWithModel = (data: ChatRequest) => {
//   return request<ChatResponse>({
//     url: '/api/v1/chat/',
//     method: 'post',
//     data
//   })
// }


// src/api/chat.ts
import request from '@/utils/request'

/* ================= 会话 ================= */

// 会话列表
export const getConversations = () => {
  return request({
    url: '/api/v1/conversations/',
    method: 'get'
  })
}

/* ================= 消息 ================= */

// 获取某个会话的历史消息
export const getConversationMessages = (conversationId: string) => {
  return request({
    url: `/api/v1/conversations/${conversationId}/messages`,
    method: 'get'
  })
}

/* ================= 对话 ================= */

// 发送消息（自动多轮）
export const sendChat = (data: {
  model_id: string
  content: string
  conversation_id?: string
}) => {
  return request({
    url: '/api/v1/chat/',
    method: 'post',
    data
  })
}


// 更新会话标题（对接后端新增的PATCH接口）
export const updateConversationTitle = (conversationId: string, title: string) => {
  return request({
    url: `/api/v1/conversations/${conversationId}/title`,
    method: 'patch',
    data: { title } // 对应后端的 ConversationTitleUpdate 模型
  })
}

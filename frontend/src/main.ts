// src/main.ts
import { createApp } from 'vue'
import { createPinia } from 'pinia' // 正确的Pinia创建方式
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'
import './assets/style.css'

// 1. 创建Pinia实例
const pinia = createPinia()
const app = createApp(App)

// 注册Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 2. 先挂载Pinia，再挂载路由和Element Plus
app.use(pinia)
app.use(router)
app.use(ElementPlus)

app.mount('#app')

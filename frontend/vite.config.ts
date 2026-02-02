// import { defineConfig } from 'vite'
// import vue from '@vitejs/plugin-vue'

// // https://vite.dev/config/
// export default defineConfig({
//   plugins: [vue()],
// })


import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    port: 5173, // 前端运行端口
    open: true, // 启动后自动打开浏览器
    proxy: {
      // 跨域代理，对接后端接口
      // 关键修改：去掉 rewrite 规则，保留完整路径转发
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true // 只保留这两行，删掉 rewrite
        //rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})

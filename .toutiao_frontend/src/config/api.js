/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 */

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: 'http://127.0.0.1:8000',
}

export const aiChatConfig = {
  // OpenAI API地址
  apiEndpoint: 'https://api.deepseek.com/chat/completions',
  
  // API Key (由开发人员指定)
  apiKey: 'sk-bbb22ca1cd1748aaa7b3bfa8affe4678',
  
  // 使用的模型
  model: 'deepseek-flash'
}

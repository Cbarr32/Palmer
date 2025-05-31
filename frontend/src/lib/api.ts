import axios from 'axios'

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const api = {
  auth: {
    login: async (email: string, password: string) => {
      const response = await apiClient.post('/auth/token', {
        username: email,
        password,
      })
      return response.data
    },
    register: async (data: any) => {
      const response = await apiClient.post('/auth/register', data)
      return response.data
    },
    me: async () => {
      const response = await apiClient.get('/auth/me')
      return response.data
    },
  },
  
  analysis: {
    quickScan: async (data: any) => {
      const response = await apiClient.post('/analysis/quick-scan', data)
      return response.data
    },
    comprehensive: async (data: any) => {
      const response = await apiClient.post('/analysis/comprehensive', data)
      return response.data
    },
    getStatus: async (id: string) => {
      const response = await apiClient.get(`/analysis/status/${id}`)
      return response.data
    },
    history: async () => {
      const response = await apiClient.get('/analysis/history')
      return response.data
    },
  },
  
  competitive: {
    analyze: async (target: string, competitors: string[]) => {
      const response = await apiClient.post('/competitive/analyze', {
        target_url: target,
        competitors,
      })
      return response.data
    },
    suggestions: async (target: string) => {
      const response = await apiClient.get(`/competitive/suggestions/${target}`)
      return response.data
    },
  },
  
  intelligence: {
    industryReport: async (industry: string, competitors: string[]) => {
      const response = await apiClient.post('/intelligence/industry-report', {
        industry,
        competitors,
      })
      return response.data
    },
    insights: async (organizationId: string) => {
      const response = await apiClient.get(`/intelligence/insights/${organizationId}`)
      return response.data
    },
    predict: async (industry: string, timeframe: string) => {
      const response = await apiClient.post('/intelligence/predict', {
        industry,
        timeframe,
      })
      return response.data
    },
  },
}

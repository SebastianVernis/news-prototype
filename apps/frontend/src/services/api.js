import axios from 'axios'

// Configuración de la API
// En desarrollo usa el proxy de Vite, en producción usa la URL configurada
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutos para operaciones largas
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// Endpoints de la API
export const sitesAPI = {
  // Obtener todos los sitios
  getAll: async () => {
    const response = await api.get('/sites')
    return response.data
  },

  // Obtener un sitio específico
  getById: async (id) => {
    const response = await api.get(`/sites/${id}`)
    return response.data
  },

  // Generar nuevos sitios
  generate: async (config) => {
    const response = await api.post('/sites/generate', config)
    return response.data
  },

  // Eliminar un sitio
  delete: async (id) => {
    const response = await api.delete(`/sites/${id}`)
    return response.data
  },

  // Obtener estadísticas
  getStats: async () => {
    const response = await api.get('/sites/stats')
    return response.data
  },
}

export const metadataAPI = {
  // Obtener metadatos
  getAll: async () => {
    const response = await api.get('/metadata')
    return response.data
  },

  // Generar metadatos
  generate: async (config) => {
    const response = await api.post('/metadata/generate', config)
    return response.data
  },

  // Cargar archivo de metadatos
  load: async (filename) => {
    const response = await api.get(`/metadata/${filename}`)
    return response.data
  },
}

export const settingsAPI = {
  // Obtener configuración
  get: async () => {
    const response = await api.get('/settings')
    return response.data
  },

  // Actualizar configuración
  update: async (settings) => {
    const response = await api.put('/settings', settings)
    return response.data
  },

  // Verificar estado del sistema
  checkStatus: async () => {
    const response = await api.get('/settings/status')
    return response.data
  },
}

export default api

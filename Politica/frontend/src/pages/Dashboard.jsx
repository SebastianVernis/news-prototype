import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Globe, FileText, Clock, TrendingUp, Plus, Eye } from 'lucide-react'
import { sitesAPI, settingsAPI } from '../services/api'
import './Dashboard.css'

function Dashboard() {
  const navigate = useNavigate()
  const [stats, setStats] = useState({
    totalSites: 0,
    recentSites: 0,
    totalArticles: 0,
    lastGeneration: null
  })

  const [systemStatus, setSystemStatus] = useState({
    nameGenerator: false,
    domainVerifier: false,
    newsApi: false,
    layoutGenerator: false
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
    loadSystemStatus()
  }, [])

  const loadStats = async () => {
    try {
      const response = await sitesAPI.getStats()
      if (response.success) {
        setStats(response.stats)
      }
    } catch (error) {
      console.error('Error loading stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadSystemStatus = async () => {
    try {
      const response = await settingsAPI.checkStatus()
      if (response.success) {
        setSystemStatus(response.status)
      }
    } catch (error) {
      console.error('Error loading system status:', error)
    }
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Dashboard</h2>
        <button 
          className="btn btn-primary"
          onClick={() => navigate('/create')}
        >
          <Plus size={20} />
          Crear Nuevos Sitios
        </button>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'var(--secondary)' }}>
            <Globe size={28} color="white" />
          </div>
          <div className="stat-content">
            <h3>{stats.totalSites}</h3>
            <p>Sitios Generados</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'var(--success)' }}>
            <TrendingUp size={28} color="white" />
          </div>
          <div className="stat-content">
            <h3>{stats.recentSites}</h3>
            <p>Sitios Recientes</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'var(--warning)' }}>
            <FileText size={28} color="white" />
          </div>
          <div className="stat-content">
            <h3>{stats.totalArticles}</h3>
            <p>Artículos Totales</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'var(--accent)' }}>
            <Clock size={28} color="white" />
          </div>
          <div className="stat-content">
            <h3>{stats.lastGeneration ? 'Hoy' : 'N/A'}</h3>
            <p>Última Generación</p>
          </div>
        </div>
      </div>

      <div className="dashboard-actions">
        <div className="action-card">
          <div className="action-header">
            <h3>Acciones Rápidas</h3>
          </div>
          <div className="action-buttons">
            <button 
              className="action-btn"
              onClick={() => navigate('/create')}
            >
              <Plus size={24} />
              <div>
                <strong>Crear Sitios</strong>
                <p>Generar nuevos sitios de noticias</p>
              </div>
            </button>
            <button 
              className="action-btn"
              onClick={() => navigate('/sites')}
            >
              <Eye size={24} />
              <div>
                <strong>Ver Sitios</strong>
                <p>Explorar sitios generados</p>
              </div>
            </button>
          </div>
        </div>

        <div className="action-card">
          <div className="action-header">
            <h3>Estado del Sistema</h3>
          </div>
          <div className="system-status">
            <div className="status-item">
              <div className={`status-dot ${systemStatus.nameGenerator ? 'active' : ''}`}></div>
              <span>Generador de Nombres</span>
            </div>
            <div className="status-item">
              <div className={`status-dot ${systemStatus.domainVerifier ? 'active' : ''}`}></div>
              <span>Verificador de Dominios</span>
            </div>
            <div className="status-item">
              <div className={`status-dot ${systemStatus.newsApi ? 'active' : ''}`}></div>
              <span>API de Noticias</span>
            </div>
            <div className="status-item">
              <div className={`status-dot ${systemStatus.layoutGenerator ? 'active' : ''}`}></div>
              <span>Generador de Layouts</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

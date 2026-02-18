import React, { useState, useEffect } from 'react'
import { Eye, Download, Trash2, Globe, Calendar, Palette } from 'lucide-react'
import { sitesAPI } from '../services/api'
import './SitesList.css'

function SitesList() {
  const [sites, setSites] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    loadSites()
  }, [])

  const loadSites = async () => {
    try {
      const response = await sitesAPI.getAll()
      if (response.success) {
        setSites(response.sites)
      }
    } catch (err) {
      console.error('Error loading sites:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleView = (site) => {
    // En desarrollo usa proxy de Vite, en producción usa URL configurada
    const apiUrl = import.meta.env.VITE_API_URL || '/api'
    window.open(`${apiUrl}/sites/${site.id}/view`, '_blank')
  }

  const handleDownload = (site) => {
    // TODO: Implementar descarga
    alert('Descarga no implementada aún')
  }

  const handleDelete = async (site) => {
    if (window.confirm(`¿Eliminar sitio "${site.nombre || `Sitio ${site.id}`}"?`)) {
      try {
        await sitesAPI.delete(site.id)
        setSites(sites.filter(s => s.id !== site.id))
      } catch (err) {
        console.error('Error deleting site:', err)
        alert('Error al eliminar el sitio')
      }
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('es-MX', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Cargando sitios...</p>
      </div>
    )
  }

  return (
    <div className="sites-list">
      <div className="page-header">
        <div>
          <h2>Mis Sitios Generados</h2>
          <p>{sites.length} sitios disponibles</p>
        </div>
        <div className="filter-buttons">
          <button 
            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            Todos
          </button>
          <button 
            className={`filter-btn ${filter === 'recent' ? 'active' : ''}`}
            onClick={() => setFilter('recent')}
          >
            Recientes
          </button>
        </div>
      </div>

      {sites.length === 0 ? (
        <div className="empty-state">
          <Globe size={64} color="var(--border)" />
          <h3>No hay sitios generados</h3>
          <p>Comienza creando tu primer sitio de noticias</p>
          <button className="btn btn-primary">
            Crear Sitios
          </button>
        </div>
      ) : (
        <div className="sites-grid">
          {sites.map(site => (
            <div key={site.id} className="site-card">
              <div 
                className="site-header"
                style={{ 
                  background: `linear-gradient(135deg, #2C3E50 0%, #3498DB 100%)`
                }}
              >
                <h3>{site.nombre}</h3>
                <p>{site.filename}</p>
              </div>

              <div className="site-body">
                <div className="site-info">
                  <div className="info-row">
                    <Globe size={16} />
                    <span>{site.filename}</span>
                  </div>
                  <div className="info-row">
                    <Palette size={16} />
                    <span>{(site.size / 1024).toFixed(2)} KB</span>
                  </div>
                  <div className="info-row">
                    <Calendar size={16} />
                    <span>{formatDate(site.createdAt)}</span>
                  </div>
                </div>

                <div className="site-stats">
                  <span>Sitio HTML generado</span>
                </div>
              </div>

              <div className="site-actions">
                <button 
                  className="action-btn action-view"
                  onClick={() => handleView(site)}
                  title="Ver sitio"
                >
                  <Eye size={18} />
                  Ver
                </button>
                <button 
                  className="action-btn action-download"
                  onClick={() => handleDownload(site)}
                  title="Descargar"
                >
                  <Download size={18} />
                </button>
                <button 
                  className="action-btn action-delete"
                  onClick={() => handleDelete(site)}
                  title="Eliminar"
                >
                  <Trash2 size={18} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default SitesList

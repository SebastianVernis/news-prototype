import React, { useState } from 'react'
import { AlertCircle, CheckCircle, Loader, Settings as SettingsIcon } from 'lucide-react'
import { sitesAPI } from '../services/api'
import './CreateSites.css'

function CreateSites() {
  const [formData, setFormData] = useState({
    quantity: 5,
    verifyDomains: false,
    useExistingMetadata: false,
    metadataFile: '',
    generateMetadata: true
  })

  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await sitesAPI.generate(formData)
      
      if (response.success) {
        setResult(response)
      } else {
        setError(response.error || 'Error desconocido al generar sitios')
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Error al generar sitios')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="create-sites">
      <div className="page-header">
        <h2>Crear Sitios de Noticias</h2>
        <p>Genera múltiples sitios con layouts únicos y contenido diverso</p>
      </div>

      <div className="create-content">
        <div className="create-form-card">
          <form onSubmit={handleSubmit}>
            <div className="form-section">
              <h3>Configuración Básica</h3>
              
              <div className="form-group">
                <label htmlFor="quantity">
                  Cantidad de Sitios
                  <span className="label-hint">(1-100)</span>
                </label>
                <input
                  type="number"
                  id="quantity"
                  name="quantity"
                  min="1"
                  max="100"
                  value={formData.quantity}
                  onChange={handleInputChange}
                  required
                />
                <small>Número de sitios HTML a generar</small>
              </div>
            </div>

            <div className="form-section">
              <h3>Opciones de Metadatos</h3>
              
              <div className="form-group checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    name="generateMetadata"
                    checked={formData.generateMetadata}
                    onChange={handleInputChange}
                  />
                  <span>Generar nuevos metadatos</span>
                </label>
                <small>Crear nombres, dominios y configuraciones únicas</small>
              </div>

              <div className="form-group checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    name="useExistingMetadata"
                    checked={formData.useExistingMetadata}
                    onChange={handleInputChange}
                    disabled={formData.generateMetadata}
                  />
                  <span>Usar metadatos existentes</span>
                </label>
                <small>Cargar desde archivo JSON previamente generado</small>
              </div>

              {formData.useExistingMetadata && (
                <div className="form-group">
                  <label htmlFor="metadataFile">Archivo de Metadatos</label>
                  <input
                    type="text"
                    id="metadataFile"
                    name="metadataFile"
                    value={formData.metadataFile}
                    onChange={handleInputChange}
                    placeholder="data/sites_metadata/sites_metadata_XXXXX.json"
                  />
                </div>
              )}
            </div>

            <div className="form-section">
              <h3>Verificación de Dominios</h3>
              
              <div className="form-group checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    name="verifyDomains"
                    checked={formData.verifyDomains}
                    onChange={handleInputChange}
                  />
                  <span>Verificar disponibilidad con WHOIS</span>
                </label>
                <small>Consulta real de disponibilidad (más lento pero preciso)</small>
              </div>

              {formData.verifyDomains && (
                <div className="warning-box">
                  <AlertCircle size={20} />
                  <div>
                    <strong>Nota:</strong> La verificación de dominios puede tardar varios minutos debido al rate limiting de WHOIS.
                  </div>
                </div>
              )}
            </div>

            <div className="form-actions">
              <button 
                type="submit" 
                className="btn btn-primary btn-lg"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Loader size={20} className="spinner" />
                    Generando Sitios...
                  </>
                ) : (
                  <>
                    <SettingsIcon size={20} />
                    Generar Sitios
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Results Panel */}
        {(result || error) && (
          <div className="results-panel">
            {error && (
              <div className="alert alert-error">
                <AlertCircle size={24} />
                <div>
                  <strong>Error</strong>
                  <p>{error}</p>
                </div>
              </div>
            )}

            {result && (
              <div className="alert alert-success">
                <CheckCircle size={24} />
                <div>
                  <strong>¡Sitios Generados Exitosamente!</strong>
                  <div className="result-stats">
                    <div className="result-stat">
                      <span className="stat-label">Sitios generados:</span>
                      <span className="stat-value">{result.sitesGenerated}</span>
                    </div>
                    {result.domainsVerified > 0 && (
                      <>
                        <div className="result-stat">
                          <span className="stat-label">Dominios verificados:</span>
                          <span className="stat-value">{result.domainsVerified}</span>
                        </div>
                        <div className="result-stat">
                          <span className="stat-label">Dominios disponibles:</span>
                          <span className="stat-value">{result.domainsAvailable}</span>
                        </div>
                      </>
                    )}
                    <div className="result-stat">
                      <span className="stat-label">Tiempo de ejecución:</span>
                      <span className="stat-value">{result.executionTime}</span>
                    </div>
                    <div className="result-stat">
                      <span className="stat-label">Archivo de metadatos:</span>
                      <span className="stat-value">{result.metadataFile}</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Info Panel */}
      <div className="info-panel">
        <h3>Características de Generación</h3>
        <ul>
          <li><strong>8 tipos de layouts</strong> diferentes por sitio</li>
          <li><strong>5 estilos de header</strong> únicos</li>
          <li><strong>5 estilos de navegación</strong> variados</li>
          <li><strong>Categorías randomizadas</strong> por sitio</li>
          <li><strong>Paletas de colores</strong> únicas</li>
          <li><strong>Nombres convincentes</strong> generados con IA</li>
          <li><strong>Metadatos SEO</strong> completos</li>
          <li><strong>Contenido diversificado</strong> en cada sitio</li>
        </ul>
      </div>
    </div>
  )
}

export default CreateSites

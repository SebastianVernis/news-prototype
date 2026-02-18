import React, { useState, useEffect } from 'react'
import { Save, Key, Database, Globe, AlertCircle } from 'lucide-react'
import { settingsAPI } from '../services/api'
import './Settings.css'

function Settings() {
  const [settings, setSettings] = useState({
    newsApiKey: '',
    newsdataKey: '',
    blackboxApiKey: '',
    defaultQuantity: 5,
    verifyDomainsByDefault: false,
    autoSaveMetadata: true,
    maxTemplates: 40
  })

  const [saved, setSaved] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadSettings()
  }, [])

  const loadSettings = async () => {
    try {
      const response = await settingsAPI.get()
      if (response.success) {
        setSettings(response.settings)
      }
    } catch (err) {
      console.error('Error loading settings:', err)
      setError('Error al cargar configuración')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    try {
      const response = await settingsAPI.update(settings)
      if (response.success) {
        setSaved(true)
        setTimeout(() => setSaved(false), 3000)
      } else {
        setError(response.error || 'Error al guardar configuración')
      }
    } catch (err) {
      console.error('Error saving settings:', err)
      setError(err.response?.data?.error || 'Error al guardar configuración')
    }
  }

  return (
    <div className="settings">
      <div className="page-header">
        <h2>Configuración del Sistema</h2>
        <p>Configura las opciones del generador de sitios</p>
      </div>

      <form onSubmit={handleSubmit}>
        {/* API Keys Section */}
        <div className="settings-section">
          <div className="section-header">
            <Key size={24} />
            <h3>Claves de API</h3>
          </div>

          <div className="form-group">
            <label htmlFor="newsApiKey">NewsAPI Key</label>
            <input
              type="password"
              id="newsApiKey"
              name="newsApiKey"
              value={settings.newsApiKey}
              onChange={handleChange}
              placeholder="Ingresa tu clave de NewsAPI"
            />
            <small>
              Obtén tu clave en{' '}
              <a href="https://newsapi.org/" target="_blank" rel="noopener noreferrer">
                newsapi.org
              </a>
            </small>
          </div>

          <div className="form-group">
            <label htmlFor="newsdataKey">NewsData Key</label>
            <input
              type="password"
              id="newsdataKey"
              name="newsdataKey"
              value={settings.newsdataKey}
              onChange={handleChange}
              placeholder="Ingresa tu clave de NewsData"
            />
            <small>
              Obtén tu clave en{' '}
              <a href="https://newsdata.io/" target="_blank" rel="noopener noreferrer">
                newsdata.io
              </a>
            </small>
          </div>

          <div className="form-group">
            <label htmlFor="blackboxApiKey">Blackbox AI API Key</label>
            <input
              type="password"
              id="blackboxApiKey"
              name="blackboxApiKey"
              value={settings.blackboxApiKey}
              onChange={handleChange}
              placeholder="Ingresa tu clave de Blackbox AI"
            />
            <small>Para generación de imágenes y parafraseo</small>
          </div>
        </div>

        {/* Generation Settings */}
        <div className="settings-section">
          <div className="section-header">
            <Database size={24} />
            <h3>Configuración de Generación</h3>
          </div>

          <div className="form-group">
            <label htmlFor="defaultQuantity">Cantidad Predeterminada de Sitios</label>
            <input
              type="number"
              id="defaultQuantity"
              name="defaultQuantity"
              min="1"
              max="100"
              value={settings.defaultQuantity}
              onChange={handleChange}
            />
            <small>Valor predeterminado al crear sitios (1-100)</small>
          </div>

          <div className="form-group">
            <label htmlFor="maxTemplates">Máximo de Templates CSS</label>
            <input
              type="number"
              id="maxTemplates"
              name="maxTemplates"
              min="1"
              max="100"
              value={settings.maxTemplates}
              onChange={handleChange}
            />
            <small>Número máximo de templates CSS disponibles</small>
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="verifyDomainsByDefault"
                checked={settings.verifyDomainsByDefault}
                onChange={handleChange}
              />
              <span>Verificar dominios por defecto</span>
            </label>
            <small>Activar verificación WHOIS automáticamente</small>
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="autoSaveMetadata"
                checked={settings.autoSaveMetadata}
                onChange={handleChange}
              />
              <span>Guardar metadatos automáticamente</span>
            </label>
            <small>Guardar metadatos en cada generación</small>
          </div>
        </div>

        {/* Domain Settings */}
        <div className="settings-section">
          <div className="section-header">
            <Globe size={24} />
            <h3>Configuración de Dominios</h3>
          </div>

          <div className="info-box">
            <AlertCircle size={20} />
            <div>
              <strong>Verificación WHOIS</strong>
              <p>
                La verificación de dominios requiere que <code>whois</code> esté instalado en tu sistema.
                En Ubuntu/Debian: <code>sudo apt-get install whois</code>
              </p>
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div className="settings-actions">
          <button type="submit" className="btn btn-primary btn-lg">
            <Save size={20} />
            Guardar Configuración
          </button>
          {saved && (
            <div className="save-success">
              ✓ Configuración guardada exitosamente
            </div>
          )}
          {error && (
            <div className="alert alert-error">
              <AlertCircle size={20} />
              {error}
            </div>
          )}
        </div>
      </form>

      {/* System Info */}
      <div className="system-info">
        <h3>Información del Sistema</h3>
        <div className="info-grid">
          <div className="info-item">
            <strong>Versión:</strong>
            <span>1.0.0</span>
          </div>
          <div className="info-item">
            <strong>Python:</strong>
            <span>3.8+</span>
          </div>
          <div className="info-item">
            <strong>Node.js:</strong>
            <span>18+</span>
          </div>
          <div className="info-item">
            <strong>Sitios Generados:</strong>
            <span>10</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Settings

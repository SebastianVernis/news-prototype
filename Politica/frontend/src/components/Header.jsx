import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Newspaper, Plus, List, Settings } from 'lucide-react'
import './Header.css'

function Header() {
  const location = useLocation()

  const isActive = (path) => location.pathname === path

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-brand">
          <Newspaper size={32} />
          <div>
            <h1>News Prototype</h1>
            <p>Generador de Sitios de Noticias</p>
          </div>
        </div>

        <nav className="header-nav">
          <Link 
            to="/" 
            className={`nav-item ${isActive('/') ? 'active' : ''}`}
          >
            <Newspaper size={20} />
            <span>Dashboard</span>
          </Link>
          <Link 
            to="/create" 
            className={`nav-item ${isActive('/create') ? 'active' : ''}`}
          >
            <Plus size={20} />
            <span>Crear Sitios</span>
          </Link>
          <Link 
            to="/sites" 
            className={`nav-item ${isActive('/sites') ? 'active' : ''}`}
          >
            <List size={20} />
            <span>Mis Sitios</span>
          </Link>
          <Link 
            to="/settings" 
            className={`nav-item ${isActive('/settings') ? 'active' : ''}`}
          >
            <Settings size={20} />
            <span>Configuración</span>
          </Link>
        </nav>
      </div>
    </header>
  )
}

export default Header

/**
 * Genera archivos style-custom.css personalizados para cada sitio
 * basándose en las paletas definidas en style.css
 */

const fs = require('fs');
const path = require('path');

// Configuración de paletas por sitio (extraídas de style.css)
const sitesConfig = {
    radiocinconoticias: {
        name: 'Radio Cinco Noticias',
        palette: {
            primary: '#AB171D',    // Brick Red
            secondary: '#91131C',  // Deep Crimson
            accent: '#BD7A7E',     // Dusty Rose
            dark: '#1A0608',
            light: '#FDF5F5',
            text: '#1A0608',
            textLight: '#7A4A4E'
        },
        fonts: {
            primary: "'Playfair Display', serif",
            secondary: "'Noto Sans', sans-serif"
        }
    },
    centralmexico: {
        name: 'Central México',
        palette: {
            primary: '#B6C1C6',    // Pale Slate
            secondary: '#8897A0',  // Cool Steel
            accent: '#9C2E3C',     // Burnt Rose
            dark: '#1A1A1A',
            light: '#F4F5F6',
            text: '#2A2A2A',
            textLight: '#5B666C'
        },
        fonts: {
            primary: "'Playfair Display', serif",
            secondary: "'Noto Sans', sans-serif"
        }
    },
    tvmexico: {
        name: 'TV México',
        palette: {
            primary: '#20131A',    // Coffee Bean
            secondary: '#5E2B37',  // Wine Plum
            accent: '#8C7A85',     // Dusty Lavender
            dark: '#160E13',
            light: '#F0E8EC',
            text: '#F0E8EC',
            textLight: '#8C7A85'
        },
        fonts: {
            primary: "'Playfair Display', serif",
            secondary: "'Noto Sans', sans-serif"
        }
    },
    cbnnoticias: {
        name: 'CBN Noticias',
        palette: {
            primary: '#003366',    // Azul marino
            secondary: '#004080',
            accent: '#FFD700',     // Dorado
            dark: '#001a33',
            light: '#F5F8FA',
            text: '#1A1A1A',
            textLight: '#5B666C'
        },
        fonts: {
            primary: "'Playfair Display', serif",
            secondary: "'Noto Sans', sans-serif"
        }
    },
    mexicoinformado: {
        name: 'México Informado',
        palette: {
            primary: '#006341',    // Verde México
            secondary: '#004d33',
            accent: '#FFD700',     // Dorado
            dark: '#001a0f',
            light: '#F0F7F4',
            text: '#1A1A1A',
            textLight: '#5B666C'
        },
        fonts: {
            primary: "'Playfair Display', serif",
            secondary: "'Noto Sans', sans-serif"
        }
    },
    nodoinformativo: {
        name: 'Nodo Informativo',
        palette: {
            primary: '#1e3a8a',    // Azul moderno
            secondary: '#1e40af',
            accent: '#60A5FA',     // Azul claro
            dark: '#0f172a',
            light: '#F0F4F8',
            text: '#1A1A1A',
            textLight: '#5B666C'
        },
        fonts: {
            primary: "'Playfair Display', serif",
            secondary: "'Noto Sans', sans-serif"
        }
    },
    bitacoraurbana: {
        name: 'Bitácora Urbana',
        palette: {
            primary: '#4a5568',    // Gris minimalista
            secondary: '#2D3748',
            accent: '#ECC94B',     // Amarillo
            dark: '#1A1A1A',
            light: '#F8F8F8',
            text: '#1A1A1A',
            textLight: '#666666'
        },
        fonts: {
            primary: "'Playfair Display', serif",
            secondary: "'Noto Sans', sans-serif"
        }
    },
    reportecentralmx: {
        name: 'Reporte Central MX',
        palette: {
            primary: '#2d3748',    // Dark profesional
            secondary: '#1A202C',
            accent: '#4299E1',     // Azul
            dark: '#0D1117',
            light: '#F7FAFC',
            text: '#1A1A1A',
            textLight: '#5B666C'
        },
        fonts: {
            primary: "'Playfair Display', serif",
            secondary: "'Noto Sans', sans-serif"
        }
    },
    verticenoticias: {
        name: 'Vértice Noticias',
        palette: {
            primary: '#9b2c2c',    // Rojo intenso
            secondary: '#7B1FA2',  // Morado
            accent: '#FFD700',     // Dorado
            dark: '#0D0D0D',
            light: '#FAFAFA',
            text: '#1A1A1A',
            textLight: '#5B666C'
        },
        fonts: {
            primary: "'Playfair Display', serif",
            secondary: "'Noto Sans', sans-serif"
        }
    },
    noticiasobjetivo: {
        name: 'Noticias Objetivo',
        palette: {
            primary: '#9b2c2c',    // Rojo intenso
            secondary: '#7B1FA2',  // Morado
            accent: '#FFD700',     // Dorado
            dark: '#0D0D0D',
            light: '#FAFAFA',
            text: '#1A1A1A',
            textLight: '#5B666C'
        },
        fonts: {
            primary: "'Playfair Display', serif",
            secondary: "'Noto Sans', sans-serif"
        }
    }
};

// Plantilla base para style-custom.css
function generateStyleCustom(siteKey, config) {
    const { name, palette, fonts } = config;
    const prefix = siteKey.charAt(0).toUpperCase() + siteKey.slice(1).replace(/-/g, '');
    
    return `/* ============================================
   ${name.toUpperCase()} - Estilo Personalizado
   Paleta personalizada
   ============================================ */

/* Paleta de colores */
:root {
    --${prefix.toLowerCase()}-primary: ${palette.primary};
    --${prefix.toLowerCase()}-secondary: ${palette.secondary};
    --${prefix.toLowerCase()}-accent: ${palette.accent};
    --${prefix.toLowerCase()}-dark: ${palette.dark};
    --${prefix.toLowerCase()}-light: ${palette.light};
    --${prefix.toLowerCase()}-text: ${palette.text};
    --${prefix.toLowerCase()}-text-light: ${palette.textLight};
}

/* Tipografía */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Noto+Sans:wght@400;500;600;700&display=swap');

body {
    font-family: ${fonts.secondary};
    background: ${palette.light};
    color: ${palette.text};
    line-height: 1.6;
}

/* ===== HEADER ===== */
.header {
    background: ${palette.dark};
    border-bottom: 3px solid ${palette.primary};
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    margin-bottom: 0;
}

.header-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 24px;
    gap: 24px;
    max-width: 1400px;
    margin: 0 auto;
    flex-wrap: wrap;
}

@media (max-width: 768px) {
    .header-container {
        flex-direction: column;
        align-items: flex-start;
    }
}

/* Logo */
.logo-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;
}

.site-logo {
    font-family: ${fonts.primary};
    font-size: 28px;
    font-weight: 700;
    color: ${palette.light};
    text-decoration: none;
    transition: opacity 0.3s ease;
}

.site-logo:hover {
    opacity: 0.8;
}

.logo-icon {
    font-size: 32px;
    color: ${palette.accent};
}

/* Navegación */
.main-nav ul {
    display: flex;
    list-style: none;
    gap: 8px;
    flex-wrap: wrap;
}

.nav-link {
    font-family: ${fonts.secondary};
    font-weight: 500;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: ${palette.light};
    padding: 8px 16px;
    border-radius: 4px;
    transition: all 0.3s ease;
}

.nav-link:hover,
.nav-link.active {
    background: ${palette.primary};
    color: ${palette.light};
}

/* Búsqueda */
.search-form {
    display: flex;
    gap: 0;
    background: rgba(255,255,255,0.1);
    border-radius: 4px;
    padding: 4px;
}

.search-input {
    background: transparent;
    border: none;
    color: ${palette.light};
    padding: 8px 12px;
    font-size: 14px;
    outline: none;
}

.search-input::placeholder {
    color: ${palette.textLight};
}

.search-button {
    background: ${palette.primary};
    border: none;
    color: ${palette.light};
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.3s ease;
}

.search-button:hover {
    background: ${palette.secondary};
}

/* ===== BREAKING NEWS ===== */
.breaking-news {
    background: ${palette.secondary};
    color: ${palette.light};
    padding: 10px 0;
    font-size: 14px;
}

.breaking-news-container {
    display: flex;
    align-items: center;
    gap: 16px;
}

.breaking-label {
    background: ${palette.primary};
    padding: 4px 12px;
    border-radius: 4px;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 12px;
    white-space: nowrap;
}

.breaking-ticker {
    flex: 1;
    overflow: hidden;
}

.breaking-ticker span {
    display: inline-block;
    animation: ticker 30s linear infinite;
}

@keyframes ticker {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}

/* ===== NEWS CARDS ===== */
.news-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 24px;
    padding: 24px 0;
}

.news-card {
    background: ${palette.light};
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.news-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.card-image-wrapper {
    position: relative;
    overflow: hidden;
    aspect-ratio: 16/9;
}

.card-image-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.news-card:hover .card-image-wrapper img {
    transform: scale(1.05);
}

.card-category-badge {
    position: absolute;
    top: 12px;
    left: 12px;
    background: ${palette.primary};
    color: ${palette.light};
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
}

.card-content {
    padding: 16px;
}

.card-title {
    font-family: ${fonts.primary};
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 8px;
    line-height: 1.4;
}

.card-title a {
    color: ${palette.text};
    transition: color 0.3s ease;
}

.card-title a:hover {
    color: ${palette.primary};
}

.card-excerpt {
    font-family: ${fonts.secondary};
    font-size: 14px;
    color: ${palette.textLight};
    line-height: 1.6;
    margin-bottom: 12px;
}

.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 12px;
    border-top: 1px solid rgba(0,0,0,0.1);
}

.card-author {
    font-size: 13px;
    color: ${palette.textLight};
}

.card-date {
    font-size: 13px;
    color: ${palette.textLight};
}

/* ===== FOOTER ===== */
.footer {
    background: ${palette.dark};
    color: ${palette.light};
    padding: 48px 0 24px;
    margin-top: 48px;
}

.footer-content {
    display: grid;
    grid-template-columns:  2fr 1fr 1fr;
    gap: 32px;
    margin-bottom: 32px;
}

.footer-section h3 {
    font-family: ${fonts.primary};
    font-size: 18px;
    margin-bottom: 16px;
    color: ${palette.accent};
}

.footer-section ul {
    list-style: none;
}

.footer-section li {
    margin-bottom: 8px;
}

.footer-section a {
    color: ${palette.light};
    transition: color 0.3s ease;
}

.footer-section a:hover {
    color: ${palette.primary};
}

.footer-bottom {
    text-align: center;
    padding-top: 24px;
    border-top: 1px solid rgba(255,255,255,0.1);
    font-size: 14px;
    color: ${palette.textLight};
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .news-grid {
        grid-template-columns: 1fr;
    }
    
    .main-nav ul {
        flex-direction: column;
        gap: 4px;
    }
    
    .search-form {
        width: 100%;
    }
    
    .search-input {
        flex: 1;
    }
}
`;
}

// Generar archivos para cada sitio
const sitesDir = path.dirname(__filename);

Object.entries(sitesConfig).forEach(([siteKey, config]) => {
    const siteDir = path.join(sitesDir, siteKey);
    const outputPath = path.join(siteDir, 'style-custom.css');
    
    const content = generateStyleCustom(siteKey, config);
    
    try {
        fs.writeFileSync(outputPath, content, 'utf8');
        console.log(`✓ Generado: ${outputPath}`);
    } catch (error) {
        console.error(`✗ Error generando ${outputPath}:`, error.message);
    }
});

console.log('\n✅ Todos los archivos style-custom.css han sido generados.');

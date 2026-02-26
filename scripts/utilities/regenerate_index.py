#!/usr/bin/env python3
"""
Regenerate all index.html files with correct image paths
"""

import os

# Get root directory from script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../../'))
SITES_DIR = os.path.join(ROOT_DIR, 'sites')

SITES = {
    'radiocinconoticias': {'name': 'Radio Cinco Noticias', 'tagline': 'Tu conexión con la actualidad', 'icon': 'fa-broadcast-tower', 'primary': '#1a1a1a'},
    'centralmexico': {'name': 'Central México', 'tagline': 'El pulso de la nación', 'icon': 'fa-newspaper', 'primary': '#004a99'},
    'tvmexico': {'name': 'TV México', 'tagline': 'Información en movimiento', 'icon': 'fa-tv', 'primary': '#c00000'},
    'cbnnoticias': {'name': 'CBN Noticias', 'tagline': 'Noticias con credibilidad', 'icon': 'fa-globe', 'primary': '#003366'},
    'mexicoinformado': {'name': 'México Informado', 'tagline': 'La verdad minuto a minuto', 'icon': 'fa-check-circle', 'primary': '#006341'},
    'nodoinformativo': {'name': 'Nodo Informativo', 'tagline': 'Conectando la información', 'icon': 'fa-network-wired', 'primary': '#1e3a8a'},
    'bitacoraurbana': {'name': 'Bitácora Urbana', 'tagline': 'Crónicas de la ciudad', 'icon': 'fa-city', 'primary': '#4a5568'},
    'reportecentralmx': {'name': 'Reporte Central MX', 'tagline': 'Análisis y profundidad', 'icon': 'fa-file-alt', 'primary': '#2d3748'},
    'verticenoticias': {'name': 'Vértice Noticias', 'tagline': 'El punto exacto de la noticia', 'icon': 'fa-crosshairs', 'primary': '#9b2c2c'},
    'noticiasobjetivo': {'name': 'Noticias Objetivo', 'tagline': 'Información sin censura', 'icon': 'fa-bullseye', 'primary': '#dc2626'}
}

def generate_index(site_slug, site_info):
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_info['name']} - {site_info['tagline']}</title>
    <meta name="description" content="{site_info['tagline']}. Noticias de México y el mundo.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;800&family=Noto+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="preloader"><div class="spinner"></div><p>Cargando noticias...</p></div>

    <header class="header">
        <div class="container header-container">
            <div class="logo-section">
                <img src="logo.png" alt="{site_slug}" class="site-logo" style="height:50px;width:auto;margin-right:15px;object-fit:contain;">
                <div>
                    <h1 class="site-title">{site_info['name']}</h1>
                    <p class="tagline">{site_info['tagline']}</p>
                </div>
            </div>
            <nav class="main-nav">
                <a href="index.html" class="nav-link active">Inicio</a>
                <a href="categoria/nacional.html" class="nav-link">Nacional</a>
                <a href="categoria/politica.html" class="nav-link">Política</a>
                <a href="categoria/economia.html" class="nav-link">Economía</a>
                <a href="categoria/deportes.html" class="nav-link">Deportes</a>
            </nav>
            <button class="search-toggle"><i class="fas fa-search"></i></button>
        </div>
    </header>

    <main class="main-content">
        <div class="container">
            <section class="breaking-news">
                <div class="breaking-label">ÚLTIMA HORA</div>
                <div class="breaking-ticker">
                    <marquee behavior="scroll" direction="left" onmouseover="this.stop();" onmouseout="this.start();">
                        <span class="ticker-item">Bienvenido a {site_info['name']} - Información verificada las 24 horas</span>
                        <span class="ticker-item">•</span>
                        <span class="ticker-item">Síguenos en redes sociales para más actualizaciones</span>
                    </marquee>
                </div>
            </section>

            <section class="featured-section">
                <div class="featured-grid layout-313">
                    <aside class="side-col left">
                        <article class="card-mini" data-article="1">
                            <img src="assets/images/article_1.jpg" alt="Noticia 1" loading="lazy">
                            <div class="card-mini-content">
                                <span class="category-badge cat-nacional">Nacional</span>
                                <h4 class="card-title">Avances en infraestructura transforman el centro del país</h4>
                                <span class="timestamp"><i class="far fa-clock"></i> Hace 2 horas</span>
                            </div>
                        </article>
                        <article class="card-mini" data-article="2">
                            <img src="assets/images/article_2.jpg" alt="Noticia 2" loading="lazy">
                            <div class="card-mini-content">
                                <span class="category-badge cat-politica">Política</span>
                                <h4 class="card-title">Nuevas reformas legislativas aprobadas en el congreso</h4>
                                <span class="timestamp"><i class="far fa-clock"></i> Hace 3 horas</span>
                            </div>
                        </article>
                        <article class="card-mini" data-article="3">
                            <img src="assets/images/article_3.jpg" alt="Noticia 3" loading="lazy">
                            <div class="card-mini-content">
                                <span class="category-badge cat-economia">Economía</span>
                                <h4 class="card-title">Mercados mexicanos cierran con ganancias históricas</h4>
                                <span class="timestamp"><i class="far fa-clock"></i> Hace 4 horas</span>
                            </div>
                        </article>
                    </aside>

                    <div class="main-col">
                        <article class="card-hero" data-article="hero">
                            <img src="assets/images/article_1.jpg" alt="Noticia Principal" loading="lazy">
                            <div class="card-hero-overlay">
                                <span class="category-badge cat-destacado">Destacado</span>
                                <h2 class="card-hero-title">Informe especial: El futuro de la tecnología en México</h2>
                                <p class="card-hero-excerpt">Un análisis profundo sobre cómo la innovación está transformando diversos sectores del país</p>
                                <div class="card-meta">
                                    <span class="author"><i class="far fa-user"></i> Redacción</span>
                                    <span class="date"><i class="far fa-calendar"></i> 19 Feb 2026</span>
                                </div>
                            </div>
                        </article>
                    </div>

                    <aside class="side-col right">
                        <article class="card-mini" data-article="4">
                            <img src="assets/images/article_4.jpg" alt="Noticia 4" loading="lazy">
                            <div class="card-mini-content">
                                <span class="category-badge cat-deportes">Deportes</span>
                                <h4 class="card-title">Selección mexicana anuncia convocatoria para próximos partidos</h4>
                                <span class="timestamp"><i class="far fa-clock"></i> Hace 5 horas</span>
                            </div>
                        </article>
                        <article class="card-mini" data-article="5">
                            <img src="assets/images/article_5.jpg" alt="Noticia 5" loading="lazy">
                            <div class="card-mini-content">
                                <span class="category-badge cat-nacional">Nacional</span>
                                <h4 class="card-title">Inauguran nuevo centro cultural en la capital</h4>
                                <span class="timestamp"><i class="far fa-clock"></i> Hace 6 horas</span>
                            </div>
                        </article>
                        <article class="card-mini" data-article="6">
                            <img src="assets/images/article_6.jpg" alt="Noticia 6" loading="lazy">
                            <div class="card-mini-content">
                                <span class="category-badge cat-politica">Política</span>
                                <h4 class="card-title">Debate nacional sobre políticas públicas se instala hoy</h4>
                                <span class="timestamp"><i class="far fa-clock"></i> Hace 7 horas</span>
                            </div>
                        </article>
                    </aside>
                </div>
            </section>

            <section class="news-section">
                <h2 class="section-title">Más Noticias</h2>
                <div class="news-grid news-grid-3">
                    <article class="news-card" data-article="7">
                        <div class="card-image-wrapper">
                            <img src="assets/images/article_7.jpg" alt="Noticia 7" loading="lazy">
                            <span class="card-category-badge cat-nacional">Nacional</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title"><a href="articulo/nota-1.html">Programas de apoyo impulsan emprendedores locales</a></h3>
                            <p class="card-excerpt">Iniciativas gubernamentales y privadas se unen para fomentar el desarrollo empresarial.</p>
                            <div class="card-footer">
                                <span class="card-author">Por Redacción</span>
                                <span class="card-date">19 Feb 2026</span>
                            </div>
                        </div>
                    </article>

                    <article class="news-card" data-article="8">
                        <div class="card-image-wrapper">
                            <img src="assets/images/article_8.jpg" alt="Noticia 8" loading="lazy">
                            <span class="card-category-badge cat-economia">Economía</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title"><a href="articulo/nota-2.html">Bolsa Mexicana registra alzas en sector tecnológico</a></h3>
                            <p class="card-excerpt">Las empresas de tecnología lideran las ganancias en la jornada bursátil.</p>
                            <div class="card-footer">
                                <span class="card-author">Por Economía</span>
                                <span class="card-date">19 Feb 2026</span>
                            </div>
                        </div>
                    </article>

                    <article class="news-card" data-article="9">
                        <div class="card-image-wrapper">
                            <img src="assets/images/article_9.jpg" alt="Noticia 9" loading="lazy">
                            <span class="card-category-badge cat-deportes">Deportes</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title"><a href="articulo/nota-3.html">Liga MX: Resultados y posiciones de la jornada 8</a></h3>
                            <p class="card-excerpt">Conoce los resultados completos y cómo queda la tabla general.</p>
                            <div class="card-footer">
                                <span class="card-author">Por Deportes</span>
                                <span class="card-date">19 Feb 2026</span>
                            </div>
                        </div>
                    </article>

                    <article class="news-card" data-article="10">
                        <div class="card-image-wrapper">
                            <img src="assets/images/article_10.jpg" alt="Noticia 10" loading="lazy">
                            <span class="card-category-badge cat-politica">Política</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title"><a href="articulo/nota-4.html">Comisión de energía debate nueva reforma del sector</a></h3>
                            <p class="card-excerpt">Legisladores discuten los alcances de la propuesta energética.</p>
                            <div class="card-footer">
                                <span class="card-author">Por Redacción</span>
                                <span class="card-date">19 Feb 2026</span>
                            </div>
                        </div>
                    </article>

                    <article class="news-card" data-article="11">
                        <div class="card-image-wrapper">
                            <img src="assets/images/article_11.jpg" alt="Noticia 11" loading="lazy">
                            <span class="card-category-badge cat-nacional">Nacional</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title"><a href="articulo/nota-5.html">Turismo en México supera expectativas del 2025</a></h3>
                            <p class="card-excerpt">El sector turístico reporta cifras récord en visitantes.</p>
                            <div class="card-footer">
                                <span class="card-author">Por Turismo</span>
                                <span class="card-date">18 Feb 2026</span>
                            </div>
                        </div>
                    </article>

                    <article class="news-card" data-article="12">
                        <div class="card-image-wrapper">
                            <img src="assets/images/article_12.jpg" alt="Noticia 12" loading="lazy">
                            <span class="card-category-badge cat-economia">Economía</span>
                        </div>
                        <div class="card-content">
                            <h3 class="card-title"><a href="articulo/nota-6.html">Banco de México reporta estabilidad en inflación</a></h3>
                            <p class="card-excerpt">El banco central mantiene su política monetaria.</p>
                            <div class="card-footer">
                                <span class="card-author">Por Economía</span>
                                <span class="card-date">18 Feb 2026</span>
                            </div>
                        </div>
                    </article>
                </div>
            </section>
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <div class="footer-grid cols-3">
                <div class="footer-column">
                    <div class="footer-logo"><i class="fas {site_info['icon']}"></i><h3>{site_info['name']}</h3></div>
                    <p class="footer-about">{site_info['tagline']}. Información veraz y oportuna.</p>
                    <div class="social-links">
                        <a href="#" class="social-link"><i class="fab fa-facebook-f"></i></a>
                        <a href="#" class="social-link"><i class="fab fa-twitter"></i></a>
                        <a href="#" class="social-link"><i class="fab fa-instagram"></i></a>
                        <a href="#" class="social-link"><i class="fab fa-youtube"></i></a>
                    </div>
                </div>
                <div class="footer-column">
                    <h4>Secciones</h4>
                    <ul class="footer-links">
                        <li><a href="categoria/nacional.html">Nacional</a></li>
                        <li><a href="categoria/politica.html">Política</a></li>
                        <li><a href="categoria/economia.html">Economía</a></li>
                        <li><a href="categoria/deportes.html">Deportes</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h4>Información</h4>
                    <ul class="footer-links">
                        <li><a href="acerca-de.html">Acerca de</a></li>
                        <li><a href="contacto.html">Contacto</a></li>
                        <li><a href="privacidad.html">Privacidad</a></li>
                        <li><a href="terminos.html">Términos</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 {site_info['name']}. Todos los derechos reservados.</p>
                <p class="disclaimer">Este sitio publica contenidos con fines informativos. Las opiniones expresadas pertenecen a sus autores.</p>
            </div>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>
'''

for slug, info in SITES.items():
    index_path = os.path.join(SITES_DIR, slug, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(generate_index(slug, info))
    print(f"✅ {slug}: index.html regenerado")

print("\n✅ Todos los index.html regenerados correctamente")

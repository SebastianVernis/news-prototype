#!/bin/bash
# Update legal pages for all new sites

SITES_DIR="/home/sebastianvernis/cloudflare-news-project/sites/Nuevos"
STABLE_DIR="/home/sebastianvernis/cloudflare-news-project/sites/Estables/radiocinconoticias"

# Copy legal.css from stable
echo "Copying legal.css..."
for site in boominformativo capitalpress diarioexpress elpulsomexicano enfoquecapital enfoquedirecto formulacdmx mexicantimes mexico360noticias mradio noticiashorizonte pulsodiario puntoclave puntonoticias radarinformativo reportediario televisionabc; do
  cp "$STABLE_DIR/legal.css" "$SITES_DIR/$site/legal.css"
done
echo "✓ legal.css copied"

# Create terminos.html for each site
echo "Creating terminos.html..."
for site in boominformativo capitalpress diarioexpress elpulsomexicano enfoquecapital enfoquedirecto formulacdmx mexicantimes mexico360noticias mradio noticiashorizonte pulsodiario puntoclave puntonoticias radarinformativo reportediario televisionabc; do
  # Get site name from directory
  SITE_NAME=$(echo "$site" | sed 's/[0-9]//g' | sed 's/_/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')
  
  # Get domain
  DOMAIN=$(wrangler d1 execute news_db --command "SELECT DOMINIO FROM SITIOS WHERE SLUG='$site'" --remote 2>/dev/null | grep -oP '(?<=│ )[^\s]+(?= \|)' | tail -1)
  [ -z "$DOMAIN" ] && DOMAIN="$site.click"
  
  cat > "$SITES_DIR/$site/terminos.html" << EOF
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Términos de Uso - $SITE_NAME</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="style-custom.css">
    <link rel="stylesheet" href="legal.css">
</head>
<body>
    <div id="site-preloader"></div>
    <div id="site-header"></div>

    <main class="main-content legal-page">
        <div class="container">
            <article class="legal-content">
                <h1>Términos de Uso</h1>
                <p class="last-updated">Última actualización: enero 2026</p>
                <section class="legal-section">
                    <h2>1. Aceptación de los Términos</h2>
                    <p>Al acceder y utilizar $SITE_NAME, aceptas estar sujeto a estos términos de uso. Si no estás de acuerdo con alguno de estos términos, no debes usar este sitio.</p>
                </section>
                <section class="legal-section">
                    <h2>2. Uso del Contenido</h2>
                    <p>El contenido publicado en $SITE_NAME es para uso informativo personal. Queda prohibida la reproducción total o parcial sin autorización expresa.</p>
                </section>
                <section class="legal-section">
                    <h2>3. Propiedad Intelectual</h2>
                    <p>Todos los contenidos, incluyendo textos, imágenes y logotipos, son propiedad de $SITE_NAME o de sus respectivos autores y están protegidos por las leyes de propiedad intelectual.</p>
                </section>
                <section class="legal-section">
                    <h2>4. Limitación de Responsabilidad</h2>
                    <p>$SITE_NAME no se hace responsable de los daños directos o indirectos derivados del uso o imposibilidad de uso de este sitio web.</p>
                </section>
                <section class="legal-section">
                    <h2>5. Modificaciones</h2>
                    <p>Nos reservamos el derecho de modificar estos términos en cualquier momento. Las modificaciones entrarán en vigor desde su publicación en el sitio.</p>
                </section>
                <section class="legal-section">
                    <h2>6. Contacto</h2>
                    <p>Para consultas sobre estos términos: <a href="mailto:contacto@$DOMAIN">contacto@$DOMAIN</a></p>
                </section>
            </article>
        </div>
    </main>

    <div id="site-footer"></div>

    <script src="script.js"></script>
    <script src="components.js"></script>
</body>
</html>
EOF
  echo "  ✓ $site terminos.html"
done

# Create privacidad.html for each site
echo "Creating privacidad.html..."
for site in boominformativo capitalpress diarioexpress elpulsomexicano enfoquecapital enfoquedirecto formulacdmx mexicantimes mexico360noticias mradio noticiashorizonte pulsodiario puntoclave puntonoticias radarinformativo reportediario televisionabc; do
  SITE_NAME=$(echo "$site" | sed 's/[0-9]//g' | sed 's/_/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')
  DOMAIN=$(wrangler d1 execute news_db --command "SELECT DOMINIO FROM SITIOS WHERE SLUG='$site'" --remote 2>/dev/null | grep -oP '(?<=│ )[^\s]+(?= \|)' | tail -1)
  [ -z "$DOMAIN" ] && DOMAIN="$site.click"
  
  cat > "$SITES_DIR/$site/privacidad.html" << EOF
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Política de Privacidad - $SITE_NAME</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="style-custom.css">
    <link rel="stylesheet" href="legal.css">
</head>
<body>
    <div id="site-preloader"></div>
    <div id="site-header"></div>

    <main class="main-content legal-page">
        <div class="container">
            <article class="legal-content">
                <h1>Política de Privacidad</h1>
                <p class="last-updated">Última actualización: enero 2026</p>
                <section class="legal-section">
                    <h2>1. Información que Recopilamos</h2>
                    <p>$SITE_NAME recopila información mínima necesaria para el funcionamiento del sitio. No recopilamos datos personales sin tu consentimiento explícito.</p>
                </section>
                <section class="legal-section">
                    <h2>2. Uso de Cookies</h2>
                    <p>Utilizamos cookies técnicas esenciales para el funcionamiento del sitio y cookies analíticas anónimas para mejorar la experiencia del usuario.</p>
                </section>
                <section class="legal-section">
                    <h2>3. Compartir Información</h2>
                    <p>No vendemos, intercambiamos ni transferimos tu información personal a terceros sin tu consentimiento, excepto cuando sea requerido por ley.</p>
                </section>
                <section class="legal-section">
                    <h2>4. Seguridad</h2>
                    <p>Implementamos medidas de seguridad apropiadas para proteger tu información contra acceso no autorizado, alteración o divulgación.</p>
                </section>
                <section class="legal-section">
                    <h2>5. Tus Derechos</h2>
                    <p>Tienes derecho a acceder, rectificar y eliminar tus datos personales. Para ejercer estos derechos, contáctanos en: contacto@$DOMAIN</p>
                </section>
                <section class="legal-section">
                    <h2>6. Contacto</h2>
                    <p>Para preguntas sobre esta política: <a href="mailto:contacto@$DOMAIN">contacto@$DOMAIN</a></p>
                </section>
            </article>
        </div>
    </main>

    <div id="site-footer"></div>

    <script src="script.js"></script>
    <script src="components.js"></script>
</body>
</html>
EOF
  echo "  ✓ $site privacidad.html"
done

# Create contacto.html for each site
echo "Creating contacto.html..."
for site in boominformativo capitalpress diarioexpress elpulsomexicano enfoquecapital enfoquedirecto formulacdmx mexicantimes mexico360noticias mradio noticiashorizonte pulsodiario puntoclave puntonoticias radarinformativo reportediario televisionabc; do
  SITE_NAME=$(echo "$site" | sed 's/[0-9]//g' | sed 's/_/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')
  DOMAIN=$(wrangler d1 execute news_db --command "SELECT DOMINIO FROM SITIOS WHERE SLUG='$site'" --remote 2>/dev/null | grep -oP '(?<=│ )[^\s]+(?= \|)' | tail -1)
  [ -z "$DOMAIN" ] && DOMAIN="$site.click"
  
  cat > "$SITES_DIR/$site/contacto.html" << EOF
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contacto - $SITE_NAME</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="style-custom.css">
    <link rel="stylesheet" href="legal.css">
</head>
<body>
    <div id="site-preloader"></div>
    <div id="site-header"></div>

    <main class="main-content legal-page">
        <div class="container">
            <article class="legal-content">
                <h1>Contacto</h1>
                <p class="last-updated">$SITE_NAME</p>
                <section class="legal-section">
                    <h2>Información de Contacto</h2>
                    <ul>
                        <li><strong>Email general:</strong> contacto@$DOMAIN</li>
                        <li><strong>Noticias y tips:</strong> noticias@$DOMAIN</li>
                        <li><strong>Publicidad:</strong> publicidad@$DOMAIN</li>
                    </ul>
                </section>
                <section class="legal-section">
                    <h2>Envíanos un Mensaje</h2>
                    <p>Si tienes una noticia, corrección o comentario, escríbenos a <a href="mailto:contacto@$DOMAIN">contacto@$DOMAIN</a>. Respondemos en un plazo de 24 a 48 horas hábiles.</p>
                </section>
                <section class="legal-section">
                    <h2>Redes Sociales</h2>
                    <p>También puedes encontrarnos en nuestras redes sociales para estar al tanto de las últimas noticias.</p>
                </section>
            </article>
        </div>
    </main>

    <div id="site-footer"></div>

    <script src="script.js"></script>
    <script src="components.js"></script>
</body>
</html>
EOF
  echo "  ✓ $site contacto.html"
done

echo ""
echo "✅ All legal pages updated!"

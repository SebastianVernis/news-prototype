// Generates legal pages: acerca-de, contacto, privacidad, terminos

function genLegalPage(site, type) {
    var titles = {
        'acerca-de': 'Acerca de ' + site.name,
        'contacto': 'Contacto',
        'privacidad': 'Aviso de Privacidad',
        'terminos': 'Terminos y Condiciones'
    };
    var title = titles[type] || type;
    var bodyContent = getLegalBody(site, type);

    var html = '<!DOCTYPE html>\n<html lang="es">\n<head>\n';
    html += '    <meta charset="UTF-8">\n';
    html += '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n';
    html += '    <title>' + title + ' - ' + site.name + '</title>\n';
    html += '    <link rel="preconnect" href="https://fonts.googleapis.com">\n';
    html += '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n';
    html += '    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">\n';
    html += '    <link rel="stylesheet" href="style.css">\n';
    html += '    <link rel="stylesheet" href="style-custom.css">\n';
    html += '    <link rel="stylesheet" href="legal.css">\n';
    html += '</head>\n<body>\n';
    html += '    <div id="site-preloader"></div>\n';
    html += '    <div id="site-header"></div>\n\n';
    html += '    <main class="main-content legal-page">\n';
    html += '        <div class="container">\n';
    html += '            <article class="legal-content">\n';
    html += '                <h1>' + title + '</h1>\n';
    html += '                <p class="last-updated">' + site.name + '</p>\n';
    html += bodyContent;
    html += '            </article>\n';
    html += '        </div>\n';
    html += '    </main>\n\n';
    html += '    <div id="site-footer"></div>\n\n';
    html += '    <script src="script.js"></script>\n';
    html += '    <script src="components.js"></script>\n';
    html += '</body>\n</html>';
    return html;
}

function getLegalBody(site, type) {
    if (type === 'acerca-de') {
        return '                <section class="legal-section">\n' +
            '                    <h2>Nuestra Mision</h2>\n' +
            '                    <p>En ' + site.name + ' nos dedicamos a proporcionar informacion veraz, oportuna y objetiva. Nuestro compromiso es con la verdad y el periodismo de calidad.</p>\n' +
            '                </section>\n' +
            '                <section class="legal-section">\n' +
            '                    <h2>Nuestra Historia</h2>\n' +
            '                    <p>Fundado en 2026, ' + site.name + ' ha crecido hasta convertirse en una fuente confiable de noticias para miles de lectores en todo Mexico.</p>\n' +
            '                </section>\n' +
            '                <section class="legal-section">\n' +
            '                    <h2>Nuestros Valores</h2>\n' +
            '                    <ul>\n' +
            '                        <li><strong>Veracidad:</strong> Compromiso con la informacion verificada</li>\n' +
            '                        <li><strong>Objetividad:</strong> Presentamos los hechos sin sesgos</li>\n' +
            '                        <li><strong>Responsabilidad:</strong> Asumimos la responsabilidad de nuestro contenido</li>\n' +
            '                        <li><strong>Respeto:</strong> Tratamos con dignidad a nuestras fuentes y lectores</li>\n' +
            '                    </ul>\n' +
            '                </section>\n';
    }
    if (type === 'contacto') {
        return '                <section class="legal-section">\n' +
            '                    <h2>Informacion de Contacto</h2>\n' +
            '                    <ul>\n' +
            '                        <li><strong>Email general:</strong> contacto@' + site.slug + '.lat</li>\n' +
            '                        <li><strong>Noticias y tips:</strong> noticias@' + site.slug + '.lat</li>\n' +
            '                        <li><strong>Publicidad:</strong> publicidad@' + site.slug + '.lat</li>\n' +
            '                    </ul>\n' +
            '                </section>\n' +
            '                <section class="legal-section">\n' +
            '                    <h2>Envianos un Mensaje</h2>\n' +
            '                    <p>Si tienes una noticia, correccion o comentario, escribenos a contacto@' + site.slug + '.lat</p>\n' +
            '                </section>\n';
    }
    if (type === 'privacidad') {
        return '                <section class="legal-section">\n' +
            '                    <h2>Recopilacion de Datos</h2>\n' +
            '                    <p>' + site.name + ' recopila informacion limitada para mejorar la experiencia del usuario. No vendemos ni compartimos datos personales con terceros.</p>\n' +
            '                </section>\n' +
            '                <section class="legal-section">\n' +
            '                    <h2>Cookies</h2>\n' +
            '                    <p>Utilizamos cookies esenciales para el funcionamiento del sitio y cookies analiticas para entender como los usuarios interactuan con nuestro contenido.</p>\n' +
            '                </section>\n' +
            '                <section class="legal-section">\n' +
            '                    <h2>Derechos del Usuario</h2>\n' +
            '                    <p>Los usuarios tienen derecho a solicitar la eliminacion de sus datos personales en cualquier momento.</p>\n' +
            '                </section>\n';
    }
    if (type === 'terminos') {
        return '                <section class="legal-section">\n' +
            '                    <h2>Uso del Sitio</h2>\n' +
            '                    <p>Al acceder y utilizar ' + site.name + ', usted acepta estos terminos y condiciones. El contenido publicado es para fines informativos unicamente.</p>\n' +
            '                </section>\n' +
            '                <section class="legal-section">\n' +
            '                    <h2>Propiedad Intelectual</h2>\n' +
            '                    <p>Todo el contenido publicado en ' + site.name + ' esta protegido por derechos de autor. Queda prohibida la reproduccion total o parcial sin autorizacion previa.</p>\n' +
            '                </section>\n' +
            '                <section class="legal-section">\n' +
            '                    <h2>Limitacion de Responsabilidad</h2>\n' +
            '                    <p>' + site.name + ' no se hace responsable por decisiones tomadas basandose en la informacion publicada en este sitio.</p>\n' +
            '                </section>\n';
    }
    return '';
}

module.exports = genLegalPage;

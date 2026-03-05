var { API_BASE, CATS } = require('./config');

// ── LEGAL PAGES ──
function genLegal(site, type) {
    var n = site.name, s = site.slug;
    var titles = {
        'acerca-de': 'Acerca de',
        'contacto': 'Contacto',
        'privacidad': 'Aviso de Privacidad',
        'terminos': 'Términos y Condiciones'
    };
    var contents = {
        'acerca-de': '<h2>Nuestra Misión</h2><p>En ' + n + ' nos dedicamos a proporcionar información veraz, oportuna y objetiva a nuestros lectores.</p><h2>Nuestros Valores</h2><ul><li><strong>Veracidad:</strong> Compromiso con la información verificada</li><li><strong>Objetividad:</strong> Presentamos los hechos sin sesgos</li><li><strong>Responsabilidad:</strong> Asumimos la responsabilidad de nuestro contenido</li></ul>',
        'contacto': '<h2>Información de Contacto</h2><p>Email: contacto@' + s + '.lat</p><p>Para consultas editoriales, colaboraciones o reportar errores en nuestro contenido, no dude en comunicarse con nosotros.</p>',
        'privacidad': '<h2>Recopilación de Datos</h2><p>' + n + ' recopila información limitada para mejorar la experiencia del usuario.</p><h2>Uso de Cookies</h2><p>Utilizamos cookies esenciales para el funcionamiento del sitio.</p><h2>Derechos del Usuario</h2><p>Puede solicitar la eliminación de sus datos en cualquier momento contactándonos.</p>',
        'terminos': '<h2>Uso del Sitio</h2><p>Al acceder a ' + n + ', acepta estos términos y condiciones de uso.</p><h2>Propiedad Intelectual</h2><p>Todo el contenido publicado es propiedad de ' + n + ' o sus respectivos autores.</p><h2>Limitación de Responsabilidad</h2><p>' + n + ' no se hace responsable por decisiones tomadas con base en la información publicada.</p>'
    };
    var lines = [];
    lines.push('<!DOCTYPE html><html lang="es"><head>');
    lines.push('<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">');
    lines.push('<title>' + titles[type] + ' - ' + n + '</title>');
    lines.push('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">');
    lines.push('<link href="style-custom.css" rel="stylesheet">');
    lines.push('<style>');
    lines.push('.legal-page{max-width:800px;margin:40px auto;padding:0 24px;font-family:sans-serif;line-height:1.8;}');
    lines.push('.legal-page h1{font-size:2rem;margin-bottom:10px;}');
    lines.push('.legal-page h2{font-size:1.3rem;margin:25px 0 10px;}');
    lines.push('.legal-page p,.legal-page li{color:#555;font-size:1rem;}');
    lines.push('.legal-page ul{padding-left:20px;}');
    lines.push('</style>');
    lines.push('</head><body>');
    lines.push('<div id="site-preloader"></div><div id="site-header"></div>');
    lines.push('<main class="legal-page">');
    lines.push('<h1>' + titles[type] + '</h1>');
    lines.push(contents[type]);
    lines.push('</main>');
    lines.push('<div id="site-footer"></div>');
    lines.push('<script src="components.js"></script>');
    lines.push('</body></html>');
    return lines.join('\n');
}

// ── ARTICULO PAGE ──
function genArticulo(site) {
    var s = site.slug, n = site.name;
    var lines = [];
    lines.push('<!DOCTYPE html><html lang="es"><head>');
    lines.push('<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">');
    lines.push('<title>Artículo - ' + n + '</title>');
    lines.push('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">');
    lines.push('<link href="../style-custom.css" rel="stylesheet">');
    lines.push('<style>');
    lines.push('.article-page{max-width:800px;margin:40px auto;padding:0 24px;font-family:sans-serif;line-height:1.8;}');
    lines.push('.article-page h1{font-size:2.2rem;margin-bottom:15px;}');
    lines.push('.article-page .meta{color:#888;font-size:0.9rem;margin-bottom:20px;}');
    lines.push('.article-page .feat-img{width:100%;max-height:450px;object-fit:cover;border-radius:8px;margin-bottom:25px;}');
    lines.push('.article-page .content{font-size:1.05rem;color:#333;}');
    lines.push('.article-page .content p{margin-bottom:15px;}');
    lines.push('</style>');
    lines.push('</head><body>');
    lines.push('<div id="site-preloader"></div><div id="site-header"></div>');
    lines.push('<main class="article-page">');
    lines.push('<div id="article-content"><p style="text-align:center;padding:60px;">Cargando artículo...</p></div>');
    lines.push('</main>');
    lines.push('<div id="site-footer"></div>');
    lines.push('<script src="../components.js"></script>');
    lines.push('<script>');
    lines.push('(function(){');
    lines.push('    var params=new URLSearchParams(window.location.search);');
    lines.push('    var slug=params.get("slug");if(!slug)return;');
    lines.push('    fetch("' + API_BASE + '/api/articles/"+encodeURIComponent(slug)+"?site=' + s + '")');
    lines.push('    .then(function(r){return r.json();})');
    lines.push('    .then(function(d){');
    lines.push('        var a=d.article||d;if(!a||!a.title)return;');
    lines.push('        document.title=a.title+" - ' + n + '";');
    lines.push('        var h="<h1>"+a.title+"</h1>";');
    lines.push('        h+=\'<div class="meta"><span><i class="far fa-user"></i> \'+(a.author||"Redacción")+\'</span> &bull; <span><i class="far fa-calendar"></i> \'+(a.publishedAt?new Date(a.publishedAt).toLocaleDateString("es-MX"):"")+\'</span> &bull; <span>\'+(a.category||"General")+\'</span></div>\';');
    lines.push('        if(a.imageUrl)h+=\'<img class="feat-img" src="\'+a.imageUrl+\'" alt="">\';');
    lines.push('        h+=\'<div class="content">\'+(a.content||a.excerpt||"")+\'</div>\';');
    lines.push('        document.getElementById("article-content").innerHTML=h;');
    lines.push('    }).catch(function(e){console.error(e);});');
    lines.push('})();');
    lines.push('</script>');
    lines.push('</body></html>');
    return lines.join('\n');
}

// ── CATEGORIA PAGE ──
function genCategoria(site, cat) {
    var s = site.slug, n = site.name;
    var catLabel = cat.charAt(0).toUpperCase() + cat.slice(1);
    var lines = [];
    lines.push('<!DOCTYPE html><html lang="es"><head>');
    lines.push('<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">');
    lines.push('<title>' + catLabel + ' - ' + n + '</title>');
    lines.push('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">');
    lines.push('<link href="../style-custom.css" rel="stylesheet">');
    lines.push('<style>');
    lines.push('.cat-page{max-width:1200px;margin:40px auto;padding:0 24px;font-family:sans-serif;}');
    lines.push('.cat-page h1{font-size:2rem;margin-bottom:30px;}');
    lines.push('.cat-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:24px;}');
    lines.push('.cat-card{background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.1);transition:transform 0.2s;}');
    lines.push('.cat-card:hover{transform:translateY(-4px);}');
    lines.push('.cat-card img{width:100%;height:200px;object-fit:cover;}');
    lines.push('.cat-card-body{padding:16px;}');
    lines.push('.cat-card-body h3{font-size:1.1rem;margin-bottom:8px;}');
    lines.push('.cat-card-body h3 a{color:inherit;text-decoration:none;}');
    lines.push('.cat-card-body p{color:#666;font-size:0.9rem;}');
    lines.push('</style>');
    lines.push('</head><body>');
    lines.push('<div id="site-preloader"></div><div id="site-header"></div>');
    lines.push('<main class="cat-page">');
    lines.push('<h1>' + catLabel + '</h1>');
    lines.push('<div id="cat-grid" class="cat-grid"><p>Cargando...</p></div>');
    lines.push('</main>');
    lines.push('<div id="site-footer"></div>');
    lines.push('<script src="../components.js"></script>');
    lines.push('<script>');
    lines.push('(function(){');
    lines.push('    fetch("' + API_BASE + '/api/articles?site=' + s + '&category=' + cat + '&limit=20")');
    lines.push('    .then(function(r){return r.json();})');
    lines.push('    .then(function(d){');
    lines.push('        var arts=d.articles;');
    lines.push('        if(!arts||!arts.length){document.getElementById("cat-grid").innerHTML="<p>No hay noticias en esta categoría.</p>";return;}');
    lines.push('        document.getElementById("cat-grid").innerHTML=arts.map(function(a){');
    lines.push('            return \'<article class="cat-card">\'+');
    lines.push('                (a.imageUrl?\'<img src="\'+a.imageUrl+\'" alt="" loading="lazy">\':"")+');
    lines.push('                \'<div class="cat-card-body">\'+');
    lines.push('                \'<h3><a href="../articulo/index.html?slug=\'+encodeURIComponent(a.slug)+\'">\'+');
    lines.push('                (a.title||"").replace(/&/g,"&amp;").replace(/</g,"&lt;")+');
    lines.push('                \'</a></h3>\'+');
    lines.push('                \'<p>\'+(a.excerpt||"").replace(/&/g,"&amp;").replace(/</g,"&lt;")+\'</p>\'+');
    lines.push('                \'</div></article>\';');
    lines.push('        }).join("");');
    lines.push('    }).catch(function(e){console.error(e);});');
    lines.push('})();');
    lines.push('</script>');
    lines.push('</body></html>');
    return lines.join('\n');
}

module.exports = { genLegal, genArticulo, genCategoria };

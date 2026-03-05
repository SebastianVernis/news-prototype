var { API_BASE } = require('./config');

/**
 * Generates index.html preserving original <main> layout,
 * adding API integration script to populate content dynamically
 */
function genIndex(site, mainHTML) {
    var s = site.slug, n = site.name;
    var lines = [];
    lines.push('<!DOCTYPE html>');
    lines.push('<html lang="es">');
    lines.push('<head>');
    lines.push('    <meta charset="UTF-8">');
    lines.push('    <meta name="viewport" content="width=device-width, initial-scale=1.0">');
    lines.push('    <title>' + n + ' - Noticias en Tiempo Real</title>');
    lines.push('    <meta name="description" content="' + n + ' - Noticias digitales en tiempo real.">');
    lines.push('    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">');
    lines.push('    <link href="style-custom.css" rel="stylesheet">');
    lines.push('    <link rel="alternate" type="application/rss+xml" title="' + n + ' RSS" href="/rss.xml">');
    lines.push('</head>');
    lines.push('<body>');
    lines.push('');
    lines.push('<div id="site-preloader"></div>');
    lines.push('<div id="site-header"></div>');
    lines.push('');
    lines.push(mainHTML);
    lines.push('');
    lines.push('<div id="site-footer"></div>');
    lines.push('');
    lines.push('<script src="components.js"></script>');
    lines.push('<script src="script.js"></script>');
    lines.push('<script>');
    lines.push(genAPIScript(s));
    lines.push('</script>');
    lines.push('');
    lines.push('</body>');
    lines.push('</html>');
    return lines.join('\n');
}

function genAPIScript(slug) {
    // This script fetches articles from the API and populates the ORIGINAL layout
    // It finds article containers, headings, paragraphs, image placeholders, etc.
    // and replaces their content with real API data
    var s = '';
    s += '(function() {\n';
    s += '    var API = "' + API_BASE + '/api/articles?site=' + slug + '&limit=20";\n';
    s += '    function esc(t){if(!t)return"";return String(t).replace(/&/g,"\\&amp;").replace(/</g,"\\&lt;").replace(/>/g,"\\&gt;");}\n';
    s += '    function enc(t){return encodeURIComponent(t||"");}\n';
    s += '\n';
    s += '    async function load(){\n';
    s += '        try{\n';
    s += '            var r=await fetch(API);if(!r.ok)throw new Error("err");\n';
    s += '            var d=await r.json();var arts=d.articles;\n';
    s += '            if(!arts||!arts.length)return;\n';
    s += '            populate(arts);\n';
    s += '        }catch(e){console.error("Error:",e);}\n';
    s += '    }\n';
    s += '\n';
    s += '    function populate(arts){\n';
    s += '        var main=document.querySelector("main");if(!main)return;\n';
    s += '        var ai=0;\n';
    s += '\n';
    s += '        // Find all article-like containers in the original layout\n';
    s += '        var containers=main.querySelectorAll(\n';
    s += '            "article, .hero, .hero-content, .hero-text, .hero-text-box, .hero-headline,"\n';
    s += '            +".z-content, .focus-section, .side-item, .side-article, .grid-item,"\n';
    s += '            +".scroll-content, .video-card, .minimal-card, .gallery-card, .classic-card,"\n';
    s += '            +".card, .card-body, .brief-card, .tech-card, .grid-card, .scroll-card,"\n';
    s += '            +".hero-card > .hero-content, .hero-section .hero-content"\n';
    s += '        );\n';
    s += '\n';
    s += '        // Deduplicate: skip children if parent is already in list\n';
    s += '        var seen=new Set();\n';
    s += '        var unique=[];\n';
    s += '        containers.forEach(function(el){\n';
    s += '            // Skip if a parent is already in our list\n';
    s += '            var dominated=false;\n';
    s += '            seen.forEach(function(s){\n';
    s += '                if(s.contains(el)&&s!==el)dominated=true;\n';
    s += '            });\n';
    s += '            if(!dominated){unique.push(el);seen.add(el);}\n';
    s += '        });\n';
    s += '\n';
    s += '        unique.forEach(function(el){\n';
    s += '            if(ai>=arts.length)return;\n';
    s += '            var a=arts[ai];\n';
    s += '            var link="articulo/index.html?slug="+enc(a.slug);\n';
    s += '\n';
    s += '            // Populate heading\n';
    s += '            var heading=el.querySelector("h1,h2,h3,h4");\n';
    s += '            if(heading){\n';
    s += '                heading.innerHTML=\'<a href="\'+link+\'" style="color:inherit;text-decoration:none;">\'+esc(a.title)+\'</a>\';\n';
    s += '            }\n';
    s += '\n';
    s += '            // Populate excerpt\n';
    s += '            var para=el.querySelector("p:not(.author-meta):not(.img-caption)");\n';
    s += '            if(para&&a.excerpt)para.textContent=a.excerpt;\n';
    s += '\n';
    s += '            // Populate category tag\n';
    s += '            var tag=el.querySelector(".tag,.tag-pill,.category-tag,.category,.category-label,.category-pill,.hero-tag,.card-meta");\n';
    s += '            if(tag&&a.category)tag.textContent=a.category;\n';
    s += '\n';
    s += '            // Populate image placeholder (background-image on div)\n';
    s += '            var imgDiv=el.querySelector("div[class*=img],div[class*=image],div[class*=thumb],div[class*=placeholder]");\n';
    s += '            if(imgDiv&&a.imageUrl){\n';
    s += '                imgDiv.style.backgroundImage="url("+a.imageUrl+")";\n';
    s += '                imgDiv.style.backgroundSize="cover";\n';
    s += '                imgDiv.style.backgroundPosition="center";\n';
    s += '            }\n';
    s += '\n';
    s += '            // Fix read-more links\n';
    s += '            var rm=el.querySelector("a.read-more,a.read-link,a.btn-outline,a.read-btn,a[href=\'#\']");\n';
    s += '            if(rm)rm.href=link;\n';
    s += '\n';
    s += '            ai++;\n';
    s += '        });\n';
    s += '\n';
    s += '        // Populate numbered lists (Swiss Design, etc.)\n';
    s += '        var listItems=main.querySelectorAll(".numbered-list li,.trending-list li");\n';
    s += '        listItems.forEach(function(el,i){\n';
    s += '            if(!arts[i])return;\n';
    s += '            var span=el.querySelector("span");\n';
    s += '            if(span)span.textContent=arts[i].title;\n';
    s += '            else el.textContent=arts[i].title;\n';
    s += '        });\n';
    s += '\n';
    s += '        // Populate marquee/ticker\n';
    s += '        var marquee=main.querySelector(".marquee,marquee");\n';
    s += '        if(marquee)marquee.textContent=arts.slice(0,5).map(function(a){return"+++ "+a.title.toUpperCase();}).join(" ");\n';
    s += '\n';
    s += '        // Populate newspaper columns\n';
    s += '        var cols=main.querySelector(".newspaper-columns");\n';
    s += '        if(cols&&arts[0]){\n';
    s += '            var credit=cols.querySelector(".author-credit");\n';
    s += '            if(credit&&arts[0].author)credit.textContent="Por "+arts[0].author;\n';
    s += '            var paras=cols.querySelectorAll("p");\n';
    s += '            paras.forEach(function(p,i){if(arts[i]&&arts[i].excerpt)p.textContent=arts[i].excerpt;});\n';
    s += '        }\n';
    s += '    }\n';
    s += '\n';
    s += '    if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",load);\n';
    s += '    else load();\n';
    s += '})();';
    return s;
}

module.exports = genIndex;

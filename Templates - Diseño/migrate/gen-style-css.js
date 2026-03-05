// Generates style.css (base reset + CSS variables)
function genStyleCSS(site, vars, colors, bodyFont) {
    var varLines = Object.entries(vars).map(function(e) {
        return '    --' + e[0] + ': ' + e[1] + ';';
    }).join('\n');

    var lines = [];
    lines.push('/* ' + site.name + ' - Base (reset + variables) */');
    lines.push('/* Style: ' + site.style + ' */');
    lines.push('');
    lines.push(':root {');
    lines.push('    --' + site.slug + '-primary: ' + colors.primary + ';');
    lines.push('    --' + site.slug + '-secondary: ' + colors.secondary + ';');
    lines.push('    --' + site.slug + '-accent: ' + colors.accent + ';');
    lines.push('    --' + site.slug + '-dark: ' + colors.dark + ';');
    lines.push('    --' + site.slug + '-light: ' + colors.light + ';');
    lines.push('    --' + site.slug + '-text: ' + colors.text + ';');
    lines.push('    --' + site.slug + '-text-light: ' + colors.textLight + ';');
    lines.push('');
    lines.push(varLines);
    lines.push('');
    lines.push("    --font-primary: 'Playfair Display', serif;");
    lines.push('    --font-secondary: ' + bodyFont + ';');
    lines.push('');
    lines.push('    --space-xs: 0.25rem; --space-sm: 0.5rem; --space-md: 1rem;');
    lines.push('    --space-lg: 1.5rem;  --space-xl: 2rem;   --space-2xl: 3rem;');
    lines.push('');
    lines.push('    --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);');
    lines.push('    --shadow-md: 0 4px 6px rgba(0,0,0,0.1);');
    lines.push('    --shadow-lg: 0 10px 20px rgba(0,0,0,0.15);');
    lines.push('');
    lines.push('    --radius-sm: 4px; --radius-md: 8px; --radius-lg: 12px;');
    lines.push('');
    lines.push('    --primary-color: ' + colors.primary + ';');
    lines.push('    --secondary-color: ' + colors.secondary + ';');
    lines.push('    --accent-color: ' + colors.accent + ';');
    lines.push('    --background-color: ' + colors.light + ';');
    lines.push('    --card-bg: #FFFFFF;');
    lines.push('    --text-color: ' + colors.text + ';');
    lines.push('    --text-muted: ' + colors.textLight + ';');
    lines.push('    --border-color: rgba(0,0,0,0.1);');
    lines.push('}');
    lines.push('');
    lines.push('* { margin: 0; padding: 0; box-sizing: border-box; }');
    lines.push('html { scroll-behavior: smooth; }');
    lines.push('body { font-family: var(--font-secondary); background: ' + colors.light + '; color: ' + colors.text + '; line-height: 1.6; }');
    lines.push('img { max-width: 100%; height: auto; display: block; }');
    lines.push('a { color: inherit; text-decoration: none; transition: all 0.3s ease; }');
    lines.push('.container { max-width: 1400px; margin: 0 auto; padding: 0 var(--space-lg); }');
    lines.push('');
    lines.push('@media (max-width: 768px) {');
    lines.push('    .container { padding: 0 var(--space-md); }');
    lines.push('}');

    return lines.join('\n');
}

module.exports = genStyleCSS;

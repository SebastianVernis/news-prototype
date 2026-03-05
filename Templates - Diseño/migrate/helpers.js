const fs = require('fs');
const path = require('path');

function mkdirSafe(d) {
    if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });
}

function writeF(fp, c) {
    mkdirSafe(path.dirname(fp));
    fs.writeFileSync(fp, c, 'utf8');
}

function copyF(s, d) {
    mkdirSafe(path.dirname(d));
    if (fs.existsSync(s)) { fs.copyFileSync(s, d); return true; }
    return false;
}

function extractStyle(html) {
    var m = html.match(/<style[^>]*>([\s\S]*?)<\/style>/i);
    return m ? m[1].trim() : '';
}

function extractVars(css) {
    var vars = {};
    var rm = css.match(/:root\s*\{([^}]+)\}/);
    if (rm) {
        var re = /--([a-zA-Z0-9_-]+)\s*:\s*([^;]+);/g, m;
        while ((m = re.exec(rm[1])) !== null) vars[m[1]] = m[2].trim();
    }
    return vars;
}

function findColor(vars, kws) {
    for (var i = 0; i < kws.length; i++) {
        for (var k in vars) {
            if (k.toLowerCase().includes(kws[i]) && vars[k].startsWith('#')) return vars[k];
        }
    }
    return null;
}

function getColors(vars) {
    return {
        primary:   findColor(vars, ['accent-color','accent-red','accent-purple','accent','brand','primary']) || findColor(vars, ['blue','purple','red','green']) || '#1a73e8',
        secondary: findColor(vars, ['secondary','crimson','surface','bg-surface']) || '#333333',
        accent:    findColor(vars, ['accent','highlight','gold','yellow','rose']) || '#1a73e8',
        dark:      findColor(vars, ['dark','bg-base','text-dark']) || '#1A1A1A',
        light:     findColor(vars, ['bg-white','bg-color','bg-light']) || '#FFFFFF',
        text:      findColor(vars, ['text-color','text-dark','text-primary']) || '#1A1A1A',
        textLight: findColor(vars, ['text-muted','text-secondary','text-light']) || '#666666',
    };
}

function getBodyFont(css) {
    var m = css.match(/body\s*\{[^}]*font-family\s*:\s*([^;]+);/);
    return m ? m[1].trim() : "'Noto Sans', Arial, sans-serif";
}

module.exports = { mkdirSafe, writeF, copyF, extractStyle, extractVars, getColors, getBodyFont };

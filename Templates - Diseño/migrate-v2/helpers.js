var fs = require('fs');

function mkdirp(p) { fs.mkdirSync(p, { recursive: true }); }
function write(fp, c) { fs.writeFileSync(fp, c, 'utf8'); }
function copy(src, dst) {
    if (fs.existsSync(src)) fs.copyFileSync(src, dst);
    else console.log('    WARN: no existe ' + src);
}

function extractStyle(html) {
    var m = html.match(/<style[^>]*>([\s\S]*?)<\/style>/i);
    return m ? m[1].trim() : '';
}

function extractMain(html) {
    var bodyM = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
    if (!bodyM) return '';
    var body = bodyM[1];
    // Remove header and footer
    body = body.replace(/<header[\s\S]*?<\/header>/i, '');
    body = body.replace(/<footer[\s\S]*?<\/footer>/i, '');
    // Check if there's a <main> tag
    var mainM = body.match(/<main[\s\S]*?<\/main>/i);
    if (mainM) return mainM[0];
    // Otherwise wrap remaining content in <main>
    return '<main>\n' + body.trim() + '\n</main>';
}

function extractVars(css) {
    var vars = {};
    var rootM = css.match(/:root\s*\{([^}]+)\}/);
    if (!rootM) return vars;
    rootM[1].split('\n').forEach(function(line) {
        var m = line.match(/--([\w-]+)\s*:\s*([^;]+)/);
        if (m) vars[m[1].trim()] = m[2].trim();
    });
    return vars;
}

function findColor(vars, keywords) {
    for (var i = 0; i < keywords.length; i++) {
        var keys = Object.keys(vars);
        for (var j = 0; j < keys.length; j++) {
            if (keys[j].toLowerCase().indexOf(keywords[i]) !== -1) {
                var v = vars[keys[j]];
                if (v.match(/#[0-9a-fA-F]{3,8}/)) return v.split('/')[0].split('*')[0].trim();
            }
        }
    }
    return null;
}

function getColors(vars) {
    return {
        primary: findColor(vars, ['accent','brand','primary','glow','neon']) || '#1a73e8',
        bg: findColor(vars, ['bg','surface','paper','bone','sand','base','navy','dark']) || '#ffffff',
        text: findColor(vars, ['text-dark','text-ink','text-main','text-primary','text-color']) || '#111111',
    };
}

function isDarkTheme(bgColor) {
    if (!bgColor) return false;
    var hex = bgColor.replace('#', '');
    if (hex.length === 3) hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
    var r = parseInt(hex.substr(0,2),16);
    var g = parseInt(hex.substr(2,2),16);
    var b = parseInt(hex.substr(4,2),16);
    return (r + g + b) / 3 < 128;
}

module.exports = { mkdirp, write, copy, extractStyle, extractMain, extractVars, getColors, isDarkTheme };

import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const SITES_DIR = path.join(ROOT, "sites");
const OUT_DIR = path.join(ROOT, "dist_pages");

const SITE_NAMES = ["site_1", "site_2", "site_3"];

const SITE_BRAND = {
  site_1: { name: "VerdadMexicano Online", accent: "#B10B1F" },
  site_2: { name: "Crónica Perspectiva", accent: "#3D55EF" },
  site_3: { name: "InfoNacionalDigital", accent: "#111827" },
};

// 1x1 transparent PNG
const LOGO_PNG_BASE64 =
  "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO5W2iAAAAAASUVORK5CYII=";

function rmrf(p) {
  if (!fs.existsSync(p)) return;
  fs.rmSync(p, { recursive: true, force: true });
}

function mkdirp(p) {
  fs.mkdirSync(p, { recursive: true });
}

function copyDir(src, dest) {
  mkdirp(dest);
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const from = path.join(src, entry.name);
    const to = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(from, to);
    } else if (entry.isFile()) {
      fs.copyFileSync(from, to);
    }
  }
}

function writeFileIfMissing(filePath, contentOrBuffer) {
  if (fs.existsSync(filePath)) return;
  fs.writeFileSync(filePath, contentOrBuffer);
}

function ensureSiteAssets({ destDir, siteName, accent }) {
  const assetsDir = path.join(destDir, "assets");
  mkdirp(assetsDir);

  const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="320" height="64" viewBox="0 0 320 64" role="img" aria-label="${siteName}">
  <rect width="320" height="64" rx="12" fill="${accent}"/>
  <text x="18" y="41" fill="#ffffff" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Ubuntu,Arial,sans-serif" font-size="20" font-weight="800">${siteName}</text>
</svg>
`;

  writeFileIfMissing(path.join(assetsDir, "logo.svg"), svg);
  writeFileIfMissing(
    path.join(assetsDir, "logo.png"),
    Buffer.from(LOGO_PNG_BASE64, "base64")
  );
}

function buildLanding() {
  const html = `<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Portales de Política</title>
  <meta name="robots" content="noindex" />
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Ubuntu,"Helvetica Neue",Arial,sans-serif;background:#0b1220;color:#e6edf3;min-height:100vh}
    .wrap{max-width:1100px;margin:0 auto;padding:56px 20px}
    .title{font-size:40px;line-height:1.1;font-weight:900;letter-spacing:-0.02em}
    .subtitle{margin-top:12px;color:#9fb0c0;max-width:70ch;line-height:1.6}
    .grid{margin-top:28px;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
    a.card{display:block;text-decoration:none;color:inherit;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.06);border-radius:14px;overflow:hidden;transition:transform .2s ease, border-color .2s ease, background .2s ease}
    a.card:hover{transform:translateY(-2px);border-color:rgba(255,255,255,.22);background:rgba(255,255,255,.09)}
    .card-top{padding:18px}
    .tag{display:inline-block;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#0b1220;background:#a7f3d0;padding:6px 10px;border-radius:999px;font-weight:800}
    .card h2{margin-top:12px;font-size:20px;font-weight:850}
    .card p{margin-top:10px;color:#b6c5d3;line-height:1.6;font-size:14px}
    .card-bottom{padding:16px 18px;border-top:1px solid rgba(255,255,255,.12);display:flex;justify-content:space-between;align-items:center;color:#9fb0c0;font-size:13px}
    .pill{padding:6px 10px;border-radius:999px;border:1px solid rgba(255,255,255,.14)}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="title">Portales de Política</div>
    <div class="subtitle">Landing de despliegue para Cloudflare Pages. Elegí un sitio para navegar el contenido generado (HTML estático).
    </div>

    <div class="grid">
      <a class="card" href="/site_1/index.html">
        <div class="card-top">
          <div class="tag">Site 1</div>
          <h2>VerdadMexicano Online</h2>
          <p>Estilo editorial clásico con header completo y navegación por categorías.</p>
        </div>
        <div class="card-bottom"><span class="pill">/site_1</span><span>Entrar →</span></div>
      </a>
      <a class="card" href="/site_2/index.html">
        <div class="card-top">
          <div class="tag">Site 2</div>
          <h2>Crónica Perspectiva</h2>
          <p>Portal con sidebar fija y lectura rápida; foco en navegación vertical.</p>
        </div>
        <div class="card-bottom"><span class="pill">/site_2</span><span>Entrar →</span></div>
      </a>
      <a class="card" href="/site_3/index.html">
        <div class="card-top">
          <div class="tag">Site 3</div>
          <h2>InfoNacionalDigital</h2>
          <p>Minimal / elegante, con acentos oscuros y cards limpias.</p>
        </div>
        <div class="card-bottom"><span class="pill">/site_3</span><span>Entrar →</span></div>
      </a>
    </div>
  </div>
</body>
</html>`;

  fs.writeFileSync(path.join(OUT_DIR, "index.html"), html, "utf8");
}

function main() {
  rmrf(OUT_DIR);
  mkdirp(OUT_DIR);

  for (const site of SITE_NAMES) {
    const src = path.join(SITES_DIR, site);
    const dest = path.join(OUT_DIR, site);

    if (!fs.existsSync(src)) {
      throw new Error(`Missing site directory: ${src}`);
    }

    copyDir(src, dest);

    const brand = SITE_BRAND[site] ?? { name: site, accent: "#111827" };
    ensureSiteAssets({ destDir: dest, siteName: brand.name, accent: brand.accent });
  }

  buildLanding();

  console.log(`Built Pages output at: ${OUT_DIR}`);
}

main();

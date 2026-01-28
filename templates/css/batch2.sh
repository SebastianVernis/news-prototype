#!/bin/bash

# Generate templates 16-40 with unique color schemes and fonts
FONTS=(
  "Rubik:wght@300;500;700" "Quicksand:wght@400;600;700" "Lora:wght@400;700" 
  "Work+Sans:wght@400;600;800" "Crimson+Text:wght@400;700" "Archivo:wght@400;700;900"
  "Bitter:wght@400;700" "Barlow:wght@400;600;800" "Josefin+Sans:wght@400;700"
  "Signika:wght@400;700" "Karla:wght@400;700" "Spectral:wght@400;700"
  "Heebo:wght@400;700;900" "Catamaran:wght@400;700" "Libre+Baskerville:wght@400;700"
  "Exo+2:wght@400;700;900" "Titillium+Web:wght@400;700" "Cabin:wght@400;700"
  "Alegreya:wght@400;700" "Public+Sans:wght@400;700" "DM+Sans:wght@400;700"
  "Space+Grotesk:wght@400;700" "Manrope:wght@400;700" "IBM+Plex+Sans:wght@400;700"
  "Mukta:wght@400;700"
)

PRIMARY_COLORS=(
  "#C62828" "#AD1457" "#6A1B9A" "#4527A0" "#283593" "#1565C0" "#0277BD" "#00838F"
  "#00695C" "#2E7D32" "#558B2F" "#9E9D24" "#F9A825" "#FF8F00" "#EF6C00" "#D84315"
  "#5D4037" "#455A64" "#37474F" "#263238" "#880E4F" "#4A148C" "#311B92" "#1A237E"
  "#004D40"
)

SECONDARY_COLORS=(
  "#EF5350" "#EC407A" "#AB47BC" "#7E57C2" "#5C6BC0" "#42A5F5" "#29B6F6" "#26C6DA"
  "#26A69A" "#66BB6A" "#9CCC65" "#D4E157" "#FFEB3B" "#FFA726" "#FF7043" "#FF5722"
  "#8D6E63" "#78909C" "#607D8B" "#546E7A" "#E91E63" "#9C27B0" "#673AB7" "#3F51B5"
  "#00897B"
)

ACCENT_COLORS=(
  "#FFCDD2" "#F8BBD0" "#E1BEE7" "#D1C4E9" "#C5CAE9" "#BBDEFB" "#B3E5FC" "#B2EBF2"
  "#B2DFDB" "#C8E6C9" "#DCEDC8" "#F0F4C3" "#FFF9C4" "#FFE0B2" "#FFCCBC" "#FFAB91"
  "#D7CCC8" "#CFD8DC" "#B0BEC5" "#90A4AE" "#FCE4EC" "#F3E5F5" "#EDE7F6" "#E8EAF6"
  "#A7FFEB"
)

BACKGROUNDS=(
  "#FAFAFA" "#FCE4EC" "#F3E5F5" "#EDE7F6" "#E8EAF6" "#E3F2FD" "#E1F5FE" "#E0F7FA"
  "#E0F2F1" "#F1F8E9" "#F9FBE7" "#FFFDE7" "#FFF8E1" "#FFF3E0" "#FBE9E7" "#EFEBE9"
  "#FAFAFA" "#ECEFF1" "#F5F5F5" "#E0E0E0" "#FCE4EC" "#F3E5F5" "#EDE7F6" "#E8EAF6"
  "#E0F2F1"
)

for i in {16..40}; do
  idx=$((i-16))
  FONT=${FONTS[$idx]}
  PRIMARY=${PRIMARY_COLORS[$idx]}
  SECONDARY=${SECONDARY_COLORS[$idx]}
  ACCENT=${ACCENT_COLORS[$idx]}
  BG=${BACKGROUNDS[$idx]}
  
  # Vary border radius
  RADIUS=$((4 + (idx % 3) * 4))
  
  # Vary layout spacing
  SPACING=$((20 + (idx % 5) * 5))
  
cat > template${i}.css << TEMPLATE
@import url('https://fonts.googleapis.com/css2?family=${FONT}&family=Roboto:wght@400;500;700&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
    --primary-color: ${PRIMARY};
    --secondary-color: ${SECONDARY};
    --accent-color: ${ACCENT};
    --background-color: ${BG};
    --text-color: #212121;
    --light-text: #757575;
    --card-bg: #FFFFFF;
}
body { font-family: 'Roboto', sans-serif; background-color: var(--background-color); color: var(--text-color); line-height: 1.65; }
.container { max-width: $((1200 + (idx % 4) * 100))px; margin: 0 auto; padding: 0 ${SPACING}px; }
.header { background-color: var(--primary-color); color: white; padding: $((18 + idx % 6))px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.header .container { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: ${SPACING}px; }
.logo h1 { font-size: $((22 + idx % 8))px; font-weight: $((idx % 2 == 0 ? 700 : 900)); }
.tagline { font-size: 0.85em; font-weight: 600; opacity: 0.9; }
.nav { display: flex; gap: $((18 + idx % 4))px; }
.nav-link { color: white; text-decoration: none; font-weight: $((idx % 2 == 0 ? 600 : 500)); transition: all 0.3s; }
.nav-link:hover { color: var(--accent-color); transform: translateY(-2px); }
.header-actions { display: flex; gap: 12px; }
.search-input { padding: 10px 18px; border: $((1 + idx % 2))px solid var(--accent-color); border-radius: ${RADIUS}px; width: $((190 + idx % 4 * 15))px; background-color: rgba(255,255,255,0.15); color: white; }
.search-input::placeholder { color: rgba(255,255,255,0.7); }
.btn-subscribe { background-color: var(--secondary-color); color: white; border: none; padding: 10px 22px; border-radius: ${RADIUS}px; font-weight: $((idx % 2 == 0 ? 700 : 600)); cursor: pointer; transition: all 0.3s; }
.btn-subscribe:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
.hero-section { margin: $((35 + idx % 6 * 3))px 0; }
.featured-article { background-color: var(--card-bg); border-radius: ${RADIUS}px; overflow: hidden; box-shadow: 0 $((4 + idx % 4))px $((15 + idx % 8))px rgba(0,0,0,0.1); display: grid; grid-template-columns: $((idx % 3 == 0 ? "1.7fr 1fr" : idx % 3 == 1 ? "1.5fr 1fr" : "1.6fr 1fr")); }
.article-image img { width: 100%; height: 100%; object-fit: cover; }
.article-content { padding: $((35 + idx % 6 * 3))px; }
.category { background-color: var(--secondary-color); color: white; padding: $((5 + idx % 2))px $((15 + idx % 3))px; border-radius: $((idx % 3 == 0 ? RADIUS + 5 : RADIUS))px; font-size: 0.8em; font-weight: $((idx % 2 == 0 ? 700 : 600)); display: inline-block; margin-bottom: 15px; text-transform: $((idx % 2 == 0 ? "uppercase" : "none")); }
.article-title { font-size: $((18 + idx % 6))px; font-weight: $((idx % 2 == 0 ? 800 : 700)); margin-bottom: $((14 + idx % 4))px; line-height: 1.3; }
.article-excerpt { color: var(--light-text); margin-bottom: ${SPACING}px; font-size: 1.05em; }
.article-meta { display: flex; gap: $((15 + idx % 5))px; font-size: 0.87em; color: var(--light-text); }
.news-grid { display: grid; grid-template-columns: $((idx % 3 == 0 ? "2.2fr 1fr" : idx % 3 == 1 ? "2fr 1fr" : "2.1fr 1fr")); gap: $((28 + idx % 8))px; margin: $((35 + idx % 6 * 3))px 0; }
.section-title { font-size: $((20 + idx % 8))px; margin-bottom: $((28 + idx % 5))px; font-weight: $((idx % 2 == 0 ? 800 : 700)); color: var(--primary-color); }
.news-card { background-color: var(--card-bg); border-radius: ${RADIUS}px; overflow: hidden; margin-bottom: $((22 + idx % 6))px; box-shadow: 0 3px $((12 + idx % 6))px rgba(0,0,0,0.08); transition: all 0.3s; }
.news-card:hover { transform: translateY($((idx % 2 == 0 ? "-6px" : "-8px"))); box-shadow: 0 $((6 + idx % 4))px $((20 + idx % 8))px rgba(0,0,0,0.12); }
.card-image { width: 100%; height: $((210 + idx % 8 * 5))px; object-fit: cover; }
.card-content { padding: $((22 + idx % 6))px; }
.card-title { font-size: $((13 + idx % 5))px; margin: $((10 + idx % 3))px 0 $((14 + idx % 4))px 0; font-weight: $((idx % 2 == 0 ? 700 : 600)); }
.card-excerpt { color: var(--light-text); margin-bottom: $((14 + idx % 4))px; line-height: 1.6; }
.sidebar-section { background-color: var(--card-bg); padding: $((22 + idx % 6))px; border-radius: ${RADIUS}px; margin-bottom: $((22 + idx % 6))px; box-shadow: 0 3px $((12 + idx % 6))px rgba(0,0,0,0.08); }
.sidebar-title { font-size: $((13 + idx % 4))px; margin-bottom: ${SPACING}px; font-weight: $((idx % 2 == 0 ? 700 : 600)); color: var(--primary-color); }
.trending-list { list-style: none; }
.trending-item { display: flex; gap: $((14 + idx % 3))px; padding: $((14 + idx % 3))px 0; border-bottom: $((1 + idx % 2))px solid var(--background-color); }
.trending-number { background-color: var(--secondary-color); color: white; width: $((28 + idx % 4))px; height: $((28 + idx % 4))px; display: flex; align-items: center; justify-content: center; border-radius: $((idx % 2 == 0 ? "50%" : RADIUS + "px")); font-weight: 700; }
.trending-content h4 { font-size: 0.95em; margin-bottom: $((5 + idx % 2))px; font-weight: 600; }
.trending-meta { font-size: 0.8em; color: var(--light-text); }
.sidebar-article { margin-bottom: ${SPACING}px; }
.sidebar-article img { width: 100%; border-radius: $((RADIUS - 2))px; margin-bottom: $((10 + idx % 3))px; }
.sidebar-article h4 { font-size: 1.02em; margin-bottom: $((6 + idx % 2))px; font-weight: 600; }
.sidebar-meta { font-size: 0.87em; color: var(--light-text); }
.newsletter { background-color: var(--primary-color); color: white; }
.newsletter .sidebar-title { color: white; }
.newsletter p { margin-bottom: $((14 + idx % 4))px; }
.newsletter-form { display: flex; flex-direction: column; gap: $((10 + idx % 2))px; }
.newsletter-input { padding: $((12 + idx % 2))px; border: none; border-radius: $((RADIUS - 2))px; }
.newsletter-btn { background-color: var(--secondary-color); color: white; border: none; padding: $((12 + idx % 2))px; border-radius: $((RADIUS - 2))px; font-weight: 700; cursor: pointer; transition: all 0.3s; }
.newsletter-btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
.categories-section { margin: $((55 + idx % 10 * 2))px 0; }
.categories-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: ${SPACING}px; }
.category-card { position: relative; border-radius: ${RADIUS}px; overflow: hidden; height: $((230 + idx % 8 * 5))px; cursor: pointer; }
.category-card img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s; }
.category-card:hover img { transform: scale($((idx % 2 == 0 ? "1.1" : "1.15"))); }
.category-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,$((idx % 2 == 0 ? "0.85" : "0.9")))); padding: $((28 + idx % 6))px ${SPACING}px ${SPACING}px; color: white; }
.category-overlay h3 { font-size: $((12 + idx % 4))px; margin-bottom: $((5 + idx % 2))px; font-weight: 700; }
.footer { background-color: var(--primary-color); color: white; padding: $((50 + idx % 8 * 2))px 0 ${SPACING}px; margin-top: $((55 + idx % 10 * 2))px; }
.footer-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: $((35 + idx % 8))px; margin-bottom: $((35 + idx % 8))px; }
.footer-column h4 { font-size: $((12 + idx % 3))px; margin-bottom: ${SPACING}px; font-weight: 700; }
.footer-column p { color: rgba(255,255,255,0.85); margin-bottom: $((10 + idx % 2))px; }
.social-links { display: flex; gap: $((14 + idx % 4))px; margin-top: $((14 + idx % 4))px; }
.social-link { color: white; text-decoration: none; font-weight: 600; transition: all 0.3s; }
.social-link:hover { color: var(--accent-color); transform: translateY(-2px); }
.footer-links { list-style: none; }
.footer-links li { margin-bottom: $((10 + idx % 2))px; }
.footer-links a { color: rgba(255,255,255,0.85); text-decoration: none; transition: color 0.3s; }
.footer-links a:hover { color: white; }
.footer-bottom { text-align: center; padding-top: $((28 + idx % 6))px; border-top: $((1 + idx % 2))px solid rgba(255,255,255,0.2); color: rgba(255,255,255,0.75); }
@media (max-width: 1200px) { .news-grid { grid-template-columns: 1fr; } .categories-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .featured-article { grid-template-columns: 1fr; } .footer-grid { grid-template-columns: 1fr; } }
TEMPLATE

done


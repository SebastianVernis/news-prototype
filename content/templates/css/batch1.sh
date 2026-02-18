#!/bin/bash

# Templates 6-15 with varied designs
for i in {6..15}; do

if [ $i -eq 6 ]; then
# Cyan Modern
cat > template${i}.css << 'TEMPLATE'
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700;900&family=Source+Sans+Pro:wght@300;400;600&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
:root { --primary-color: #006BA6; --secondary-color: #0496FF; --accent-color: #00D9FF; --background-color: #E8F4F8; --text-color: #003554; --light-text: #4A90A4; --card-bg: #FFFFFF; }
body { font-family: 'Source Sans Pro', sans-serif; background-color: var(--background-color); color: var(--text-color); line-height: 1.65; }
.container { max-width: 1280px; margin: 0 auto; padding: 0 20px; }
.header { background-color: white; padding: 22px 0; box-shadow: 0 3px 12px rgba(0,107,166,0.1); }
.header .container { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 22px; }
.logo h1 { font-family: 'Montserrat', sans-serif; font-size: 2.4em; color: var(--primary-color); font-weight: 900; }
.tagline { font-size: 0.88em; color: var(--secondary-color); font-weight: 600; }
.nav { display: flex; gap: 22px; }
.nav-link { color: var(--text-color); text-decoration: none; font-weight: 600; transition: color 0.3s; }
.nav-link:hover { color: var(--accent-color); }
.header-actions { display: flex; gap: 12px; }
.search-input { padding: 11px 18px; border: 2px solid var(--secondary-color); border-radius: 8px; width: 230px; }
.btn-subscribe { background-color: var(--secondary-color); color: white; border: none; padding: 11px 24px; border-radius: 8px; font-weight: 700; cursor: pointer; }
.hero-section { margin: 42px 0; }
.featured-article { background-color: var(--card-bg); border-radius: 12px; overflow: hidden; box-shadow: 0 8px 30px rgba(0,107,166,0.15); display: grid; grid-template-columns: 1.6fr 1fr; }
.article-image img { width: 100%; height: 100%; object-fit: cover; }
.article-content { padding: 42px; }
.category { background-color: var(--accent-color); color: var(--primary-color); padding: 6px 18px; border-radius: 18px; font-size: 0.82em; font-weight: 700; display: inline-block; margin-bottom: 16px; }
.article-title { font-family: 'Montserrat', sans-serif; font-size: 2.1em; font-weight: 800; margin-bottom: 16px; color: var(--primary-color); }
.article-excerpt { color: var(--light-text); margin-bottom: 22px; font-size: 1.02em; }
.article-meta { display: flex; gap: 18px; font-size: 0.88em; color: var(--light-text); }
.news-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 35px; margin: 42px 0; }
.section-title { font-family: 'Montserrat', sans-serif; font-size: 2.2em; margin-bottom: 32px; color: var(--primary-color); font-weight: 800; }
.news-card { background-color: var(--card-bg); border-radius: 10px; overflow: hidden; margin-bottom: 28px; box-shadow: 0 4px 18px rgba(0,107,166,0.1); transition: transform 0.3s; }
.news-card:hover { transform: translateY(-6px); }
.card-image { width: 100%; height: 230px; object-fit: cover; }
.card-content { padding: 26px; }
.card-title { font-family: 'Montserrat', sans-serif; font-size: 1.45em; margin: 12px 0 16px 0; font-weight: 700; color: var(--primary-color); }
.card-excerpt { color: var(--light-text); margin-bottom: 16px; }
.sidebar-section { background-color: var(--card-bg); padding: 26px; border-radius: 10px; margin-bottom: 26px; box-shadow: 0 4px 18px rgba(0,107,166,0.1); }
.sidebar-title { font-family: 'Montserrat', sans-serif; font-size: 1.35em; margin-bottom: 22px; color: var(--primary-color); font-weight: 700; }
.trending-list { list-style: none; }
.trending-item { display: flex; gap: 16px; padding: 16px 0; border-bottom: 1px solid var(--background-color); }
.trending-number { background-color: var(--secondary-color); color: white; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-weight: 700; }
.trending-content h4 { font-size: 0.96em; margin-bottom: 6px; }
.trending-meta { font-size: 0.82em; color: var(--light-text); }
.sidebar-article { margin-bottom: 22px; }
.sidebar-article img { width: 100%; border-radius: 6px; margin-bottom: 12px; }
.sidebar-article h4 { font-size: 1.02em; margin-bottom: 6px; }
.sidebar-meta { font-size: 0.88em; color: var(--light-text); }
.newsletter { background-color: var(--primary-color); color: white; }
.newsletter .sidebar-title { color: white; }
.newsletter p { margin-bottom: 16px; }
.newsletter-form { display: flex; flex-direction: column; gap: 11px; }
.newsletter-input { padding: 13px; border: none; border-radius: 6px; }
.newsletter-btn { background-color: var(--accent-color); color: var(--primary-color); border: none; padding: 13px; border-radius: 6px; font-weight: 700; cursor: pointer; }
.categories-section { margin: 62px 0; }
.categories-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 22px; }
.category-card { position: relative; border-radius: 10px; overflow: hidden; height: 245px; cursor: pointer; }
.category-card img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s; }
.category-card:hover img { transform: scale(1.12); }
.category-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,107,166,0.9)); padding: 32px 22px 22px; color: white; }
.category-overlay h3 { font-size: 1.25em; margin-bottom: 6px; }
.footer { background-color: var(--primary-color); color: white; padding: 55px 0 22px; margin-top: 62px; }
.footer-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 42px; margin-bottom: 42px; }
.footer-column h4 { font-size: 1.25em; margin-bottom: 22px; }
.footer-column p { color: rgba(255,255,255,0.85); margin-bottom: 11px; }
.social-links { display: flex; gap: 16px; margin-top: 16px; }
.social-link { color: white; text-decoration: none; transition: color 0.3s; }
.social-link:hover { color: var(--accent-color); }
.footer-links { list-style: none; }
.footer-links li { margin-bottom: 11px; }
.footer-links a { color: rgba(255,255,255,0.85); text-decoration: none; transition: color 0.3s; }
.footer-links a:hover { color: white; }
.footer-bottom { text-align: center; padding-top: 32px; border-top: 1px solid rgba(255,255,255,0.25); color: rgba(255,255,255,0.75); }
@media (max-width: 1200px) { .news-grid { grid-template-columns: 1fr; } .categories-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .featured-article { grid-template-columns: 1fr; } .footer-grid { grid-template-columns: 1fr; } }
TEMPLATE
fi

if [ $i -eq 7 ]; then
# Red Bold
cat > template${i}.css << 'TEMPLATE'
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=PT+Sans:wght@400;700&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
:root { --primary-color: #B71C1C; --secondary-color: #E53935; --accent-color: #FFCDD2; --background-color: #FAFAFA; --text-color: #212121; --light-text: #757575; --card-bg: #FFFFFF; }
body { font-family: 'PT Sans', sans-serif; background-color: var(--background-color); color: var(--text-color); line-height: 1.7; }
.container { max-width: 1320px; margin: 0 auto; padding: 0 20px; }
.header { background-color: var(--primary-color); color: white; padding: 18px 0; border-bottom: 4px solid var(--secondary-color); }
.header .container { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px; }
.logo h1 { font-family: 'Oswald', sans-serif; font-size: 3.2em; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; }
.tagline { font-size: 0.9em; font-weight: 700; text-transform: uppercase; letter-spacing: 3px; }
.nav { display: flex; gap: 28px; }
.nav-link { color: white; text-decoration: none; font-weight: 700; text-transform: uppercase; font-size: 0.92em; transition: color 0.3s; }
.nav-link:hover { color: var(--accent-color); }
.header-actions { display: flex; gap: 14px; }
.search-input { padding: 12px 20px; border: 2px solid white; border-radius: 4px; width: 240px; background-color: rgba(255,255,255,0.1); color: white; }
.search-input::placeholder { color: rgba(255,255,255,0.7); }
.btn-subscribe { background-color: white; color: var(--primary-color); border: none; padding: 12px 26px; border-radius: 4px; font-weight: 700; cursor: pointer; text-transform: uppercase; }
.hero-section { margin: 40px 0; }
.featured-article { background-color: var(--card-bg); border-radius: 0; overflow: hidden; box-shadow: 0 6px 24px rgba(0,0,0,0.15); display: grid; grid-template-columns: 1.5fr 1fr; border-top: 5px solid var(--primary-color); }
.article-image img { width: 100%; height: 100%; object-fit: cover; }
.article-content { padding: 45px; }
.category { background-color: var(--secondary-color); color: white; padding: 7px 20px; border-radius: 0; font-size: 0.85em; font-weight: 700; display: inline-block; margin-bottom: 18px; text-transform: uppercase; letter-spacing: 1px; }
.article-title { font-family: 'Oswald', sans-serif; font-size: 2.6em; font-weight: 700; margin-bottom: 18px; text-transform: uppercase; }
.article-excerpt { color: var(--light-text); margin-bottom: 24px; font-size: 1.08em; }
.article-meta { display: flex; gap: 22px; font-size: 0.9em; color: var(--light-text); font-weight: 700; }
.news-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 38px; margin: 40px 0; }
.section-title { font-family: 'Oswald', sans-serif; font-size: 2.8em; margin-bottom: 34px; text-transform: uppercase; color: var(--primary-color); }
.news-card { background-color: var(--card-bg); border-radius: 0; overflow: hidden; margin-bottom: 32px; box-shadow: 0 4px 16px rgba(0,0,0,0.12); transition: all 0.3s; border-left: 5px solid var(--secondary-color); }
.news-card:hover { transform: translateX(5px); box-shadow: 0 6px 24px rgba(0,0,0,0.18); }
.card-image { width: 100%; height: 235px; object-fit: cover; }
.card-content { padding: 28px; }
.card-title { font-family: 'Oswald', sans-serif; font-size: 1.7em; margin: 12px 0 18px 0; font-weight: 700; text-transform: uppercase; }
.card-excerpt { color: var(--light-text); margin-bottom: 18px; }
.sidebar-section { background-color: var(--card-bg); padding: 28px; border-radius: 0; margin-bottom: 28px; box-shadow: 0 4px 16px rgba(0,0,0,0.12); }
.sidebar-title { font-family: 'Oswald', sans-serif; font-size: 1.6em; margin-bottom: 24px; text-transform: uppercase; color: var(--primary-color); }
.trending-list { list-style: none; }
.trending-item { display: flex; gap: 16px; padding: 18px 0; border-bottom: 2px solid var(--background-color); }
.trending-number { background-color: var(--secondary-color); color: white; width: 34px; height: 34px; display: flex; align-items: center; justify-content: center; border-radius: 0; font-weight: 700; font-family: 'Oswald', sans-serif; }
.trending-content h4 { font-size: 1em; margin-bottom: 7px; font-weight: 700; }
.trending-meta { font-size: 0.85em; color: var(--light-text); }
.sidebar-article { margin-bottom: 24px; }
.sidebar-article img { width: 100%; border-radius: 0; margin-bottom: 12px; }
.sidebar-article h4 { font-size: 1.08em; margin-bottom: 7px; font-weight: 700; }
.sidebar-meta { font-size: 0.9em; color: var(--light-text); }
.newsletter { background-color: var(--primary-color); color: white; }
.newsletter .sidebar-title { color: white; }
.newsletter p { margin-bottom: 18px; }
.newsletter-form { display: flex; flex-direction: column; gap: 12px; }
.newsletter-input { padding: 14px; border: 2px solid white; border-radius: 0; background-color: rgba(255,255,255,0.1); color: white; }
.newsletter-input::placeholder { color: rgba(255,255,255,0.7); }
.newsletter-btn { background-color: white; color: var(--primary-color); border: none; padding: 14px; border-radius: 0; font-weight: 700; cursor: pointer; text-transform: uppercase; }
.categories-section { margin: 68px 0; }
.categories-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
.category-card { position: relative; border-radius: 0; overflow: hidden; height: 255px; cursor: pointer; border: 3px solid var(--secondary-color); }
.category-card img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s; }
.category-card:hover img { transform: scale(1.1); }
.category-overlay { position: absolute; bottom: 0; left: 0; right: 0; background-color: rgba(183,28,28,0.95); padding: 24px; color: white; }
.category-overlay h3 { font-family: 'Oswald', sans-serif; font-size: 1.5em; margin-bottom: 7px; text-transform: uppercase; }
.footer { background-color: var(--primary-color); color: white; padding: 60px 0 24px; margin-top: 68px; }
.footer-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 44px; margin-bottom: 44px; }
.footer-column h4 { font-family: 'Oswald', sans-serif; font-size: 1.6em; margin-bottom: 24px; text-transform: uppercase; }
.footer-column p { color: rgba(255,255,255,0.9); margin-bottom: 12px; }
.social-links { display: flex; gap: 18px; margin-top: 18px; }
.social-link { color: white; text-decoration: none; font-weight: 700; transition: color 0.3s; text-transform: uppercase; }
.social-link:hover { color: var(--accent-color); }
.footer-links { list-style: none; }
.footer-links li { margin-bottom: 12px; }
.footer-links a { color: rgba(255,255,255,0.9); text-decoration: none; transition: color 0.3s; }
.footer-links a:hover { color: white; }
.footer-bottom { text-align: center; padding-top: 34px; border-top: 2px solid rgba(255,255,255,0.2); }
@media (max-width: 1200px) { .news-grid { grid-template-columns: 1fr; } .categories-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .featured-article { grid-template-columns: 1fr; } .footer-grid { grid-template-columns: 1fr; } }
TEMPLATE
fi

# Continue for templates 8-15...
if [ $i -ge 8 ] && [ $i -le 15 ]; then
# Generate variations
PRIMARY_COLORS=("#283593" "#1565C0" "#00695C" "#4A148C" "#BF360C" "#424242" "#006064" "#1B5E20")
SECONDARY_COLORS=("#5C6BC0" "#42A5F5" "#26A69A" "#AB47BC" "#FF5722" "#757575" "#0097A7" "#66BB6A")
ACCENT_COLORS=("#C5CAE9" "#90CAF9" "#80CBC4" "#E1BEE7" "#FFAB91" "#BDBDBD" "#B2EBF2" "#C8E6C9")
BACKGROUNDS=("#F5F5F5" "#FAFAFA" "#ECEFF1" "#F3E5F5" "#FBE9E7" "#FAFAFA" "#E0F2F1" "#F1F8E9")

idx=$((i-8))
cat > template${i}.css << TEMPLATE
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;600;800&family=Open+Sans:wght@400;600&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
:root { --primary-color: ${PRIMARY_COLORS[$idx]}; --secondary-color: ${SECONDARY_COLORS[$idx]}; --accent-color: ${ACCENT_COLORS[$idx]}; --background-color: ${BACKGROUNDS[$idx]}; --text-color: #212121; --light-text: #757575; --card-bg: #FFFFFF; }
body { font-family: 'Open Sans', sans-serif; background-color: var(--background-color); color: var(--text-color); line-height: 1.6; }
.container { max-width: 1300px; margin: 0 auto; padding: 0 20px; }
.header { background-color: var(--primary-color); color: white; padding: 20px 0; }
.header .container { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px; }
.logo h1 { font-family: 'Nunito', sans-serif; font-size: 2.5em; font-weight: 800; }
.tagline { font-size: 0.85em; font-weight: 600; }
.nav { display: flex; gap: 20px; }
.nav-link { color: white; text-decoration: none; font-weight: 600; transition: color 0.3s; }
.nav-link:hover { color: var(--accent-color); }
.header-actions { display: flex; gap: 10px; }
.search-input { padding: 10px 15px; border: 1px solid var(--accent-color); border-radius: 20px; width: 200px; background-color: rgba(255,255,255,0.2); color: white; }
.search-input::placeholder { color: rgba(255,255,255,0.7); }
.btn-subscribe { background-color: var(--secondary-color); color: white; border: none; padding: 10px 20px; border-radius: 20px; font-weight: 600; cursor: pointer; }
.hero-section { margin: 40px 0; }
.featured-article { background-color: var(--card-bg); border-radius: 10px; overflow: hidden; box-shadow: 0 5px 20px rgba(0,0,0,0.1); display: grid; grid-template-columns: 1.5fr 1fr; }
.article-image img { width: 100%; height: 100%; object-fit: cover; }
.article-content { padding: 40px; }
.category { background-color: var(--secondary-color); color: white; padding: 5px 15px; border-radius: 15px; font-size: 0.8em; font-weight: 600; display: inline-block; margin-bottom: 15px; }
.article-title { font-family: 'Nunito', sans-serif; font-size: 2em; font-weight: 800; margin-bottom: 15px; }
.article-excerpt { color: var(--light-text); margin-bottom: 20px; }
.article-meta { display: flex; gap: 15px; font-size: 0.85em; color: var(--light-text); }
.news-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 30px; margin: 40px 0; }
.section-title { font-family: 'Nunito', sans-serif; font-size: 2em; margin-bottom: 30px; font-weight: 800; color: var(--primary-color); }
.news-card { background-color: var(--card-bg); border-radius: 8px; overflow: hidden; margin-bottom: 25px; box-shadow: 0 3px 15px rgba(0,0,0,0.08); transition: transform 0.3s; }
.news-card:hover { transform: translateY(-5px); }
.card-image { width: 100%; height: 220px; object-fit: cover; }
.card-content { padding: 25px; }
.card-title { font-family: 'Nunito', sans-serif; font-size: 1.4em; margin: 10px 0 15px 0; font-weight: 700; }
.card-excerpt { color: var(--light-text); margin-bottom: 15px; }
.sidebar-section { background-color: var(--card-bg); padding: 25px; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 3px 15px rgba(0,0,0,0.08); }
.sidebar-title { font-family: 'Nunito', sans-serif; font-size: 1.3em; margin-bottom: 20px; font-weight: 700; color: var(--primary-color); }
.trending-list { list-style: none; }
.trending-item { display: flex; gap: 15px; padding: 15px 0; border-bottom: 1px solid var(--background-color); }
.trending-number { background-color: var(--secondary-color); color: white; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-weight: 700; }
.trending-content h4 { font-size: 0.95em; margin-bottom: 5px; }
.trending-meta { font-size: 0.8em; color: var(--light-text); }
.sidebar-article { margin-bottom: 20px; }
.sidebar-article img { width: 100%; border-radius: 5px; margin-bottom: 10px; }
.sidebar-article h4 { font-size: 1em; margin-bottom: 5px; }
.sidebar-meta { font-size: 0.85em; color: var(--light-text); }
.newsletter { background-color: var(--primary-color); color: white; }
.newsletter .sidebar-title { color: white; }
.newsletter p { margin-bottom: 15px; }
.newsletter-form { display: flex; flex-direction: column; gap: 10px; }
.newsletter-input { padding: 12px; border: none; border-radius: 5px; }
.newsletter-btn { background-color: var(--secondary-color); color: white; border: none; padding: 12px; border-radius: 5px; font-weight: 600; cursor: pointer; }
.categories-section { margin: 60px 0; }
.categories-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.category-card { position: relative; border-radius: 8px; overflow: hidden; height: 240px; cursor: pointer; }
.category-card img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s; }
.category-card:hover img { transform: scale(1.1); }
.category-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.8)); padding: 30px 20px 20px; color: white; }
.category-overlay h3 { font-size: 1.2em; margin-bottom: 5px; }
.footer { background-color: var(--primary-color); color: white; padding: 50px 0 20px; margin-top: 60px; }
.footer-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 40px; margin-bottom: 40px; }
.footer-column h4 { font-size: 1.2em; margin-bottom: 20px; }
.footer-column p { color: rgba(255,255,255,0.8); margin-bottom: 10px; }
.social-links { display: flex; gap: 15px; margin-top: 15px; }
.social-link { color: white; text-decoration: none; transition: color 0.3s; }
.social-link:hover { color: var(--accent-color); }
.footer-links { list-style: none; }
.footer-links li { margin-bottom: 10px; }
.footer-links a { color: rgba(255,255,255,0.8); text-decoration: none; transition: color 0.3s; }
.footer-links a:hover { color: white; }
.footer-bottom { text-align: center; padding-top: 30px; border-top: 1px solid rgba(255,255,255,0.2); color: rgba(255,255,255,0.7); }
@media (max-width: 1200px) { .news-grid { grid-template-columns: 1fr; } .categories-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .featured-article { grid-template-columns: 1fr; } .footer-grid { grid-template-columns: 1fr; } }
TEMPLATE
fi

done


#!/bin/bash

# Template output directory
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUTPUT_DIR="${NEWS_TEMPLATES_DIR:-$ROOT_DIR/public/templates/css}"
mkdir -p "$OUTPUT_DIR"

# Template 6 - Elegant Purple
cat > "$OUTPUT_DIR/template6.css" << 'TEMPLATE'
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Montserrat:wght@300;400;600&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
    --primary-color: #6A0DAD;
    --secondary-color: #9D4EDD;
    --accent-color: #E0AAFF;
    --background-color: #F8F9FA;
    --text-color: #3C096C;
    --light-text: #8C43A0;
    --card-bg: #FFFFFF;
}
body { font-family: 'Montserrat', sans-serif; background-color: var(--background-color); color: var(--text-color); line-height: 1.7; }
.container { max-width: 1250px; margin: 0 auto; padding: 0 25px; }
.header { background-color: var(--primary-color); color: white; padding: 22px 0; }
.header .container { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px; }
.logo h1 { font-family: 'Playfair Display', serif; font-size: 2.5em; font-weight: 700; }
.tagline { font-size: 0.9em; opacity: 0.9; }
.nav { display: flex; gap: 22px; }
.nav-link { color: white; text-decoration: none; font-weight: 500; transition: all 0.3s; position: relative; }
.nav-link::after { content: ''; position: absolute; bottom: -5px; left: 0; width: 0; height: 2px; background-color: var(--accent-color); transition: width 0.3s; }
.nav-link:hover::after { width: 100%; }
.nav-link:hover { color: var(--accent-color); }
.header-actions { display: flex; gap: 12px; }
.search-input { padding: 10px 18px; border: 1px solid var(--accent-color); border-radius: 20px; width: 180px; }
.btn-subscribe { background-color: var(--secondary-color); color: white; border: none; padding: 10px 22px; border-radius: 20px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
.btn-subscribe:hover { background-color: var(--accent-color); transform: translateY(-2px); }
.hero-section { margin: 40px 0; }
.featured-article { background-color: var(--card-bg); border-radius: 12px; overflow: hidden; box-shadow: 0 8px 30px rgba(106,13,173,0.15); display: grid; grid-template-columns: 1.6fr 1fr; border-top: 4px solid var(--primary-color); }
.article-image img { width: 100%; height: 100%; object-fit: cover; }
.article-content { padding: 35px; }
.Category { background-color: var(--primary-color); color: white; padding: 6px 18px; border-radius: 20px; font-size: 0.8em; font-weight: 600; display: inline-block; margin-bottom: 15px; }
.article-title { font-family: 'Playfair Display', serif; font-size: 2.2em; margin-bottom: 15px; color: var(--primary-color); }
.article-excerpt { color: var(--light-text); margin-bottom: 20px; }
.article-meta { display: flex; gap: 18px; font-size: 0.9em; color: var(--light-text); }
.news-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 35px; margin: 40px 0; }
.section-title { font-family: 'Playfair Display', serif; font-size: 2.3em; margin-bottom: 30px; color: var(--primary-color); position: relative; padding-bottom: 10px; }
.section-title::after { content: ''; position: absolute; bottom: 0; left: 0; width: 60px; height: 3px; background-color: var(--secondary-color); }
.news-card { background-color: var(--card-bg); border-radius: 10px; overflow: hidden; margin-bottom: 28px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); transition: all 0.3s; border-left: 3px solid var(--primary-color); }
.news-card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(106,13,173,0.2); }
.card-image { width: 100%; height: 200px; object-fit: cover; }
.card-content { padding: 22px; }
.card-title { font-family: 'Playfair Display', serif; font-size: 1.4em; margin: 10px 0 12px 0; font-weight: 700; color: var(--text-color); }
.card-excerpt { color: var(--light-text); margin-bottom: 15px; }
.sidebar-section { background-color: var(--card-bg); padding: 25px; border-radius: 10px; margin-bottom: 25px; box-shadow: 0 5px 20px rgba(0,0,0,0.05); border-top: 3px solid var(--secondary-color); }
.sidebar-title { font-family: 'Playfair Display', serif; font-size: 1.5em; margin-bottom: 20px; color: var(--primary-color); }
.trending-list { list-style: none; }
.trending-item { display: flex; gap: 12px; padding: 15px 0; border-bottom: 1px solid var(--background-color); }
.trending-number { background-color: var(--primary-color); color: white; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-weight: 700; font-size: 0.9em; }
.trending-content h4 { font-size: 0.95em; margin-bottom: 5px; font-weight: 600; }
.trending-meta { font-size: 0.8em; color: var(--light-text); }
.sidebar-article { margin-bottom: 20px; }
.sidebar-article img { width: 100%; border-radius: 6px; margin-bottom: 10px; }
.sidebar-article h4 { font-size: 1em; margin-bottom: 5px; font-weight: 600; }
.sidebar-meta { font-size: 0.85em; color: var(--light-text); }
.newsletter { background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; }
.newsletter .sidebar-title { color: white; }
.newsletter p { margin-bottom: 15px; }
.newsletter-form { display: flex; flex-direction: column; gap: 10px; }
.newsletter-input { padding: 12px; border: none; border-radius: 5px; }
.newsletter-btn { background-color: var(--accent-color); color: var(--text-color); border: none; padding: 12px; border-radius: 5px; font-weight: 600; cursor: pointer; }
.categories-section { margin: 60px 0; }
.categories-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 22px; }
.Category-card { position: relative; border-radius: 10px; overflow: hidden; height: 220px; cursor: pointer; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
.Category-card img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s; }
.Category-card:hover img { transform: scale(1.1); }
.Category-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.85)); padding: 25px 18px 18px; color: white; }
.Category-overlay h3 { font-family: 'Playfair Display', serif; font-size: 1.3em; margin-bottom: 5px; }
.footer { background-color: var(--text-color); color: white; padding: 55px 0 20px; margin-top: 60px; }
.footer-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 35px; margin-bottom: 40px; }
.footer-column h4 { font-family: 'Playfair Display', serif; font-size: 1.3em; margin-bottom: 20px; color: var(--accent-color); }
.footer-column p { color: rgba(255,255,255,0.8); margin-bottom: 10px; }
.social-links { display: flex; gap: 15px; margin-top: 15px; }
.social-link { color: white; text-decoration: none; transition: color 0.3s; }
.social-link:hover { color: var(--accent-color); }
.footer-links { list-style: none; }
.footer-links li { margin-bottom: 10px; }
.footer-links a { color: rgba(255,255,255,0.8); text-decoration: none; transition: color 0.3s; }
.footer-links a:hover { color: var(--accent-color); }
.footer-bottom { text-align: center; padding-top: 30px; border-top: 1px solid rgba(255,255,255,0.2); color: rgba(255,255,255,0.7); }
@media (max-width: 1200px) { .news-grid { grid-template-columns: 1fr; } .categories-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .featured-article { grid-template-columns: 1fr; } .footer-grid { grid-template-columns: 1fr; } }
TEMPLATE

# Template 7 - Modern Blue
cat > "$OUTPUT_DIR/template7.css" << 'TEMPLATE'
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Oswald:wght@400;500;700&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
    --primary-color: #1565C0;
    --secondary-color: #2196F3;
    --accent-color: #42A5F5;
    --background-color: #E3F2FD;
    --text-color: #0D47A1;
    --light-text: #424242;
    --card-bg: #FFFFFF;
}
body { font-family: 'Roboto', sans-serif; background-color: var(--background-color); color: var(--text-color); line-height: 1.6; }
.container { max-width: 1300px; margin: 0 auto; padding: 0 20px; }
.header { background-color: var(--primary-color); color: white; padding: 18px 0; border-bottom: 3px solid var(--accent-color); }
.header .container { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; }
.logo h1 { font-family: 'Oswald', sans-serif; font-size: 2.3em; font-weight: 700; letter-spacing: 1px; }
.tagline { font-size: 0.85em; opacity: 0.9; }
.nav { display: flex; gap: 20px; }
.nav-link { color: white; text-decoration: none; font-weight: 500; position: relative; padding: 8px 0; transition: all 0.3s; }
.nav-link::before { content: ''; position: absolute; bottom: 0; left: 0; width: 0; height: 2px; background-color: var(--accent-color); transition: width 0.3s; }
.nav-link:hover::before { width: 100%; }
.nav-link:hover { color: var(--accent-color); }
.header-actions { display: flex; gap: 10px; }
.search-input { padding: 10px 15px; border: 1px solid var(--accent-color); border-radius: 4px; width: 180px; }
.btn-subscribe { background-color: var(--secondary-color); color: white; border: none; padding: 10px 20px; border-radius: 4px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
.btn-subscribe:hover { background-color: var(--accent-color); transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
.hero-section { margin: 35px 0; }
.featured-article { background-color: var(--card-bg); border-radius: 8px; overflow: hidden; box-shadow: 0 6px 25px rgba(21,101,192,0.15); display: grid; grid-template-columns: 1.5fr 1fr; border: 1px solid var(--accent-color); }
.article-image img { width: 100%; height: 100%; object-fit: cover; }
.article-content { padding: 30px; }
.Category { background-color: var(--primary-color); color: white; padding: 5px 15px; border-radius: 4px; font-size: 0.8em; font-weight: 600; display: inline-block; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px; }
.article-title { font-family: 'Oswald', sans-serif; font-size: 1.8em; margin-bottom: 12px; color: var(--text-color); }
.article-excerpt { color: var(--light-text); margin-bottom: 18px; }
.article-meta { display: flex; gap: 15px; font-size: 0.85em; color: var(--light-text); }
.news-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 30px; margin: 35px 0; }
.section-title { font-family: 'Oswald', sans-serif; font-size: 2em; margin-bottom: 25px; color: var(--primary-color); text-transform: uppercase; letter-spacing: 1px; }
.news-card { background-color: var(--card-bg); border-radius: 6px; overflow: hidden; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); transition: all 0.3s; }
.news-card:hover { transform: translateY(-4px); box-shadow: 0 8px 25px rgba(21,101,192,0.2); }
.card-image { width: 100%; height: 180px; object-fit: cover; }
.card-content { padding: 20px; }
.card-title { font-family: 'Oswald', sans-serif; font-size: 1.2em; margin: 8px 0 10px 0; font-weight: 600; color: var(--text-color); }
.card-excerpt { color: var(--light-text); margin-bottom: 12px; }
.sidebar-section { background-color: var(--card-bg); padding: 22px; border-radius: 6px; margin-bottom: 22px; box-shadow: 0 4px 15px rgba(0,0,0,0.06); }
.sidebar-title { font-family: 'Oswald', sans-serif; font-size: 1.3em; margin-bottom: 18px; color: var(--primary-color); text-transform: uppercase; letter-spacing: 1px; }
.trending-list { list-style: none; }
.trending-item { display: flex; gap: 12px; padding: 12px 0; border-bottom: 1px solid var(--background-color); }
.trending-number { background-color: var(--primary-color); color: white; width: 25px; height: 25px; display: flex; align-items: center; justify-content: center; border-radius: 4px; font-weight: 700; font-size: 0.85em; }
.trending-content h4 { font-size: 0.9em; margin-bottom: 4px; font-weight: 600; }
.trending-meta { font-size: 0.75em; color: var(--light-text); }
.sidebar-article { margin-bottom: 18px; }
.sidebar-article img { width: 100%; border-radius: 4px; margin-bottom: 8px; }
.sidebar-article h4 { font-size: 0.95em; margin-bottom: 5px; font-weight: 600; }
.sidebar-meta { font-size: 0.8em; color: var(--light-text); }
.newsletter { background-color: var(--primary-color); color: white; }
.newsletter .sidebar-title { color: white; }
.newsletter p { margin-bottom: 12px; }
.newsletter-form { display: flex; flex-direction: column; gap: 8px; }
.newsletter-input { padding: 10px; border: none; border-radius: 4px; }
.newsletter-btn { background-color: var(--accent-color); color: white; border: none; padding: 10px; border-radius: 4px; font-weight: 600; cursor: pointer; }
.categories-section { margin: 50px 0; }
.categories-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
.Category-card { position: relative; border-radius: 6px; overflow: hidden; height: 200px; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.Category-card img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s; }
.Category-card:hover img { transform: scale(1.05); }
.Category-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.8)); padding: 20px 15px 15px; color: white; }
.Category-overlay h3 { font-family: 'Oswald', sans-serif; font-size: 1.1em; margin-bottom: 4px; }
.footer { background-color: var(--text-color); color: white; padding: 45px 0 18px; margin-top: 50px; }
.footer-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 30px; margin-bottom: 35px; }
.footer-column h4 { font-family: 'Oswald', sans-serif; font-size: 1.2em; margin-bottom: 18px; text-transform: uppercase; letter-spacing: 1px; }
.footer-column p { color: rgba(255,255,255,0.8); margin-bottom: 8px; }
.social-links { display: flex; gap: 12px; margin-top: 12px; }
.social-link { color: white; text-decoration: none; transition: color 0.3s; }
.social-link:hover { color: var(--accent-color); }
.footer-links { list-style: none; }
.footer-links li { margin-bottom: 8px; }
.footer-links a { color: rgba(255,255,255,0.8); text-decoration: none; transition: color 0.3s; }
.footer-links a:hover { color: var(--accent-color); }
.footer-bottom { text-align: center; padding-top: 25px; border-top: 1px solid rgba(255,255,255,0.2); color: rgba(255,255,255,0.7); }
@media (max-width: 1200px) { .news-grid { grid-template-columns: 1fr; } .categories-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .featured-article { grid-template-columns: 1fr; } .footer-grid { grid-template-columns: 1fr; } }
TEMPLATE

# Template 8 - Warm Terracotta
cat > "$OUTPUT_DIR/template8.css" << 'TEMPLATE'
@import url('https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600;700&family=Lato:wght@300;400;700&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
    --primary-color: #C62828;
    --secondary-color: #EF5350;
    --accent-color: #FFAB91;
    --background-color: #FFFBF0;
    --text-color: #4E342E;
    --light-text: #8D6E63;
    --card-bg: #FFFFFF;
}
body { font-family: 'Lato', sans-serif; background-color: var(--background-color); color: var(--text-color); line-height: 1.7; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
.header { background-color: var(--primary-color); color: white; padding: 20px 0; box-shadow: 0 4px 12px rgba(198,40,40,0.3); }
.header .container { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px; }
.logo h1 { font-family: 'Crimson Text', serif; font-size: 2.4em; font-weight: 700; }
.tagline { font-size: 0.85em; opacity: 0.9; }
.nav { display: flex; gap: 20px; }
.nav-link { color: white; text-decoration: none; font-weight: 500; transition: all 0.3s; padding: 5px 10px; border-radius: 4px; }
.nav-link:hover { background-color: var(--accent-color); color: var(--text-color); }
.header-actions { display: flex; gap: 10px; }
.search-input { padding: 10px 15px; border: 1px solid var(--accent-color); border-radius: 20px; width: 180px; }
.btn-subscribe { background-color: var(--secondary-color); color: white; border: none; padding: 10px 20px; border-radius: 20px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
.btn-subscribe:hover { background-color: var(--accent-color); color: var(--text-color); transform: translateY(-2px); }
.hero-section { margin: 40px 0; }
.featured-article { background-color: var(--card-bg); border-radius: 10px; overflow: hidden; box-shadow: 0 8px 30px rgba(198,40,40,0.15); display: grid; grid-template-columns: 1.5fr 1fr; border-left: 5px solid var(--primary-color); }
.article-image img { width: 100%; height: 100%; object-fit: cover; }
.article-content { padding: 35px; }
.Category { background-color: var(--primary-color); color: white; padding: 6px 16px; border-radius: 20px; font-size: 0.8em; font-weight: 600; display: inline-block; margin-bottom: 15px; }
.article-title { font-family: 'Crimson Text', serif; font-size: 2em; margin-bottom: 15px; color: var(--primary-color); }
.article-excerpt { color: var(--light-text); margin-bottom: 20px; }
.article-meta { display: flex; gap: 18px; font-size: 0.9em; color: var(--light-text); }
.news-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 30px; margin: 40px 0; }
.section-title { font-family: 'Crimson Text', serif; font-size: 2.1em; margin-bottom: 30px; color: var(--primary-color); }
.news-card { background-color: var(--card-bg); border-radius: 8px; overflow: hidden; margin-bottom: 25px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); transition: all 0.3s; }
.news-card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(198,40,40,0.2); }
.card-image { width: 100%; height: 200px; object-fit: cover; }
.card-content { padding: 22px; }
.card-title { font-family: 'Crimson Text', serif; font-size: 1.4em; margin: 10px 0 12px 0; font-weight: 600; color: var(--text-color); }
.card-excerpt { color: var(--light-text); margin-bottom: 15px; }
.sidebar-section { background-color: var(--card-bg); padding: 25px; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 5px 20px rgba(0,0,0,0.06); }
.sidebar-title { font-family: 'Crimson Text', serif; font-size: 1.4em; margin-bottom: 20px; color: var(--primary-color); }
.trending-list { list-style: none; }
.trending-item { display: flex; gap: 12px; padding: 15px 0; border-bottom: 1px solid var(--background-color); }
.trending-number { background-color: var(--primary-color); color: white; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-weight: 700; font-size: 0.9em; }
.trending-content h4 { font-size: 0.95em; margin-bottom: 5px; font-weight: 600; }
.trending-meta { font-size: 0.8em; color: var(--light-text); }
.sidebar-article { margin-bottom: 20px; }
.sidebar-article img { width: 100%; border-radius: 6px; margin-bottom: 10px; }
.sidebar-article h4 { font-size: 1em; margin-bottom: 5px; font-weight: 600; }
.sidebar-meta { font-size: 0.85em; color: var(--light-text); }
.newsletter { background-color: var(--primary-color); color: white; }
.newsletter .sidebar-title { color: white; }
.newsletter p { margin-bottom: 15px; }
.newsletter-form { display: flex; flex-direction: column; gap: 10px; }
.newsletter-input { padding: 12px; border: none; border-radius: 5px; }
.newsletter-btn { background-color: var(--accent-color); color: var(--text-color); border: none; padding: 12px; border-radius: 5px; font-weight: 600; cursor: pointer; }
.categories-section { margin: 60px 0; }
.categories-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.Category-card { position: relative; border-radius: 8px; overflow: hidden; height: 220px; cursor: pointer; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
.Category-card img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s; }
.Category-card:hover img { transform: scale(1.1); }
.Category-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.8)); padding: 25px 18px 18px; color: white; }
.Category-overlay h3 { font-family: 'Crimson Text', serif; font-size: 1.2em; margin-bottom: 5px; }
.footer { background-color: var(--text-color); color: white; padding: 50px 0 20px; margin-top: 60px; }
.footer-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 35px; margin-bottom: 40px; }
.footer-column h4 { font-family: 'Crimson Text', serif; font-size: 1.2em; margin-bottom: 20px; }
.footer-column p { color: rgba(255,255,255,0.8); margin-bottom: 10px; }
.social-links { display: flex; gap: 15px; margin-top: 15px; }
.social-link { color: white; text-decoration: none; transition: color 0.3s; }
.social-link:hover { color: var(--accent-color); }
.footer-links { list-style: none; }
.footer-links li { margin-bottom: 10px; }
.footer-links a { color: rgba(255,255,255,0.8); text-decoration: none; transition: color 0.3s; }
.footer-links a:hover { color: var(--accent-color); }
.footer-bottom { text-align: center; padding-top: 30px; border-top: 1px solid rgba(255,255,255,0.2); color: rgba(255,255,255,0.7); }
@media (max-width: 1200px) { .news-grid { grid-template-columns: 1fr; } .categories-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .featured-article { grid-template-columns: 1fr; } .footer-grid { grid-template-columns: 1fr; } }
TEMPLATE

# Template 9 - Fresh Mint
cat > "$OUTPUT_DIR/template9.css" << 'TEMPLATE'
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Quicksand:wght@400;500;600;700&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
    --primary-color: #009688;
    --secondary-color: #26A69A;
    --accent-color: #80CBC4;
    --background-color: #E0F2F1;
    --text-color: #004D40;
    --light-text: #4DB6AC;
    --card-bg: #FFFFFF;
}
body { font-family: 'Nunito', sans-serif; background-color: var(--background-color); color: var(--text-color); line-height: 1.7; }
.container { max-width: 1250px; margin: 0 auto; padding: 0 25px; }
.header { background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; padding: 20px 0; }
.header .container { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px; }
.logo h1 { font-family: 'Quicksand', cursive; font-size: 2.3em; font-weight: 800; letter-spacing: 1px; }
.tagline { font-size: 0.85em; opacity: 0.9; }
.nav { display: flex; gap: 22px; }
.nav-link { color: white; text-decoration: none; font-weight: 600; transition: all 0.3s; position: relative; padding-bottom: 5px; }
.nav-link::before { content: ''; position: absolute; bottom: 0; left: 50%; width: 0; height: 2px; background-color: var(--accent-color); transition: all 0.3s; transform: translateX(-50%); }
.nav-link:hover::before { width: 100%; }
.nav-link:hover { color: var(--accent-color); transform: translateY(-2px); }
.header-actions { display: flex; gap: 12px; }
.search-input { padding: 10px 18px; border: 1px solid white; border-radius: 30px; width: 180px; background-color: rgba(255,255,255,0.2); color: white; }
.search-input::placeholder { color: rgba(255,255,255,0.7); }
.btn-subscribe { background-color: white; color: var(--primary-color); border: none; padding: 10px 22px; border-radius: 30px; font-weight: 700; cursor: pointer; transition: all 0.3s; text-transform: uppercase; font-size: 0.9em; }
.btn-subscribe:hover { background-color: var(--accent-color); transform: translateY(-3px); box-shadow: 0 6px 15px rgba(0,0,0,0.15); }
.hero-section { margin: 40px 0; }
.featured-article { background-color: var(--card-bg); border-radius: 12px; overflow: hidden; box-shadow: 0 10px 35px rgba(0,150,136,0.15); display: grid; grid-template-columns: 1.6fr 1fr; border: 2px solid var(--accent-color); }
.article-image img { width: 100%; height: 100%; object-fit: cover; }
.article-content { padding: 38px; }
.Category { background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; padding: 7px 20px; border-radius: 25px; font-size: 0.8em; font-weight: 700; display: inline-block; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }
.article-title { font-family: 'Quicksand', cursive; font-size: 2.1em; margin-bottom: 15px; color: var(--primary-color); }
.article-excerpt { color: var(--light-text); margin-bottom: 20px; }
.article-meta { display: flex; gap: 18px; font-size: 0.9em; color: var(--light-text); font-weight: 600; }
.news-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 35px; margin: 40px 0; }
.section-title { font-family: 'Quicksand', cursive; font-size: 2.2em; margin-bottom: 30px; color: var(--primary-color); letter-spacing: 1px; }
.news-card { background-color: var(--card-bg); border-radius: 10px; overflow: hidden; margin-bottom: 28px; box-shadow: 0 6px 20px rgba(0,0,0,0.08); transition: all 0.3s; border-top: 3px solid var(--primary-color); }
.news-card:hover { transform: translateY(-6px); box-shadow: 0 12px 35px rgba(0,150,136,0.2); }
.card-image { width: 100%; height: 210px; object-fit: cover; }
.card-content { padding: 24px; }
.card-title { font-family: 'Quicksand', cursive; font-size: 1.4em; margin: 10px 0 12px 0; font-weight: 700; color: var(--text-color); }
.card-excerpt { color: var(--light-text); margin-bottom: 15px; }
.sidebar-section { background-color: var(--card-bg); padding: 28px; border-radius: 10px; margin-bottom: 28px; box-shadow: 0 6px 20px rgba(0,0,0,0.06); }
.sidebar-title { font-family: 'Quicksand', cursive; font-size: 1.5em; margin-bottom: 22px; color: var(--primary-color); letter-spacing: 1px; }
.trending-list { list-style: none; }
.trending-item { display: flex; gap: 15px; padding: 16px 0; border-bottom: 1px solid var(--background-color); }
.trending-number { background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; border-radius: 8px; font-weight: 700; font-size: 1em; }
.trending-content h4 { font-size: 0.95em; margin-bottom: 6px; font-weight: 600; }
.trending-meta { font-size: 0.8em; color: var(--light-text); font-weight: 500; }
.sidebar-article { margin-bottom: 22px; }
.sidebar-article img { width: 100%; border-radius: 8px; margin-bottom: 12px; }
.sidebar-article h4 { font-size: 1em; margin-bottom: 6px; font-weight: 600; }
.sidebar-meta { font-size: 0.85em; color: var(--light-text); }
.newsletter { background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; }
.newsletter .sidebar-title { color: white; }
.newsletter p { margin-bottom: 16px; }
.newsletter-form { display: flex; flex-direction: column; gap: 12px; }
.newsletter-input { padding: 13px; border: none; border-radius: 6px; }
.newsletter-btn { background-color: white; color: var(--primary-color); border: none; padding: 13px; border-radius: 6px; font-weight: 700; cursor: pointer; text-transform: uppercase; }
.categories-section { margin: 65px 0; }
.categories-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 22px; }
.Category-card { position: relative; border-radius: 10px; overflow: hidden; height: 230px; cursor: pointer; box-shadow: 0 6px 18px rgba(0,0,0,0.1); }
.Category-card img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s; }
.Category-card:hover img { transform: scale(1.12); }
.Category-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,77,64,0.9)); padding: 30px 20px 20px; color: white; }
.Category-overlay h3 { font-family: 'Quicksand', cursive; font-size: 1.3em; margin-bottom: 6px; }
.footer { background: linear-gradient(135deg, var(--text-color), var(--primary-color)); color: white; padding: 55px 0 22px; margin-top: 65px; }
.footer-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 40px; margin-bottom: 42px; }
.footer-column h4 { font-family: 'Quicksand', cursive; font-size: 1.4em; margin-bottom: 22px; letter-spacing: 1px; }
.footer-column p { color: rgba(255,255,255,0.85); margin-bottom: 12px; }
.social-links { display: flex; gap: 18px; margin-top: 18px; }
.social-link { color: white; text-decoration: none; font-weight: 600; transition: all 0.3s; text-transform: uppercase; font-size: 0.9em; }
.social-link:hover { color: var(--accent-color); transform: translateY(-2px); }
.footer-links { list-style: none; }
.footer-links li { margin-bottom: 12px; }
.footer-links a { color: rgba(255,255,255,0.85); text-decoration: none; transition: color 0.3s; }
.footer-links a:hover { color: var(--accent-color); }
.footer-bottom { text-align: center; padding-top: 32px; border-top: 1px solid rgba(255,255,255,0.25); color: rgba(255,255,255,0.75); }
@media (max-width: 1200px) { .news-grid { grid-template-columns: 1fr; } .categories-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .featured-article { grid-template-columns: 1fr; } .footer-grid { grid-template-columns: 1fr; } }
TEMPLATE

# Template 10 - Rustic Brown
cat > "$OUTPUT_DIR/template10.css" << 'TEMPLATE'
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Open+Sans:wght@400;600;700&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
    --primary-color: #5D4037;
    --secondary-color: #8D6E63;
    --accent-color: #BCAAA4;
    --background-color: #EFEBE0;
    --text-color: #3E2723;
    --light-text: #6D4C41;
    --card-bg: #FFFFFF;
}
body { font-family: 'Open Sans', sans-serif; background-color: var(--background-color); color: var(--text-color); line-height: 1.7; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
.header { background-color: var(--primary-color); color: white; padding: 22px 0; border-bottom: 4px solid var(--secondary-color); }
.header .container { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px; }
.logo h1 { font-family: 'Merriweather', serif; font-size: 2.2em; font-weight: 700; }
.tagline { font-size: 0.85em; opacity: 0.9; }
.nav { display: flex; gap: 20px; }
.nav-link { color: white; text-decoration: none; font-weight: 600; transition: all 0.3s; position: relative; padding: 5px 0; }
.nav-link::after { content: ''; position: absolute; bottom: -5px; left: 0; width: 0; height: 2px; background-color: var(--accent-color); transition: width 0.3s; }
.nav-link:hover::after { width: 100%; }
.nav-link:hover { color: var(--accent-color); }
.header-actions { display: flex; gap: 10px; }
.search-input { padding: 10px 15px; border: 1px solid var(--accent-color); border-radius: 4px; width: 180px; background-color: white; }
.btn-subscribe { background-color: var(--secondary-color); color: white; border: none; padding: 10px 20px; border-radius: 4px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
.btn-subscribe:hover { background-color: var(--accent-color); color: var(--text-color); transform: translateY(-2px); }
.hero-section { margin: 40px 0; }
.featured-article { background-color: var(--card-bg); border-radius: 8px; overflow: hidden; box-shadow: 0 8px 25px rgba(93,64,55,0.15); display: grid; grid-template-columns: 1.5fr 1fr; border: 1px solid var(--accent-color); }
.article-image img { width: 100%; height: 100%; object-fit: cover; }
.article-content { padding: 32px; }
.Category { background-color: var(--primary-color); color: white; padding: 6px 16px; border-radius: 4px; font-size: 0.8em; font-weight: 600; display: inline-block; margin-bottom: 15px; }
.article-title { font-family: 'Merriweather', serif; font-size: 1.9em; margin-bottom: 15px; color: var(--primary-color); }
.article-excerpt { color: var(--light-text); margin-bottom: 20px; }
.article-meta { display: flex; gap: 18px; font-size: 0.9em; color: var(--light-text); }
.news-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 30px; margin: 40px 0; }
.section-title { font-family: 'Merriweather', serif; font-size: 2em; margin-bottom: 30px; color: var(--primary-color); }
.news-card { background-color: var(--card-bg); border-radius: 6px; overflow: hidden; margin-bottom: 25px; box-shadow: 0 5px 18px rgba(0,0,0,0.08); transition: all 0.3s; }
.news-card:hover { transform: translateY(-4px); box-shadow: 0 10px 25px rgba(93,64,55,0.2); }
.card-image { width: 100%; height: 190px; object-fit: cover; }
.card-content { padding: 20px; }
.card-title { font-family: 'Merriweather', serif; font-size: 1.3em; margin: 10px 0 12px 0; font-weight: 700; color: var(--text-color); }
.card-excerpt { color: var(--light-text); margin-bottom: 15px; }
.sidebar-section { background-color: var(--card-bg); padding: 24px; border-radius: 6px; margin-bottom: 24px; box-shadow: 0 5px 18px rgba(0,0,0,0.06); }
.sidebar-title { font-family: 'Merriweather', serif; font-size: 1.4em; margin-bottom: 20px; color: var(--primary-color); }
.trending-list { list-style: none; }
.trending-item { display: flex; gap: 12px; padding: 15px 0; border-bottom: 1px solid var(--background-color); }
.trending-number { background-color: var(--primary-color); color: white; width: 26px; height: 26px; display: flex; align-items: center; justify-content: center; border-radius: 4px; font-weight: 700; font-size: 0.85em; }
.trending-content h4 { font-size: 0.95em; margin-bottom: 5px; font-weight: 600; }
.trending-meta { font-size: 0.8em; color: var(--light-text); }
.sidebar-article { margin-bottom: 20px; }
.sidebar-article img { width: 100%; border-radius: 4px; margin-bottom: 10px; }
.sidebar-article h4 { font-size: 1em; margin-bottom: 5px; font-weight: 600; }
.sidebar-meta { font-size: 0.85em; color: var(--light-text); }
.newsletter { background-color: var(--primary-color); color: white; }
.newsletter .sidebar-title { color: white; }
.newsletter p { margin-bottom: 15px; }
.newsletter-form { display: flex; flex-direction: column; gap: 10px; }
.newsletter-input { padding: 12px; border: none; border-radius: 4px; }
.newsletter-btn { background-color: var(--accent-color); color: var(--text-color); border: none; padding: 12px; border-radius: 4px; font-weight: 600; cursor: pointer; }
.categories-section { margin: 60px 0; }
.categories-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.Category-card { position: relative; border-radius: 6px; overflow: hidden; height: 210px; cursor: pointer; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
.Category-card img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s; }
.Category-card:hover img { transform: scale(1.08); }
.Category-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.8)); padding: 25px 18px 18px; color: white; }
.Category-overlay h3 { font-family: 'Merriweather', serif; font-size: 1.2em; margin-bottom: 5px; }
.footer { background-color: var(--text-color); color: white; padding: 50px 0 20px; margin-top: 60px; }
.footer-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 35px; margin-bottom: 40px; }
.footer-column h4 { font-family: 'Merriweather', serif; font-size: 1.2em; margin-bottom: 20px; }
.footer-column p { color: rgba(255,255,255,0.8); margin-bottom: 10px; }
.social-links { display: flex; gap: 15px; margin-top: 15px; }
.social-link { color: white; text-decoration: none; transition: color 0.3s; }
.social-link:hover { color: var(--accent-color); }
.footer-links { list-style: none; }
.footer-links li { margin-bottom: 10px; }
.footer-links a { color: rgba(255,255,255,0.8); text-decoration: none; transition: color 0.3s; }
.footer-links a:hover { color: var(--accent-color); }
.footer-bottom { text-align: center; padding-top: 30px; border-top: 1px solid rgba(255,255,255,0.2); color: rgba(255,255,255,0.7); }
@media (max-width: 1200px) { .news-grid { grid-template-columns: 1fr; } .categories-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .featured-article { grid-template-columns: 1fr; } .footer-grid { grid-template-columns: 1fr; } }
TEMPLATE

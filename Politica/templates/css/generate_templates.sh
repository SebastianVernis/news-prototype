#!/bin/bash

# Template 4 - Minimalist Green
cat > template4.css << 'TEMPLATE'
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Source+Serif+Pro:wght@400;700&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
    --primary-color: #2D6A4F;
    --secondary-color: #52B788;
    --accent-color: #95D5B2;
    --background-color: #F1FAEE;
    --text-color: #1B4332;
    --light-text: #74C69D;
    --card-bg: #FFFFFF;
}
body { font-family: 'Inter', sans-serif; background-color: var(--background-color); color: var(--text-color); line-height: 1.6; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
.header { background-color: white; padding: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.header .container { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px; }
.logo h1 { font-family: 'Source Serif Pro', serif; font-size: 2.2em; color: var(--primary-color); font-weight: 800; }
.tagline { font-size: 0.85em; color: var(--secondary-color); }
.nav { display: flex; gap: 20px; }
.nav-link { color: var(--text-color); text-decoration: none; font-weight: 500; transition: color 0.3s; }
.nav-link:hover { color: var(--secondary-color); }
.header-actions { display: flex; gap: 10px; }
.search-input { padding: 10px 15px; border: 1px solid var(--accent-color); border-radius: 5px; width: 200px; }
.btn-subscribe { background-color: var(--primary-color); color: white; border: none; padding: 10px 20px; border-radius: 5px; font-weight: 600; cursor: pointer; }
.hero-section { margin: 40px 0; }
.featured-article { background-color: var(--card-bg); border-radius: 10px; overflow: hidden; box-shadow: 0 3px 15px rgba(0,0,0,0.08); display: grid; grid-template-columns: 1.5fr 1fr; }
.article-image img { width: 100%; height: 100%; object-fit: cover; }
.article-content { padding: 40px; }
.category { background-color: var(--secondary-color); color: white; padding: 5px 15px; border-radius: 15px; font-size: 0.8em; font-weight: 600; display: inline-block; margin-bottom: 15px; }
.article-title { font-family: 'Source Serif Pro', serif; font-size: 2em; font-weight: 700; margin-bottom: 15px; color: var(--primary-color); }
.article-excerpt { color: var(--light-text); margin-bottom: 20px; }
.article-meta { display: flex; gap: 15px; font-size: 0.85em; color: var(--light-text); }
.news-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 30px; margin: 40px 0; }
.section-title { font-family: 'Source Serif Pro', serif; font-size: 2em; margin-bottom: 30px; color: var(--primary-color); }
.news-card { background-color: var(--card-bg); border-radius: 8px; overflow: hidden; margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); transition: transform 0.3s; }
.news-card:hover { transform: translateY(-5px); }
.card-image { width: 100%; height: 220px; object-fit: cover; }
.card-content { padding: 25px; }
.card-title { font-family: 'Source Serif Pro', serif; font-size: 1.4em; margin: 10px 0 15px 0; font-weight: 700; color: var(--primary-color); }
.card-excerpt { color: var(--light-text); margin-bottom: 15px; }
.sidebar-section { background-color: var(--card-bg); padding: 25px; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); }
.sidebar-title { font-family: 'Source Serif Pro', serif; font-size: 1.3em; margin-bottom: 20px; color: var(--primary-color); }
.trending-list { list-style: none; }
.trending-item { display: flex; gap: 15px; padding: 15px 0; border-bottom: 1px solid var(--accent-color); }
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

# Template 5 - Bold Orange
cat > template5.css << 'TEMPLATE'
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Raleway:wght@300;400;600;800&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
    --primary-color: #FF6F00;
    --secondary-color: #FFA726;
    --accent-color: #FFD54F;
    --background-color: #FFF8E1;
    --text-color: #E65100;
    --light-text: #FF8A50;
    --card-bg: #FFFFFF;
}
body { font-family: 'Raleway', sans-serif; background-color: var(--background-color); color: var(--text-color); line-height: 1.7; }
.container { max-width: 1350px; margin: 0 auto; padding: 0 20px; }
.header { background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; padding: 25px 0; }
.header .container { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px; }
.logo h1 { font-family: 'Bebas Neue', cursive; font-size: 3.5em; letter-spacing: 3px; }
.tagline { font-size: 0.9em; font-weight: 600; letter-spacing: 2px; }
.nav { display: flex; gap: 25px; }
.nav-link { color: white; text-decoration: none; font-weight: 600; text-transform: uppercase; font-size: 0.9em; transition: all 0.3s; }
.nav-link:hover { color: var(--accent-color); transform: translateY(-2px); }
.header-actions { display: flex; gap: 15px; }
.search-input { padding: 12px 20px; border: 2px solid white; border-radius: 30px; width: 220px; background-color: rgba(255,255,255,0.2); color: white; }
.search-input::placeholder { color: rgba(255,255,255,0.8); }
.btn-subscribe { background-color: white; color: var(--primary-color); border: none; padding: 12px 28px; border-radius: 30px; font-weight: 800; cursor: pointer; text-transform: uppercase; font-size: 0.9em; transition: all 0.3s; }
.btn-subscribe:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.2); }
.hero-section { margin: 45px 0; }
.featured-article { background-color: var(--card-bg); border-radius: 15px; overflow: hidden; box-shadow: 0 10px 40px rgba(255,111,0,0.2); display: grid; grid-template-columns: 1.7fr 1fr; border: 3px solid var(--primary-color); }
.article-image img { width: 100%; height: 100%; object-fit: cover; }
.article-content { padding: 45px; }
.category { background-color: var(--primary-color); color: white; padding: 8px 20px; border-radius: 25px; font-size: 0.85em; font-weight: 800; display: inline-block; margin-bottom: 18px; text-transform: uppercase; letter-spacing: 2px; }
.article-title { font-family: 'Bebas Neue', cursive; font-size: 3em; margin-bottom: 18px; line-height: 1.1; }
.article-excerpt { color: var(--light-text); margin-bottom: 25px; font-size: 1.1em; }
.article-meta { display: flex; gap: 20px; font-size: 0.95em; color: var(--light-text); font-weight: 600; }
.news-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 40px; margin: 45px 0; }
.section-title { font-family: 'Bebas Neue', cursive; font-size: 3em; margin-bottom: 35px; color: var(--primary-color); letter-spacing: 2px; }
.news-card { background-color: var(--card-bg); border-radius: 12px; overflow: hidden; margin-bottom: 30px; box-shadow: 0 5px 20px rgba(255,111,0,0.15); transition: all 0.3s; border: 2px solid transparent; }
.news-card:hover { transform: translateY(-8px); box-shadow: 0 10px 40px rgba(255,111,0,0.3); border-color: var(--secondary-color); }
.card-image { width: 100%; height: 240px; object-fit: cover; }
.card-content { padding: 28px; }
.card-title { font-family: 'Bebas Neue', cursive; font-size: 2em; margin: 12px 0 18px 0; letter-spacing: 1px; }
.card-excerpt { color: var(--light-text); margin-bottom: 18px; line-height: 1.7; }
.sidebar-section { background-color: var(--card-bg); padding: 28px; border-radius: 12px; margin-bottom: 28px; box-shadow: 0 5px 20px rgba(255,111,0,0.15); }
.sidebar-title { font-family: 'Bebas Neue', cursive; font-size: 2em; margin-bottom: 22px; color: var(--primary-color); letter-spacing: 1px; }
.trending-list { list-style: none; }
.trending-item { display: flex; gap: 15px; padding: 18px 0; border-bottom: 2px solid var(--background-color); }
.trending-number { background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; width: 35px; height: 35px; display: flex; align-items: center; justify-content: center; border-radius: 8px; font-weight: 800; font-family: 'Bebas Neue', cursive; font-size: 1.3em; }
.trending-content h4 { font-size: 1em; margin-bottom: 8px; font-weight: 700; }
.trending-meta { font-size: 0.85em; color: var(--light-text); font-weight: 600; }
.sidebar-article { margin-bottom: 22px; }
.sidebar-article img { width: 100%; border-radius: 8px; margin-bottom: 12px; }
.sidebar-article h4 { font-size: 1.1em; margin-bottom: 8px; font-weight: 700; }
.sidebar-meta { font-size: 0.9em; color: var(--light-text); }
.newsletter { background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; }
.newsletter .sidebar-title { color: white; }
.newsletter p { margin-bottom: 18px; }
.newsletter-form { display: flex; flex-direction: column; gap: 12px; }
.newsletter-input { padding: 15px; border: 2px solid white; border-radius: 8px; background-color: rgba(255,255,255,0.2); color: white; }
.newsletter-input::placeholder { color: rgba(255,255,255,0.8); }
.newsletter-btn { background-color: white; color: var(--primary-color); border: none; padding: 15px; border-radius: 8px; font-weight: 800; cursor: pointer; text-transform: uppercase; }
.categories-section { margin: 70px 0; }
.categories-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 25px; }
.category-card { position: relative; border-radius: 12px; overflow: hidden; height: 260px; cursor: pointer; border: 3px solid var(--primary-color); }
.category-card img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s; }
.category-card:hover img { transform: scale(1.15); }
.category-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(255,111,0,0.95)); padding: 35px 22px 22px; color: white; }
.category-overlay h3 { font-family: 'Bebas Neue', cursive; font-size: 1.8em; margin-bottom: 8px; letter-spacing: 1px; }
.footer { background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; padding: 65px 0 25px; margin-top: 70px; }
.footer-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 45px; margin-bottom: 45px; }
.footer-column h4 { font-family: 'Bebas Neue', cursive; font-size: 1.8em; margin-bottom: 22px; letter-spacing: 1px; }
.footer-column p { color: rgba(255,255,255,0.9); margin-bottom: 12px; }
.social-links { display: flex; gap: 18px; margin-top: 18px; }
.social-link { color: white; text-decoration: none; font-weight: 700; transition: all 0.3s; text-transform: uppercase; font-size: 0.9em; }
.social-link:hover { color: var(--accent-color); transform: translateY(-2px); }
.footer-links { list-style: none; }
.footer-links li { margin-bottom: 12px; }
.footer-links a { color: rgba(255,255,255,0.9); text-decoration: none; transition: color 0.3s; }
.footer-links a:hover { color: var(--accent-color); }
.footer-bottom { text-align: center; padding-top: 35px; border-top: 2px solid rgba(255,255,255,0.3); }
@media (max-width: 1200px) { .news-grid { grid-template-columns: 1fr; } .categories-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .featured-article { grid-template-columns: 1fr; } .footer-grid { grid-template-columns: 1fr; } }
TEMPLATE


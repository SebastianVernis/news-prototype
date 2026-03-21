#!/bin/bash

set -e

cd /home/sebastianvernis/ProyectosActivos/cloudflare-news-project

echo "Configurando Tokens copia y pega el siguiente token 
'17f616e5c86c4988d2f6a6955ba9a98bc3c7ddda4c3557286ba3b80f8aa76291'"
cd cms-originaux && wrangler secret put ADMIN_TOKEN
cd ../cms-nuevos && wrangler secret put ADMIN_TOKEN
cd ../cms-nuevos2 && wrangler secret put ADMIN_TOKEN

cd ..

echo "Creando tablas en las bases de datos..."
wrangler d1 execute news_db_cms_originaux --file=cms-originaux/schema.sql --remote
wrangler d1 execute news_db_cms_nuevos --file=cms-nuevos/schema.sql --remote
wrangler d1 execute news_db_cms_nuevos2 --file=cms-nuevos2/schema.sql --remote

cd cms-nuevos2

cat > insert_sitios.sql << 'SQLEOF'
INSERT OR REPLACE INTO SITIOS (ID, SLUG, NOMBRE, DOMINIO, TAGLINE, TEMPLATE_ID, ACTIVO, FACEBOOK_ACTIVO) VALUES
('centronews', 'centronews', 'CentroNews', 'centronews.sebastianvernis.space', 'Noticias Corporativas', 1, 1, 1),
('noticias123', 'noticias123', 'Noticias123', 'noticias123.sebastianvernis.space', 'Última Hora', 1, 1, 1),
('breakingcentermexico', 'breakingcentermexico', 'BreakingCenter México', 'breakingcentermexico.sebastianvernis.space', 'Noticias Urgentes', 1, 1, 1),
('alavistanoticias', 'alavistanoticias', 'A La Vista Noticias', 'alavistanoticias.sebastianvernis.space', 'Revista Digital', 1, 1, 1),
('socialmexiconews', 'socialmexiconews', 'SocialMexico News', 'socialmexiconews.sebastianvernis.space', 'Viral y Entretenimiento', 1, 1, 1),
('tmznews', 'tmznews', 'TMZNews', 'tmznews.sebastianvernis.space', 'Espectáculos y Gossip', 1, 1, 1),
('radioabc', 'radioabc', 'RadioABC', 'radioabc.sebastianvernis.space', 'Noticias Institucionales', 1, 1, 1),
('noticiasintegra', 'noticiasintegra', 'Noticias Integra', 'noticiasintegra.sebastianvernis.space', 'Periodismo de Investigación', 1, 1, 1);
SQLEOF

wrangler d1 execute news_db_cms_nuevos2 --file=insert_sitios.sql --remote
wrangler d1 execute news_db_cms_nuevos2 --command "SELECT ID, SLUG, NOMBRE FROM SITIOS" --remote

cd ..

cd cms-originaux && ./deploy.sh
cd ../cms-nuevos && ./deploy.sh
cd ../cms-nuevos2 && ./deploy.sh

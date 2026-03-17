
      INSERT INTO ARTICULOS_PARAFRASEADOS (
        ID, ID_ARTICULO_ORIGINAL, TITULO_PARAFRASEADO, SLUG, 
        DESCRIPCION_PARAFRASEADA, CONTENIDO, CATEGORIA, AUTOR, 
        FECHA_PUBLICACION, URL_IMAGEN, SITIO_DESTINO, DESTACADO, 
        VISTAS, ESTADO, FB_REQUERIDO, ES_BREVE
      ) VALUES (
        'https://actualidad.rt.com/actualidad/588842-atacan-balazos-alcaldesa-mexicana-matar-hijo', 
        'https://actualidad.rt.com/actualidad/588842-atacan-balazos-alcaldesa-mexicana-matar-hijo',
        'Alcaldesa mexicana recibe disparos; su hijo muere en ataque',
        'alcaldesa-mexicana-recibe-disparos-su-hijo-muere-en-ataque',
        'Nora Alicia Biebrich fue sorprendida durante su trayecto por una vía de comunicación en México.',
        'La alcaldesa de Bacanora, Nora Alicia Biebrich, resultó herida en un ataque armado ocurrido este maes en la carretera Huetamo-Mazatlán, fuentes oficiales. El incidente se saldó con la muee, quien falleció debido a las heridas sufridas en el ataque. La funcionaria municipal sobrevivió a las lesiones provocadas.',
        'NACIONAL',
        'Redacción',
        '2026-02-26T03:54:54.479Z',
        'https://mfes.b37m.ru/actualidad/public_images/2026.02/article/699def7be9ff71613522059c.jpg',
        'mexicoinformado,cbnnoticias,centralmexico',
        0, 0, 'PUBLICADO', 0, 0
      )
      ON CONFLICT(ID) DO NOTHING;
    
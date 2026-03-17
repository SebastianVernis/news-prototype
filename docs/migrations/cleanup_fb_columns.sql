-- Limpieza de columnas Facebook de tablas antiguas
-- Fecha: 2026-03-10
-- Objetivo: Eliminar referencias de Facebook de ARTICULOS_ORIGINALES, ARTICULOS_PARAFRASEADOS y ARTICULOS_CMS
-- La única fuente de verdad para Facebook serán las tablas ARTICULOS_SITIO_{SLUG}

-- ============================================================
-- 1. ARTICULOS_ORIGINALES - No tiene columnas FB, solo verificar
-- ============================================================
-- Esta tabla no tiene columnas de Facebook, está limpia

-- ============================================================
-- 2. ARTICULOS_PARAFRASEADOS - Eliminar columnas FB
-- ============================================================

-- Paso 1: Crear tabla temporal sin columnas FB
CREATE TABLE ARTICULOS_PARAFRASEADOS_NEW AS
SELECT 
  ID,
  ID_ARTICULO_ORIGINAL,
  TITULO_PARAFRASEADO,
  DESCRIPCION_PARAFRASEADA,
  CONTENIDO,
  LONGITUD,
  SITIO_DESTINO,
  CATEGORIA,
  FECHA_PUBLICACION,
  AUTOR,
  VERIFICACION,
  DESTACADO,
  URL_IMAGEN,
  SLUG,
  VISTAS,
  ESTADO,
  ES_BREVE,
  SOURCE_URL
  -- Se eliminan: FB_REQUERIDO, FB_PUBLICADO, FB_FECHA, FB_SITIOS_PUBLICADOS
FROM ARTICULOS_PARAFRASEADOS;

-- Paso 2: Eliminar tabla original
DROP TABLE ARTICULOS_PARAFRASEADOS;

-- Paso 3: Renombrar tabla nueva
ALTER TABLE ARTICULOS_PARAFRASEADOS_NEW RENAME TO ARTICULOS_PARAFRASEADOS;

-- Paso 4: Recrear índices
CREATE INDEX IF NOT EXISTS idx_art_para_sitio ON ARTICULOS_PARAFRASEADOS(SITIO_DESTINO);
CREATE INDEX IF NOT EXISTS idx_art_para_fecha ON ARTICULOS_PARAFRASEADOS(FECHA_PUBLICACION DESC);

-- ============================================================
-- 3. ARTICULOS_CMS - Eliminar columnas FB
-- ============================================================

-- Paso 1: Crear tabla temporal sin columnas FB
CREATE TABLE ARTICULOS_CMS_NEW AS
SELECT 
  ID,
  TITULO,
  SLUG,
  DESCRIPCION,
  CONTENIDO,
  CATEGORIA,
  ID_AUTOR,
  URL_IMAGEN,
  SITIOS_DESTINO,
  ESTADO,
  DESTACADO,
  FECHA_CREACION,
  FECHA_PUBLICACION
  -- Se eliminan: FB_PUBLICADO, FB_FECHA, FB_REQUERIDO, FB_SITIOS_PUBLICADOS
FROM ARTICULOS_CMS;

-- Paso 2: Eliminar tabla original
DROP TABLE ARTICULOS_CMS;

-- Paso 3: Renombrar tabla nueva
ALTER TABLE ARTICULOS_CMS_NEW RENAME TO ARTICULOS_CMS;

-- Paso 4: Recrear índices
CREATE INDEX IF NOT EXISTS idx_art_cms_estado ON ARTICULOS_CMS(ESTADO);

-- ============================================================
-- 4. Verificación final
-- ============================================================

-- Verificar que ARTICULOS_PARAFRASEADOS no tiene columnas FB
-- PRAGMA table_info(ARTICULOS_PARAFRASEADOS);

-- Verificar que ARTICULOS_CMS no tiene columnas FB
-- PRAGMA table_info(ARTICULOS_CMS);

-- Verificar que ARTICULOS_SITIO_* tienen las columnas FB
-- PRAGMA table_info(ARTICULOS_SITIO_RADIOCINCONOTICIAS);

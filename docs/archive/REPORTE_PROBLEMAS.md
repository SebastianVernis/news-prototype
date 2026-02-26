# 📋 Reporte de Artículos con Problemas

**Fecha:** 2026-02-26  
**Base de datos:** news_db (remota)

---

## 🔤 ARTÍCULOS CON PROBLEMAS DE ENCODING

Estos artículos aún tienen caracteres con encoding incorrecto (ISO-8859-1 en lugar de UTF-8):

### ARTICULOS_ORIGINALES (4 artículos)

| ID | Título | Tabla |
|----|--------|-------|
| `ae2ade95-05f0-4feb-bd12-499467bea5d2` | Inter de Miami es goleado por el LAFC y arranca con derrota la defensa del título en la MLS 2026 | ORIGINALES |
| `a1cab324-1ee2-4010-bc93-b1415f58fa94` | Lionel Messi podría enfrentar sanción; la MLS investigará al argentino por sus reclamos arbitrales | ORIGINALES |
| `0d442faf-9712-47f2-9ae9-2bcfcefb9ae1` | Secretaría de la Defensa CONFIRMA la muerte de Nemesio Oseguera Cervantes, 'El Mencho', en Jalisco; EU cooperó en operación | ORIGINALES |
| `334fdab0-89c3-4e71-8005-ea91e5ed5df5` | ¿Murió 'El Mencho'? Reportan que Nemesio Oseguera Cervantes fue abatido en Tapalpa, Jalisco | ORIGINALES |

### ARTICULOS_PARAFRASEADOS (1 artículo)

| ID | Título | Tabla |
|----|--------|-------|
| `49e670f9-29b9-439f-9200-29d7da4e5790` | De Ariadne Díaz a conductores de 'Hoy': Estos famosos alzan la voz a violencia por muerte de 'El Mencho' | PARAFRASEADOS |

---

## 🖼️ ARTÍCULOS SIN IMAGEN O CON LOGO PLACEHOLDER

Estos artículos no tienen imagen válida (usan `/logo.png` como placeholder o están sin imagen):

### ARTICULOS_ORIGINALES (12 artículos)

| ID | Título | URL_IMAGEN |
|----|--------|------------|
| `6c0aae6b-0d16-4d05-b1c5-e3e054e41889` | AICM reforzó seguridad; operó sin contratiempos | `/logo.png` |
| `c80c7141-8358-4047-a696-b50ed911d953` | Activos, sólo 7 bloqueos viales en tierra jalisciense | `/logo.png` |
| `d0791469-b788-4354-9b12-c23b1ac26d64` | Agremiados de la CROC podrán acceder a Leche para el Bienestar: Sader | `/logo.png` |
| `ae156f2f-3f29-464f-aab8-2c6323aa5d87` | Alcalde de Vallarta da la cara luego de 27 horas | `/logo.png` |
| `6be083cd-4f24-4a7a-8ded-d6c42c3079ae` | Aplicó el IMSS 670 mil dosis contra sarampión el pasado fin de semana | `/logo.png` |
| `8c4c7865-4c87-49e1-8778-999beaeadc01` | Bernardo Barranco V.: La conspiración de Trump contra el papa Francisco | `/logo.png` |
| `6af316d6-313f-4f6f-b986-8c583659bc0b` | Cancelan al menos 237 vuelos a la región tras la muerte de El Mencho | `NULL` |
| `8bd37295-2c76-4fa9-933b-716a4a4208bb` | Cárdenas, por anular pluris del Senado | `NULL` |
| `dbe861b1-f287-4cdd-bdd5-79159e473c32` | Aspecto en el Senado | `NULL` |
| `9c4c9666-695a-4598-9608-d803d63fe694` | Chinita tú | `NULL` |
| `a0ed37ce-b37b-4f9f-8608-ad976d965c87` | Las Mejores Prepas 2026 | `NULL` |
| `9583bc73-8cb6-4a95-a8c4-933f078491ce` | Mientras México arde | `NULL` |

### ARTICULOS_PARAFRASEADOS (0 artículos)

✅ **Todos los artículos parafraseados tienen imagen válida** (100%)

---

## 📊 RESUMEN

| Problema | ORIGINALES | PARAFRASEADOS | CMS | TOTAL |
|----------|------------|---------------|-----|-------|
| **Encoding incorrecto** | 4 | 1 | 0 | **5** |
| **Sin imagen / Logo placeholder** | 12 | 0 | 0 | **12** |

---

## 🔧 ACCIONES RECOMENDADAS

### Para Encoding:
1. **Revisar manualmente** los 5 artículos listados
2. **Corregir título y contenido** con herramienta de encoding
3. **O eliminar** si el contenido ya no es relevante

### Para Imágenes:
1. **Scraping manual** de las URLs originales para obtener imágenes
2. **O eliminar** artículos que no sean prioritarios
3. **Subir imágenes** desde el CMS para los artículos más importantes

---

## 📝 CONSULTAS SQL PARA LIMPIEZA

### Eliminar artículos con encoding problemático:
```sql
DELETE FROM ARTICULOS_ORIGINALES 
WHERE ID IN (
  'ae2ade95-05f0-4feb-bd12-499467bea5d2',
  'a1cab324-1ee2-4010-bc93-b1415f58fa94',
  '0d442faf-9712-47f2-9ae9-2bcfcefb9ae1',
  '334fdab0-89c3-4e71-8005-ea91e5ed5df5'
);

DELETE FROM ARTICULOS_PARAFRASEADOS 
WHERE ID = '49e670f9-29b9-439f-9200-29d7da4e5790';
```

### Eliminar artículos sin imagen:
```sql
DELETE FROM ARTICULOS_ORIGINALES 
WHERE URL_IMAGEN IS NULL 
   OR URL_IMAGEN = '' 
   OR URL_IMAGEN LIKE '%/logo.png%';
```

---

**Generado automáticamente desde la base de datos**

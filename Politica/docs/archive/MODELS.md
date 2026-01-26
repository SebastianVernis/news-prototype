# 🎨 Modelos de IA Disponibles en Blackbox

## Modelos de Generación de Imágenes

### Recomendados para Noticias

| Modelo | ID | Costo/Imagen | Velocidad | Calidad | Uso Recomendado |
|--------|-----|--------------|-----------|---------|-----------------|
| **Flux Schnell** ⭐ | `blackboxai/black-forest-labs/flux-schnell` | $0.003 | ⚡⚡⚡ Muy rápido | ⭐⭐⭐ Buena | **Default** - Producción masiva |
| **SDXL Lightning** | `blackboxai/bytedance/sdxl-lightning-4step` | $0.0014 | ⚡⚡⚡ Muy rápido | ⭐⭐⭐ Buena | Alternativa económica |
| **Flux Dev** | `blackboxai/black-forest-labs/flux-dev` | $0.025 | ⚡⚡ Rápido | ⭐⭐⭐⭐ Muy buena | Calidad superior |
| **Flux 1.1 Pro** | `blackboxai/black-forest-labs/flux-1.1-pro` | $0.040 | ⚡⚡ Rápido | ⭐⭐⭐⭐⭐ Excelente | Artículos destacados |
| **Flux Pro** | `blackboxai/black-forest-labs/flux-pro` | $0.055 | ⚡ Normal | ⭐⭐⭐⭐⭐ Premium | Máxima calidad |
| **Flux 1.1 Pro Ultra** | `blackboxai/black-forest-labs/flux-1.1-pro-ultra` | $0.060 | ⚡ Normal | ⭐⭐⭐⭐⭐ Ultra | Casos especiales |

### Otros Modelos Disponibles

| Categoría | Modelos |
|-----------|---------|
| **Stable Diffusion** | SDXL, Stable Diffusion, SDXL Emoji |
| **Upscaling** | Clarity Upscaler, Real ESRGAN, Gfpgan, Codeformer |
| **Especializados** | Face To Many, Controlnet Scribble, Kandinsky 2.2 |
| **Análisis** | BLIP, BLIP 2, Llava 13B, Image Tagger, NSFW Detection |

## Modelos de Texto (Parafraseado)

### Recomendados

| Modelo | ID | Costo | Velocidad | Calidad | Uso |
|--------|-----|-------|-----------|---------|-----|
| **GPT-4o** ⭐ | `blackboxai/openai/gpt-4o` | Variable | ⚡⚡ Rápido | ⭐⭐⭐⭐⭐ | **Default** - Mejor calidad |
| **GPT-4** | `blackboxai/openai/gpt-4` | Variable | ⚡ Normal | ⭐⭐⭐⭐⭐ | Alternativa premium |
| **Claude 3.5 Sonnet** | `blackboxai/anthropic/claude-3.5-sonnet` | Variable | ⚡⚡ Rápido | ⭐⭐⭐⭐⭐ | Excelente para escritura |
| **GPT-3.5 Turbo** | `blackboxai/openai/gpt-3.5-turbo` | Económico | ⚡⚡⚡ Muy rápido | ⭐⭐⭐ | Producción masiva |

## Cómo Cambiar de Modelo

### Para Imágenes

Edita `generate-images-ai.py`, línea ~60:

```python
# Cambiar de Flux Schnell a Flux Dev
payload = {
    "model": "blackboxai/black-forest-labs/flux-dev",  # Cambiar aquí
    "messages": [...]
}
```

### Para Parafraseado

Edita `paraphrase.py`, línea ~60:

```python
# Cambiar de GPT-4o a Claude
payload = {
    "model": "blackboxai/anthropic/claude-3.5-sonnet",  # Cambiar aquí
    "messages": [...]
}
```

## Estimación de Costos

### Modo Prueba (2 artículos, 5 variaciones)
- **Parafraseado**: 10 llamadas × ~$0.01 = **~$0.10**
- **Imágenes** (Flux Schnell): 10 imágenes × $0.003 = **$0.03**
- **Total**: **~$0.13**

### Modo Completo (5 artículos, 40 variaciones)
- **Parafraseado**: 200 llamadas × ~$0.01 = **~$2.00**
- **Imágenes** (Flux Schnell): 200 imágenes × $0.003 = **$0.60**
- **Total**: **~$2.60**

### Optimización de Costos

**Para reducir costos:**
1. Usar SDXL Lightning ($0.0014/imagen) en lugar de Flux Schnell
2. Usar GPT-3.5 Turbo para parafraseado
3. Reducir número de variaciones (ej: 20 en lugar de 40)

**Para máxima calidad:**
1. Usar Flux 1.1 Pro Ultra ($0.06/imagen)
2. Usar Claude 3.5 Sonnet para parafraseado
3. Aumentar temperatura para más creatividad

## Características de los Modelos Flux

### Flux Schnell (Default)
- ✅ Muy rápido (< 2 segundos)
- ✅ Económico ($0.003)
- ✅ Buena calidad para noticias
- ✅ Hasta 4 imágenes por request
- ⚠️ Menos detalles que Pro

### Flux Dev
- ✅ Balance calidad/precio
- ✅ Mejor para detalles
- ✅ Hasta 4 imágenes por request
- ⚠️ 8x más caro que Schnell

### Flux Pro / Ultra
- ✅ Máxima calidad
- ✅ Detalles fotorealistas
- ✅ Mejor comprensión de prompts
- ⚠️ Más lento
- ⚠️ Más costoso

## Documentación Oficial

- **Blackbox AI Docs**: https://docs.blackbox.ai
- **API Reference**: https://docs.blackbox.ai/api-reference/introduction
- **Image Models**: https://docs.blackbox.ai/api-reference/models/image-models
- **Pricing**: Consultar en el dashboard de Blackbox

## Notas Importantes

1. **Límites de Rate**: Blackbox puede tener límites de requests por minuto
2. **Timeouts**: Modelos más lentos pueden requerir timeouts mayores
3. **Prompts**: Flux entiende prompts en inglés mejor que en español
4. **Resolución**: Todos los modelos Flux soportan hasta 4K
5. **Batch**: Algunos modelos permiten generar múltiples imágenes por request

---

**Última actualización**: Enero 2026  
**Fuente**: Documentación oficial de Blackbox AI

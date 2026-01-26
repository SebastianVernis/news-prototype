# Arquitecturas de Despliegue - Sistema de Generación de Sitios

## 📋 Comparativa de Opciones

| Aspecto | Render + Vercel | Cloudflare Workers + Pages |
|---------|----------------|---------------------------|
| **Backend API** | Render Web Service | Cloudflare Workers |
| **Frontend Admin** | Vercel | Cloudflare Pages |
| **Sitios Generados** | Vercel (múltiples proyectos) | Cloudflare Pages (múltiples proyectos) |
| **Almacenamiento** | Render Disk / S3 | Cloudflare R2 |
| **Base de Datos** | Render PostgreSQL | Cloudflare D1 / Neon |
| **Costo Inicial** | Free tier generoso | Free tier ultragenero |
| **Escalabilidad** | Media-Alta | Muy Alta (edge) |
| **Latencia** | Buena | Excelente (global edge) |
| **Cold Start** | ~1-2s (Render free) | ~0ms (Workers) |
| **Límites CPU** | 512MB RAM free | 10ms CPU / request |
| **Complejidad** | Baja | Media |

## 🏗️ Opción 1: Render + Vercel

### Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIOS                                 │
└────────────┬─────────────────────┬──────────────────────────────┘
             │                     │
             │                     │
    ┌────────▼────────┐   ┌───────▼────────┐
    │   VERCEL (CDN)  │   │  VERCEL (CDN)  │
    │  Admin Frontend │   │ Sitio Generado │
    │   React/Vite    │   │   (estático)   │
    └────────┬────────┘   └────────────────┘
             │
             │ API Calls
             │
    ┌────────▼─────────────────────────────┐
    │    RENDER WEB SERVICE (Backend)      │
    │    - Flask API                       │
    │    - Master Orchestrator             │
    │    - Python Scripts                  │
    │    - Generación de contenido         │
    └────────┬─────────────────────────────┘
             │
             │
    ┌────────▼─────────────────────────────┐
    │  ALMACENAMIENTO                      │
    │  - Render Disk (temporal)            │
    │  - AWS S3 / R2 (permanente)          │
    │  - Sitios generados                  │
    │  - Imágenes, logos, CSS              │
    └──────────────────────────────────────┘
             │
             │ Deploy
             │
    ┌────────▼─────────────────────────────┐
    │  VERCEL (Deploy automático)          │
    │  - 1 proyecto por sitio generado     │
    │  - Deploy via API o Git              │
    └──────────────────────────────────────┘

SERVICIOS EXTERNOS:
┌─────────────────┐  ┌──────────────────┐  ┌──────────────┐
│  NewsAPI        │  │  Blackbox AI API │  │  Whois       │
│  (Noticias)     │  │  (IA contenido)  │  │  (Dominios)  │
└─────────────────┘  └──────────────────┘  └──────────────┘
```

### Componentes

#### 1. Backend en Render
- **Tipo**: Web Service (Python)
- **Plan**: Starter ($7/mes) o Free (con sleep)
- **Especificaciones**:
  - 512MB RAM (Free) / 2GB RAM (Starter)
  - Disk persistente (opcional, +$1/GB)
  - Auto-deploy desde GitHub
  - Variables de entorno seguras

#### 2. Admin Frontend en Vercel
- **Tipo**: Vercel Project
- **Plan**: Hobby (Free)
- **Características**:
  - React + Vite
  - Deploy automático desde Git
  - Edge network global
  - HTTPS automático

#### 3. Sitios Generados en Vercel
- **Tipo**: Múltiples Vercel Projects
- **Plan**: Hobby (Free, hasta 100 proyectos)
- **Deploy**:
  - Via Vercel API
  - 1 proyecto por sitio
  - Custom domains opcionales

#### 4. Almacenamiento
**Opción A: Render Disk**
- Pros: Integrado, simple
- Contras: No persistente en free tier, costoso

**Opción B: AWS S3**
- Pros: Barato, confiable, escalable
- Contras: Requiere configuración

**Opción C: Cloudflare R2**
- Pros: Sin costos de egress, barato
- Contras: Requiere cuenta Cloudflare

### Flujo de Despliegue

```
1. DESARROLLO
   ├── Push código a GitHub
   ├── Render auto-deploy backend
   └── Vercel auto-deploy frontend

2. GENERACIÓN DE SITIO
   ├── Usuario hace request desde frontend
   ├── Backend genera sitio completo
   ├── Sitio guardado en almacenamiento
   └── Backend devuelve URL del sitio

3. DESPLIEGUE DE SITIO
   Opción A: Manual
   ├── Usuario descarga ZIP del sitio
   └── Usuario sube a Vercel manualmente

   Opción B: Automático (vía API)
   ├── Backend crea nuevo proyecto Vercel vía API
   ├── Backend sube archivos del sitio
   └── Vercel devuelve URL pública
```

### Configuración

#### render.yaml (Backend)
```yaml
services:
  - type: web
    name: news-generator-backend
    env: python
    plan: starter
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn -w 2 -b 0.0.0.0:$PORT backend.app:app"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: BLACKBOX_API_KEY
        sync: false
      - key: VERCEL_TOKEN
        sync: false
      - key: AWS_ACCESS_KEY_ID
        sync: false
      - key: AWS_SECRET_ACCESS_KEY
        sync: false
    disk:
      name: data-disk
      mountPath: /opt/render/project/src/data
      sizeGB: 10
```

#### vercel.json (Frontend Admin)
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "framework": "vite",
  "env": {
    "VITE_API_URL": "https://news-generator-backend.onrender.com"
  }
}
```

#### vercel.json (Sitio Generado)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "**/*.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ]
}
```

---

## 🌐 Opción 2: Cloudflare Workers + Pages

### Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                    USUARIOS (GLOBAL)                             │
└────────────┬─────────────────────┬──────────────────────────────┘
             │                     │
             │ (Edge Network - 300+ locations)
             │                     │
    ┌────────▼─────────┐  ┌───────▼────────┐
    │ CLOUDFLARE PAGES │  │ CLOUDFLARE PAGES│
    │  Admin Frontend  │  │ Sitio Generado  │
    │   React/Vite     │  │   (estático)    │
    └────────┬─────────┘  └─────────────────┘
             │
             │ API Calls
             │
    ┌────────▼──────────────────────────────┐
    │   CLOUDFLARE WORKERS (Backend API)    │
    │   - Serverless Functions (Edge)       │
    │   - TypeScript/JavaScript             │
    │   - Hono/Express-like framework       │
    │   - 0ms cold start                    │
    └────────┬──────────────────────────────┘
             │
             ├─────────┬──────────┬──────────┐
             │         │          │          │
    ┌────────▼──┐ ┌───▼───┐ ┌────▼────┐ ┌──▼──────┐
    │ R2 Bucket│ │  D1   │ │  Queue  │ │  Durable│
    │(Storage) │ │  (DB) │ │  (Jobs) │ │ Objects │
    └──────────┘ └───────┘ └─────────┘ └─────────┘

SERVICIOS EXTERNOS:
┌─────────────────┐  ┌──────────────────┐
│  NewsAPI        │  │  Blackbox AI API │
│  (Noticias)     │  │  (IA contenido)  │
└─────────────────┘  └──────────────────┘
```

### Componentes

#### 1. Backend en Cloudflare Workers
- **Tipo**: Serverless Functions (Edge)
- **Plan**: Paid ($5/mes, 10M requests)
- **Características**:
  - JavaScript/TypeScript
  - 0ms cold start
  - 10ms CPU time / request
  - 128MB memoria
  - Deploy global instantáneo

#### 2. Admin Frontend en Cloudflare Pages
- **Tipo**: Static Site Hosting
- **Plan**: Free (unlimited)
- **Características**:
  - React + Vite build
  - Edge network global
  - Deploy automático desde Git
  - HTTPS automático

#### 3. Sitios Generados en Cloudflare Pages
- **Tipo**: Múltiples Pages Projects
- **Plan**: Free (unlimited proyectos)
- **Deploy**: Via Wrangler CLI o API

#### 4. Almacenamiento R2
- **Tipo**: Object Storage (S3-compatible)
- **Plan**: $0.015/GB almacenado
- **Ventajas**:
  - $0 egress (sin costo de transferencia)
  - API compatible con S3
  - Integración directa con Workers

#### 5. Base de Datos D1
- **Tipo**: SQLite serverless
- **Plan**: Free tier generoso
- **Uso**: Metadata de sitios, tracking

#### 6. Queues (Opcional)
- **Tipo**: Message Queue
- **Uso**: Procesar generación de sitios asíncronamente

### Flujo de Despliegue

```
1. DESARROLLO
   ├── Push código a GitHub
   ├── Pages auto-deploy frontend
   └── Wrangler auto-deploy Workers

2. GENERACIÓN DE SITIO (Asíncrono)
   ├── Usuario hace request desde frontend
   ├── Worker recibe request, crea job en Queue
   ├── Worker responde con job_id inmediatamente
   ├── Consumer Worker procesa job:
   │   ├── Descarga noticias
   │   ├── Genera contenido con IA
   │   ├── Genera imágenes
   │   ├── Crea HTML/CSS
   │   └── Sube a R2
   └── Frontend hace polling de status

3. DESPLIEGUE DE SITIO
   ├── Worker finaliza generación
   ├── Worker crea nuevo Pages project vía API
   ├── Worker sube archivos desde R2 a Pages
   └── Worker actualiza DB con URL pública
```

### Configuración

#### wrangler.toml (Workers Backend)
```toml
name = "news-generator-api"
main = "src/index.ts"
compatibility_date = "2024-01-01"

# Workers AI (opcional, para IA nativa)
[ai]
binding = "AI"

# R2 Storage
[[r2_buckets]]
binding = "SITES_BUCKET"
bucket_name = "generated-sites"
preview_bucket_name = "generated-sites-dev"

# D1 Database
[[d1_databases]]
binding = "DB"
database_name = "news-generator-db"
database_id = "xxx"

# Queue para procesamiento asíncrono
[[queues.producers]]
binding = "SITE_GENERATION_QUEUE"
queue = "site-generation-jobs"

[[queues.consumers]]
queue = "site-generation-jobs"
max_batch_size = 10
max_batch_timeout = 30

# Variables de entorno
[vars]
ENVIRONMENT = "production"

# Secrets (via wrangler secret put)
# BLACKBOX_API_KEY
# NEWSAPI_KEY
# CLOUDFLARE_API_TOKEN
```

#### wrangler.toml (Frontend Pages)
```toml
name = "news-generator-admin"
pages_build_output_dir = "dist"

[build]
command = "npm run build"

[env.production.vars]
VITE_API_URL = "https://news-generator-api.workers.dev"
```

#### package.json (Workers)
```json
{
  "name": "news-generator-workers",
  "scripts": {
    "dev": "wrangler dev",
    "deploy": "wrangler deploy",
    "tail": "wrangler tail"
  },
  "dependencies": {
    "hono": "^4.0.0",
    "@hono/zod-validator": "^0.2.0"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "^4.0.0",
    "wrangler": "^3.0.0"
  }
}
```

### Limitaciones y Soluciones

#### Problema: CPU Time Limit (10ms)
**Solución**: Procesar en background con Queues
```typescript
// Endpoint recibe request
app.post('/api/sites/generate', async (c) => {
  const jobId = crypto.randomUUID();
  
  // Encolar job
  await c.env.SITE_GENERATION_QUEUE.send({
    jobId,
    params: await c.req.json()
  });
  
  // Responder inmediatamente
  return c.json({ jobId, status: 'queued' });
});

// Consumer procesa job (sin límite de tiempo)
async function handleQueue(batch, env) {
  for (const message of batch.messages) {
    const { jobId, params } = message.body;
    await generateSiteComplete(jobId, params, env);
  }
}
```

#### Problema: No Python en Workers
**Solución 1**: Reescribir lógica en TypeScript
**Solución 2**: Llamar APIs externas para IA (Blackbox API ya es externa)
**Solución 3**: Usar Workers AI nativo de Cloudflare

```typescript
// Ejemplo con Workers AI
const response = await env.AI.run('@cf/meta/llama-2-7b-chat-int8', {
  prompt: "Parafrasea este artículo..."
});
```

---

## 🎯 Recomendación Final

### Para MVP / Desarrollo Rápido: **Render + Vercel**
**Ventajas:**
- ✅ Usa código Python existente sin cambios
- ✅ Setup en < 30 minutos
- ✅ Free tier funcional
- ✅ Deploy automático
- ✅ Debugging más fácil

**Desventajas:**
- ❌ Cold start en free tier de Render
- ❌ Menos escalable
- ❌ Costos crecen linealmente

### Para Producción / Escala: **Cloudflare Workers + Pages**
**Ventajas:**
- ✅ Latencia ultra-baja (edge global)
- ✅ No cold start
- ✅ Escalabilidad ilimitada
- ✅ Costos predecibles y bajos
- ✅ Egress gratis (R2)

**Desventajas:**
- ❌ Requiere reescribir backend en TypeScript
- ❌ Límites de CPU (10ms / request)
- ❌ Curva de aprendizaje mayor
- ❌ Debugging más complejo

---

## 📊 Estimación de Costos (Mensual)

### Render + Vercel
```
Render Web Service (Starter):    $7/mes
Render Disk (10GB):               $1/mes
AWS S3 (100GB + requests):        ~$3/mes
Vercel (Hobby):                   $0/mes
TOTAL:                            ~$11/mes
```

### Cloudflare Workers + Pages
```
Workers (Paid, 10M requests):     $5/mes
R2 Storage (100GB):               $1.50/mes
D1 Database (free tier):          $0/mes
Pages (unlimited):                $0/mes
TOTAL:                            ~$6.50/mes
```

---

## 🚀 Próximos Pasos

1. **Decidir arquitectura** según prioridades
2. **Crear configuraciones** de deployment
3. **Implementar scripts** de deploy automatizado
4. **Documentar proceso** de deployment
5. **Probar** en staging environment

¿Deseas que implemente una de estas arquitecturas específicamente?

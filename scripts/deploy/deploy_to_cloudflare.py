#!/usr/bin/env python3
"""
Deploy all sites to Cloudflare Pages
Generates deployment commands and instructions
"""

import os
import subprocess

# Get the root directory (project root, not scripts/deploy)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../../'))
SITES_DIR = os.path.join(ROOT_DIR, 'sites')
PROJECT_PREFIX = 'news-site'

# List of sites
SITES = [
    'radiocinconoticias',
    'centralmexico',
    'tvmexico',
    'cbnnoticias',
    'mexicoinformado',
    'nodoinformativo',
    'bitacoraurbana',
    'reportecentralmx',
    'verticenoticias',
    'noticiasobjetivo'
]

def check_wrangler():
    """Check if wrangler is installed and logged in"""
    try:
        result = subprocess.run(['wrangler', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ wrangler CLI instalado: {result.stdout.strip()}")
            return True
        else:
            print("❌ wrangler CLI no está instalado")
            print("   Instala con: npm install -g wrangler")
            return False
    except FileNotFoundError:
        print("❌ wrangler CLI no encontrado")
        print("   Instala con: npm install -g wrangler")
        return False

def check_login():
    """Check if logged in to Cloudflare"""
    try:
        result = subprocess.run(['wrangler', 'whoami'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Sesión activa: {result.stdout.strip()}")
            return True
        else:
            print("❌ No has iniciado sesión en Cloudflare")
            print("   Ejecuta: wrangler login")
            return False
    except:
        return False

def deploy_site(site):
    """Deploy a single site to Cloudflare Pages"""
    site_path = os.path.join(SITES_DIR, site)
    project_name = f"{PROJECT_PREFIX}-{site}"
    
    if not os.path.exists(site_path):
        print(f"❌ Directorio no encontrado: {site_path}")
        return False
    
    print(f"\n📍 Desplegando: {site}")
    print(f"   Project: {project_name}")
    print(f"   Path: {site_path}")
    
    try:
        result = subprocess.run([
            'wrangler', 'pages', 'deploy', site_path,
            '--project-name', project_name,
            '--branch', 'main',
            '--commit-dirty=true'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {site} desplegado exitosamente")
            print(f"   URL: https://{project_name}.pages.dev")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Timeout en el despliegue")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def generate_deployment_guide():
    """Generate a deployment guide markdown file"""
    guide = """# Guía de Despliegue - Cloudflare News Project

## Requisitos Previos

1. **Tener cuenta en Cloudflare** (gratuita)
2. **Instalar wrangler CLI**:
   ```bash
   npm install -g wrangler
   ```

3. **Iniciar sesión**:
   ```bash
   wrangler login
   ```

## Despliegue Automático

Ejecuta el script de despliegue:

```bash
chmod +x deploy_all_sites.sh
./deploy_all_sites.sh
```

## Despliegue Manual (Sitio por Sitio)

### 1. Radio Cinco Noticias
```bash
wrangler pages deploy ./sites/radiocinconoticias --project-name=news-site-radiocinconoticias
```
URL: https://news-site-radiocinconoticias.pages.dev

### 2. Central México
```bash
wrangler pages deploy ./sites/centralmexico --project-name=news-site-centralmexico
```
URL: https://news-site-centralmexico.pages.dev

### 3. TV México
```bash
wrangler pages deploy ./sites/tvmexico --project-name=news-site-tvmexico
```
URL: https://news-site-tvmexico.pages.dev

### 4. CBN Noticias
```bash
wrangler pages deploy ./sites/cbnnoticias --project-name=news-site-cbnnoticias
```
URL: https://news-site-cbnnoticias.pages.dev

### 5. México Informado
```bash
wrangler pages deploy ./sites/mexicoinformado --project-name=news-site-mexicoinformado
```
URL: https://news-site-mexicoinformado.pages.dev

### 6. Nodo Informativo
```bash
wrangler pages deploy ./sites/nodoinformativo --project-name=news-site-nodoinformativo
```
URL: https://news-site-nodoinformativo.pages.dev

### 7. Bitácora Urbana
```bash
wrangler pages deploy ./sites/bitacoraurbana --project-name=news-site-bitacoraurbana
```
URL: https://news-site-bitacoraurbana.pages.dev

### 8. Reporte Central MX
```bash
wrangler pages deploy ./sites/reportecentralmx --project-name=news-site-reportecentralmx
```
URL: https://news-site-reportecentralmx.pages.dev

### 9. Vértice Noticias
```bash
wrangler pages deploy ./sites/verticenoticias --project-name=news-site-verticenoticias
```
URL: https://news-site-verticenoticias.pages.dev

### 10. Noticias Objetivo
```bash
wrangler pages deploy ./sites/noticiasobjetivo --project-name=news-site-noticiasobjetivo
```
URL: https://news-site-noticiasobjetivo.pages.dev

## Configuración de Dominio Personalizado

1. Ve al dashboard de Cloudflare Pages
2. Selecciona el proyecto
3. Click en "Custom domains"
4. Agrega tu dominio

## Variables de Entorno (Opcional)

Si necesitas variables de entorno:

1. Ve al dashboard del proyecto en Cloudflare
2. Selecciona "Settings" > "Environment variables"
3. Agrega las variables necesarias

## Actualizaciones

Para actualizar un sitio después de hacer cambios:

```bash
wrangler pages deploy ./sites/[nombre-sitio] --project-name=news-site-[nombre-sitio]
```

## Monitoreo

- **Deployments**: https://dash.cloudflare.com/?to=/:account/pages
- **Analytics**: Dashboard de cada proyecto

---

**Generado:** $(date +%Y-%m-%d)
**Total de sitios:** 10
"""
    
    with open('DEPLOYMENT_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("\n✅ Guía de despliegue generada: DEPLOYMENT_GUIDE.md")

def main():
    print("==============================================")
    print("   Cloudflare Pages Deployment")
    print("==============================================")
    print()
    
    # Check prerequisites
    if not check_wrangler():
        print("\n⚠️  No se puede continuar sin wrangler CLI")
        print("   Se generará una guía de despliegue manual")
        generate_deployment_guide()
        return
    
    print()
    
    if not check_login():
        print("\n⚠️  Necesitas iniciar sesión primero")
        print("   Ejecuta: wrangler login")
        generate_deployment_guide()
        return
    
    print()
    print(f"📦 Sitios a desplegar: {len(SITES)}")
    print()
    
    # Deploy each site
    deployed = 0
    failed = 0
    
    for site in SITES:
        if deploy_site(site):
            deployed += 1
        else:
            failed += 1
    
    # Summary
    print()
    print("==============================================")
    print("   Resumen del Despliegue")
    print("==============================================")
    print(f"✅ Exitosos: {deployed}")
    print(f"❌ Fallidos: {failed}")
    print()
    
    if deployed > 0:
        print("📋 URLs de los sitios:")
        for site in SITES:
            print(f"   https://{PROJECT_PREFIX}-{site}.pages.dev")
    
    print()
    print("==============================================")
    
    # Generate guide
    generate_deployment_guide()

if __name__ == '__main__':
    main()

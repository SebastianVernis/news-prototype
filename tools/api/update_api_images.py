#!/usr/bin/env python3
"""
Script para actualizar las URLs de imágenes en las funciones de API
Reemplaza las URLs de placeholder con las imágenes almacenadas en R2
"""

import json
import re
from pathlib import Path

def update_api_functions_with_r2_images():
    """Actualizar las funciones de API con imágenes de R2"""
    
    # Definir mapeo de imágenes de ejemplo (esto vendría del sistema R2)
    r2_image_mapping = {
        "Plan+Económico": "https://news-images.YOURACCOUNT.r2.cloudflarestorage.com/news-images/20260216_economy_plan.jpg",
        "Banxico": "https://news-images.YOURACCOUNT.r2.cloudflarestorage.com/news-images/20260216_banxico_interest.jpg",
        "Mariposa+Nueva": "https://news-images.YOURACCOUNT.r2.cloudflarestorage.com/news-images/20260216_butterfly_discovery.jpg",
        "Solar+Flotante": "https://news-images.YOURACCOUNT.r2.cloudflarestorage.com/news-images/20260216_solar_plant.jpg",
        "Oro+Matemáticas": "https://news-images.YOURACCOUNT.r2.cloudflarestorage.com/news-images/20260216_math_gold.jpg",
        "Vacuna+TBC": "https://news-images.YOURACCOUNT.r2.cloudflarestorage.com/news-images/20260216_vaccine_trial.jpg",
        "Tumba+Maya": "https://news-images.YOURACCOUNT.r2.cloudflarestorage.com/news-images/20260216_maya_tomb.jpg",
        "Corredor+Turístico": "https://news-images.YOURACCOUNT.r2.cloudflarestorage.com/news-images/20260216_tourism_corridor.jpg",
        "Robot+Playa": "https://news-images.YOURACCOUNT.r2.cloudflarestorage.com/news-images/20260216_beach_robot.jpg",
        "Bioplástico": "https://news-images.YOURACCOUNT.r2.cloudflarestorage.com/news-images/20260216_bioplastic.jpg",
        "Marte+Alimentos": "https://news-images.YOURACCOUNT.r2.cloudflarestorage.com/news-images/20260216_mars_food.jpg"
    }
    
    # Ruta del archivo de función de API
    repo_root = Path(__file__).resolve().parents[2]
    api_file_path = str(repo_root / "functions" / "api" / "articles" / "index.js")
    
    # Leer el archivo actual
    with open(api_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar las URLs de placeholder con URLs de R2
    updated_content = content
    for placeholder_text, r2_url in r2_image_mapping.items():
        placeholder_url = f"https://placehold.co/800x450/"
        # Buscar y reemplazar la URL específica
        pattern = rf'("{placeholder_url}[^"]*\?text={placeholder_text}")'
        updated_content = re.sub(pattern, f'"{r2_url}"', updated_content)
    
    # Guardar el archivo actualizado
    backup_path = api_file_path + ".backup"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)  # Guardar copia de seguridad
    
    with open(api_file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ API functions actualizadas con imágenes de R2")
    print(f"📄 Backup guardado en: {backup_path}")
    
    # Actualizar también el archivo de artículo individual
    update_individual_article_function(r2_image_mapping)

def update_individual_article_function(r2_image_mapping):
    """Actualizar la función de artículo individual con imágenes de R2"""
    
    article_file_path = str(repo_root / "functions" / "api" / "articles" / "[slug].js")
    
    try:
        with open(article_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Similar update for individual article function
        updated_content = content
        for placeholder_text, r2_url in r2_image_mapping.items():
            placeholder_url = f"https://placehold.co/800x450/"
            pattern = rf'("{placeholder_url}[^"]*\?text={placeholder_text}")'
            updated_content = re.sub(pattern, f'"{r2_url}"', updated_content)
        
        # Guardar archivo actualizado
        backup_path = article_file_path + ".backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        with open(article_file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Función de artículo individual actualizada con imágenes de R2")
        print(f"📄 Backup guardado en: {backup_path}")
        
    except FileNotFoundError:
        print(f"⚠️  Archivo no encontrado: {article_file_path} (posiblemente ya renombrado o movido)")

def create_image_upload_workflow():
    """Crear un workflow para subir imágenes y actualizar la API"""
    
    workflow_content = '''# Workflow para gestión de imágenes de noticias
# Este workflow se ejecutaría cuando se generan nuevas imágenes

name: Upload Images to R2 and Update API
on:
  workflow_dispatch:
    inputs:
      article_slug:
        description: 'Slug del artículo'
        required: true
        default: 'nuevo-articulo'
      image_path:
        description: 'Ruta de la imagen local'
        required: true
        default: './images/nuevo-articulo.jpg'

jobs:
  upload-and-update:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install boto3 requests python-dotenv
      
      - name: Configure AWS Credentials for R2
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.R2_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.R2_SECRET_ACCESS_KEY }}
          aws-region: auto
          endpoint-url: https://${{ secrets.CF_ACCOUNT_ID }}.r2.cloudflarestorage.com
      
      - name: Upload image to R2
        run: |
          python scripts/upload_to_r2.py "${{ inputs.image_path }}" "${{ inputs.article_slug }}"
      
      - name: Update API with new image URL
        run: |
          python scripts/update_api_image.py "${{ inputs.article_slug }}" "${{ secrets.API_UPDATE_TOKEN }}"
'''
    
    workflow_path = str(repo_root / ".github" / "workflows" / "upload-images.yml")
    workflow_dir = Path(workflow_path).parent
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    with open(workflow_path, 'w', encoding='utf-8') as f:
        f.write(workflow_content)
    
    print(f"✅ Workflow de carga de imágenes creado en: {workflow_path}")

def main():
    """Función principal"""
    print("🔄 Actualizando funciones de API con imágenes de R2...")
    print("="*60)
    
    # Actualizar funciones de API con imágenes de R2
    update_api_functions_with_r2_images()
    
    # Crear workflow de automatización
    create_image_upload_workflow()
    
    print("="*60)
    print("✅ Proceso de actualización de imágenes completado")
    print("📋 Próximos pasos:")
    print("   1. Configurar credenciales de R2 en variables de entorno")
    print("   2. Subir imágenes reales a R2")
    print("   3. Actualizar las URLs en las funciones de API")
    print("   4. Desplegar las funciones actualizadas")

if __name__ == "__main__":
    main()

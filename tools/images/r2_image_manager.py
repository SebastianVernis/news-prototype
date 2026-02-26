#!/usr/bin/env python3
"""
Sistema de Gestión de Imágenes para Sitios de Noticias
Sube imágenes a R2 y actualiza las rutas en la API
"""

import os
import boto3
import requests
from pathlib import Path
from datetime import datetime
import mimetypes
from botocore.exceptions import ClientError
import json

class R2ImageManager:
    """Manejador de imágenes para R2 Cloudflare"""
    
    def __init__(self):
        # Cargar variables de entorno
        self.account_id = os.getenv('CF_ACCOUNT_ID')
        self.access_key_id = os.getenv('R2_ACCESS_KEY_ID')
        self.secret_access_key = os.getenv('R2_SECRET_ACCESS_KEY')
        self.bucket_name = os.getenv('R2_BUCKET_NAME', 'news-images')
        
        # Endpoint de R2
        self.endpoint_url = f"https://{self.account_id}.r2.cloudflarestorage.com"
        
        # Inicializar cliente S3 para R2
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key
        )
        
        # Directorio de imágenes
        repo_root = Path(__file__).resolve().parents[2]
        self.images_dir = Path(os.getenv("NEWS_IMAGES_DIR", repo_root / "generated_images"))
        
    def upload_image_to_r2(self, image_path, object_name=None):
        """Sube una imagen a R2 y devuelve la URL pública"""
        if not object_name:
            # Generar nombre único para la imagen
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = Path(image_path).name
            object_name = f"news-images/{timestamp}_{filename}"
        
        # Detectar tipo MIME
        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        
        try:
            # Subir archivo a R2
            self.s3_client.upload_file(
                image_path,
                self.bucket_name,
                object_name,
                ExtraArgs={'ContentType': mime_type}
            )
            
            # Generar URL pública
            public_url = f"https://{self.bucket_name}.{self.account_id}.r2.cloudflarestorage.com/{object_name}"
            return public_url
            
        except ClientError as e:
            print(f"❌ Error subiendo imagen a R2: {e}")
            return None
    
    def upload_generated_images(self):
        """Sube todas las imágenes generadas a R2"""
        if not self.images_dir.exists():
            print(f"⚠️  Directorio de imágenes no encontrado: {self.images_dir}")
            return []
        
        uploaded_images = []
        
        # Recorrer todas las imágenes en el directorio
        for image_file in self.images_dir.rglob("*"):
            if image_file.is_file() and image_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
                print(f"📤 Subiendo imagen: {image_file.name}")
                
                # Subir imagen a R2
                public_url = self.upload_image_to_r2(str(image_file))
                
                if public_url:
                    uploaded_images.append({
                        'local_path': str(image_file),
                        'r2_url': public_url,
                        'uploaded_at': datetime.now().isoformat()
                    })
                    print(f"✅ Subido: {public_url}")
                else:
                    print(f"❌ Fallo al subir: {image_file.name}")
        
        return uploaded_images

class APIUpdater:
    """Actualiza las rutas de imágenes en la API"""
    
    def __init__(self, api_base_url="https://noticias-hoy.pages.dev/api"):
        self.api_base_url = api_base_url
        
    def update_article_images(self, article_id, new_image_url):
        """Actualiza la URL de imagen de un artículo"""
        try:
            # Este sería el endpoint para actualizar un artículo
            # En la implementación real, necesitarías un endpoint de actualización
            update_data = {
                'imageUrl': new_image_url
            }
            
            # headers con token de autenticación
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {os.getenv("ADMIN_TOKEN")}'  # Asumiendo token de admin
            }
            
            # Realizar la solicitud de actualización
            response = requests.patch(
                f"{self.api_base_url}/articles/{article_id}",
                json=update_data,
                headers=headers
            )
            
            if response.status_code == 200:
                print(f"✅ Artículo {article_id} actualizado con nueva imagen")
                return True
            else:
                print(f"❌ Error actualizando artículo {article_id}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error en la actualización de artículo: {e}")
            return False

def main():
    """Función principal para gestionar imágenes"""
    print("🖼️  Sistema de Gestión de Imágenes para Sitios de Noticias")
    print("="*60)
    
    # Inicializar gestor de R2
    try:
        r2_manager = R2ImageManager()
        print(f"✅ Conectado a R2 bucket: {r2_manager.bucket_name}")
    except Exception as e:
        print(f"❌ Error inicializando R2: {e}")
        print("⚠️  Asegúrate de tener las variables de entorno configuradas:")
        print("   - CF_ACCOUNT_ID")
        print("   - R2_ACCESS_KEY_ID") 
        print("   - R2_SECRET_ACCESS_KEY")
        print("   - R2_BUCKET_NAME")
        return
    
    # Subir imágenes generadas a R2
    print("\n📤 Subiendo imágenes a R2...")
    uploaded_images = r2_manager.upload_generated_images()
    
    print(f"\n📊 Resultado: {len(uploaded_images)} imágenes subidas a R2")
    
    # Guardar mapeo de imágenes subidas
    mapping_file = "/tmp/image_mapping.json"
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(uploaded_images, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Mapeo de imágenes guardado en: {mapping_file}")
    
    # Actualizar API con nuevas rutas de imágenes
    print("\n🔄 Actualizando rutas en la API...")
    
    # Aquí iría la lógica para actualizar las rutas de imágenes en la API
    # Esto dependería de cómo se almacenan los artículos en tu backend
    api_updater = APIUpdater()
    
    print("✅ Proceso de gestión de imágenes completado")
    
    # Mostrar resumen
    print(f"\n📋 RESUMEN:")
    print(f"   • Imágenes subidas a R2: {len(uploaded_images)}")
    print(f"   • Mapeo guardado en: {mapping_file}")
    print(f"   • Rutas de API actualizadas: Pendiente de implementación específica")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script para deployar sitios generados a Vercel automáticamente
Usa la API de Vercel para crear proyectos y subir archivos
"""

import os
import json
import requests
import time
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv
import base64

load_dotenv()

VERCEL_TOKEN = os.getenv('VERCEL_TOKEN')
VERCEL_API_URL = 'https://api.vercel.com'
VERCEL_TEAM_ID = os.getenv('VERCEL_TEAM_ID')  # Opcional, para teams


class VercelDeployer:
    """Deployer para sitios generados en Vercel"""
    
    def __init__(self, token: str = None, team_id: str = None):
        self.token = token or VERCEL_TOKEN
        if not self.token:
            raise ValueError("VERCEL_TOKEN no encontrado")
        
        self.team_id = team_id or VERCEL_TEAM_ID
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        if self.team_id:
            self.base_url = f"{VERCEL_API_URL}/v9/projects?teamId={self.team_id}"
        else:
            self.base_url = f"{VERCEL_API_URL}/v9/projects"
    
    def crear_proyecto(self, nombre: str, framework: str = 'other') -> Dict:
        """
        Crea un nuevo proyecto en Vercel
        
        Args:
            nombre: Nombre del proyecto (debe ser único)
            framework: Framework usado (other, nextjs, vite, etc.)
            
        Returns:
            Información del proyecto creado
        """
        data = {
            'name': nombre,
            'framework': framework,
            'publicSource': False
        }
        
        response = requests.post(
            self.base_url,
            headers=self.headers,
            json=data
        )
        
        if response.status_code == 201:
            return response.json()
        elif response.status_code == 409:
            # Proyecto ya existe
            print(f"⚠️  Proyecto '{nombre}' ya existe")
            return self.obtener_proyecto(nombre)
        else:
            raise Exception(f"Error creando proyecto: {response.text}")
    
    def obtener_proyecto(self, nombre: str) -> Optional[Dict]:
        """Obtiene información de un proyecto existente"""
        url = f"{self.base_url}/{nombre}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def crear_deployment(self, project_name: str, site_dir: Path) -> Dict:
        """
        Crea un deployment de un sitio en Vercel
        
        Args:
            project_name: Nombre del proyecto en Vercel
            site_dir: Directorio del sitio a deployar
            
        Returns:
            Información del deployment
        """
        # Leer archivos del sitio
        files = self._preparar_archivos(site_dir)
        
        if not files:
            raise Exception(f"No hay archivos para deployar en {site_dir}")
        
        # Crear deployment
        deployment_data = {
            'name': project_name,
            'files': files,
            'projectSettings': {
                'framework': 'other'
            },
            'target': 'production'
        }
        
        url = f"{VERCEL_API_URL}/v13/deployments"
        if self.team_id:
            url += f"?teamId={self.team_id}"
        
        response = requests.post(
            url,
            headers=self.headers,
            json=deployment_data
        )
        
        if response.status_code not in [200, 201]:
            raise Exception(f"Error en deployment: {response.text}")
        
        deployment = response.json()
        
        # Esperar a que el deployment esté listo
        deployment_url = self._esperar_deployment(deployment['id'])
        
        return {
            'id': deployment['id'],
            'url': deployment_url,
            'status': 'ready'
        }
    
    def _preparar_archivos(self, site_dir: Path) -> List[Dict]:
        """Prepara archivos para el deployment"""
        files = []
        
        # Obtener todos los archivos
        for file_path in site_dir.rglob('*'):
            if file_path.is_file():
                # Ruta relativa
                rel_path = str(file_path.relative_to(site_dir))
                
                # Leer contenido
                if file_path.suffix in ['.html', '.css', '.js', '.json', '.txt']:
                    # Archivos de texto
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    encoding = 'utf-8'
                else:
                    # Archivos binarios (imágenes)
                    with open(file_path, 'rb') as f:
                        content = base64.b64encode(f.read()).decode('utf-8')
                    encoding = 'base64'
                
                files.append({
                    'file': rel_path,
                    'data': content,
                    'encoding': encoding
                })
        
        return files
    
    def _esperar_deployment(self, deployment_id: str, timeout: int = 300) -> str:
        """Espera a que el deployment esté listo"""
        url = f"{VERCEL_API_URL}/v13/deployments/{deployment_id}"
        if self.team_id:
            url += f"?teamId={self.team_id}"
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            response = requests.get(url, headers=self.headers)
            
            if response.status_code != 200:
                raise Exception(f"Error obteniendo estado: {response.text}")
            
            deployment = response.json()
            state = deployment.get('readyState')
            
            if state == 'READY':
                return f"https://{deployment['url']}"
            elif state == 'ERROR':
                raise Exception(f"Deployment falló: {deployment.get('error')}")
            
            time.sleep(5)
        
        raise Exception(f"Timeout esperando deployment {deployment_id}")
    
    def deployar_sitio_completo(self, site_dir: Path, site_name: str = None) -> Dict:
        """
        Deploya un sitio completo a Vercel
        
        Args:
            site_dir: Directorio del sitio
            site_name: Nombre del sitio (opcional, usa nombre del directorio)
            
        Returns:
            Información del deployment
        """
        if not site_dir.exists():
            raise Exception(f"Directorio no existe: {site_dir}")
        
        # Generar nombre del proyecto
        if not site_name:
            site_name = site_dir.name
        
        # Sanitizar nombre (Vercel solo permite lowercase, números, guiones)
        project_name = site_name.lower().replace('_', '-').replace(' ', '-')
        project_name = ''.join(c for c in project_name if c.isalnum() or c == '-')
        
        print(f"📦 Deployando sitio: {site_name}")
        print(f"   Proyecto Vercel: {project_name}")
        
        # Crear proyecto si no existe
        try:
            proyecto = self.crear_proyecto(project_name)
            print(f"✅ Proyecto creado/encontrado")
        except Exception as e:
            print(f"❌ Error creando proyecto: {e}")
            raise
        
        # Crear deployment
        try:
            deployment = self.crear_deployment(project_name, site_dir)
            print(f"✅ Deployment completado")
            print(f"🌐 URL: {deployment['url']}")
            return deployment
        except Exception as e:
            print(f"❌ Error en deployment: {e}")
            raise


def main():
    """Función principal para pruebas"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Deploy sitio a Vercel")
    parser.add_argument('site_dir', type=str, help='Directorio del sitio')
    parser.add_argument('--name', type=str, help='Nombre del proyecto')
    
    args = parser.parse_args()
    
    deployer = VercelDeployer()
    site_dir = Path(args.site_dir)
    
    try:
        resultado = deployer.deployar_sitio_completo(site_dir, args.name)
        print("\n✅ Deployment exitoso!")
        print(f"URL: {resultado['url']}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

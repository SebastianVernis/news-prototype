#!/usr/bin/env python3
"""
Protocolo de Pre-Creación de Sitios de Noticias
Gestiona el proceso completo de preparación antes de crear sitios:
- Generación de nombres convincentes
- Verificación de disponibilidad de dominios
- Creación de metadatos JSON para site-builder
"""

import json
import os
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

from site_name_generator import SiteNameGenerator
from domain_verifier import DomainVerifier


class SitePreCreation:
    """Gestiona el protocolo de pre-creación de sitios"""
    
    def __init__(self, output_dir: str = "../data/sites_metadata"):
        """
        Inicializa el protocolo
        
        Args:
            output_dir: Directorio para guardar metadatos
        """
        self.output_dir = output_dir
        self.name_generator = SiteNameGenerator()
        self.domain_verifier = DomainVerifier(rate_limit_delay=2.0)
        
        # Crear directorio si no existe
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    def generar_colores_marca(self) -> Dict[str, str]:
        """
        Genera paleta de colores para la marca
        
        Returns:
            dict: Colores en formato hex
        """
        # Paletas predefinidas apropiadas para sitios de noticias
        paletas = [
            # Profesional azul
            {
                "primario": "#2C3E50",
                "secundario": "#3498DB",
                "acento": "#E74C3C",
                "texto": "#2C3E50",
                "fondo": "#ECF0F1"
            },
            # Clásico negro-rojo
            {
                "primario": "#1A1A1A",
                "secundario": "#C0392B",
                "acento": "#E67E22",
                "texto": "#2C3E50",
                "fondo": "#FFFFFF"
            },
            # Moderno verde
            {
                "primario": "#27AE60",
                "secundario": "#16A085",
                "acento": "#F39C12",
                "texto": "#2C3E50",
                "fondo": "#ECF0F1"
            },
            # Elegante púrpura
            {
                "primario": "#8E44AD",
                "secundario": "#9B59B6",
                "acento": "#E74C3C",
                "texto": "#2C3E50",
                "fondo": "#F8F9FA"
            },
            # Corporativo azul oscuro
            {
                "primario": "#34495E",
                "secundario": "#2980B9",
                "acento": "#E67E22",
                "texto": "#2C3E50",
                "fondo": "#ECF0F1"
            },
            # Minimalista gris
            {
                "primario": "#4A4A4A",
                "secundario": "#7F8C8D",
                "acento": "#E74C3C",
                "texto": "#2C3E50",
                "fondo": "#FFFFFF"
            }
        ]
        
        return random.choice(paletas)
    
    def generar_metadata_logo(self, nombre: str, colores: Dict[str, str]) -> Dict[str, any]:
        """
        Genera metadatos para la creación del logo
        
        Args:
            nombre: Nombre del sitio
            colores: Paleta de colores
            
        Returns:
            dict: Metadatos del logo
        """
        # Extraer iniciales del nombre
        palabras = nombre.split()
        iniciales = "".join([p[0].upper() for p in palabras[:3]])
        
        # Estilos de logo
        estilos = [
            "minimal",          # Minimalista
            "modern",           # Moderno
            "classic",          # Clásico
            "bold",             # Audaz
            "elegant",          # Elegante
            "tech"              # Tecnológico
        ]
        
        # Tipos de logo
        tipos = [
            "wordmark",         # Solo texto
            "lettermark",       # Iniciales
            "combination",      # Texto + símbolo
            "emblem"            # Emblema
        ]
        
        return {
            "nombre_completo": nombre,
            "iniciales": iniciales,
            "estilo": random.choice(estilos),
            "tipo": random.choice(tipos),
            "colores": colores,
            "fuente_sugerida": random.choice([
                "Montserrat",
                "Roboto",
                "Open Sans",
                "Lato",
                "Merriweather",
                "Playfair Display",
                "Source Sans Pro"
            ]),
            "peso_fuente": random.choice(["regular", "medium", "bold", "black"]),
            "formato_salida": ["png", "svg"],
            "dimensiones": {
                "logo_principal": "500x200",
                "favicon": "64x64",
                "social": "1200x630"
            }
        }
    
    def generar_categorias_noticias(self) -> List[str]:
        """
        Genera categorías de noticias para el sitio
        
        Returns:
            list: Lista de categorías
        """
        categorias_base = ["Inicio", "Nacional", "Internacional", "Política"]
        
        categorias_adicionales = [
            "Economía", "Tecnología", "Deportes", "Entretenimiento",
            "Cultura", "Ciencia", "Salud", "Educación",
            "Opinión", "Sociedad", "Negocios", "Mundo"
        ]
        
        # Seleccionar 3-5 categorías adicionales
        num_adicionales = random.randint(3, 5)
        categorias_seleccionadas = random.sample(categorias_adicionales, num_adicionales)
        
        return categorias_base + categorias_seleccionadas
    
    def generar_contacto(self, dominio: str, nombre: str) -> Dict[str, str]:
        """
        Genera información de contacto para el sitio
        
        Args:
            dominio: Dominio del sitio
            nombre: Nombre del sitio
            
        Returns:
            dict: Información de contacto
        """
        return {
            "email_general": f"contacto@{dominio}",
            "email_redaccion": f"redaccion@{dominio}",
            "email_publicidad": f"publicidad@{dominio}",
            "telefono": f"+52 55 {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
            "direccion": "Ciudad de México, México",
            "horario": "Disponible 24/7"
        }
    
    def generar_redes_sociales(self, nombre: str, dominio: str) -> Dict[str, str]:
        """
        Genera URLs de redes sociales (placeholders)
        
        Args:
            nombre: Nombre del sitio
            dominio: Dominio base
            
        Returns:
            dict: URLs de redes sociales
        """
        # Limpiar nombre para username
        username = dominio.split('.')[0]
        
        return {
            "facebook": f"https://facebook.com/{username}",
            "twitter": f"https://twitter.com/{username}",
            "instagram": f"https://instagram.com/{username}",
            "youtube": f"https://youtube.com/@{username}",
            "linkedin": f"https://linkedin.com/company/{username}",
            "telegram": f"https://t.me/{username}"
        }
    
    def generar_metadata_seo(self, nombre: str, tagline: str, dominio: str) -> Dict[str, any]:
        """
        Genera metadatos SEO
        
        Args:
            nombre: Nombre del sitio
            tagline: Tagline del sitio
            dominio: Dominio completo
            
        Returns:
            dict: Metadatos SEO
        """
        return {
            "titulo": f"{nombre} - {tagline}",
            "descripcion": f"{nombre} es tu fuente confiable de noticias e información actualizada. {tagline}. Mantente informado con las últimas noticias de México y el mundo.",
            "keywords": [
                "noticias", "méxico", "actualidad", "información",
                "política", "economía", "deportes", "entretenimiento",
                nombre.lower(), dominio.split('.')[0]
            ],
            "og_type": "website",
            "og_locale": "es_MX",
            "twitter_card": "summary_large_image"
        }
    
    def verificar_y_seleccionar_dominio(
        self,
        nombre_sitio: str,
        max_intentos: int = 5,
        verificar_whois: bool = True
    ) -> Dict[str, any]:
        """
        Verifica disponibilidad y selecciona el mejor dominio
        
        Args:
            nombre_sitio: Nombre del sitio
            max_intentos: Máximo de intentos para encontrar dominio disponible
            verificar_whois: Si hacer verificación whois real
            
        Returns:
            dict: Información del dominio seleccionado
        """
        dominios_intentar = []
        
        # Generar variantes del dominio
        nombre_base, tld_preferido = self.name_generator.generar_dominio(nombre_sitio)
        
        # Lista de TLDs a intentar en orden de preferencia
        tlds_probar = [tld_preferido, "com", "mx", "com.mx", "news", "info"]
        
        for tld in tlds_probar[:max_intentos]:
            dominios_intentar.append(f"{nombre_base}.{tld}")
        
        # Si no se verifica whois, usar el primero
        if not verificar_whois:
            return {
                "dominio": dominios_intentar[0],
                "disponible": True,
                "verificado": False,
                "mensaje": "Dominio no verificado (modo simulación)"
            }
        
        # Verificar cada dominio
        print(f"\n🔍 Verificando disponibilidad de dominios para '{nombre_sitio}'...")
        
        for dominio in dominios_intentar:
            resultado = self.domain_verifier.verificar_dominio(dominio)
            
            if resultado.get('disponible'):
                print(f"   ✅ {dominio} - DISPONIBLE")
                return {
                    "dominio": dominio,
                    "disponible": True,
                    "verificado": True,
                    "resultado_whois": resultado
                }
            elif resultado.get('registrado'):
                print(f"   ⛔ {dominio} - Registrado")
            else:
                print(f"   ❓ {dominio} - Estado desconocido")
        
        # Si ninguno está disponible, usar el primero sin verificar
        print(f"   ⚠️ Ningún dominio verificado disponible, usando {dominios_intentar[0]}")
        return {
            "dominio": dominios_intentar[0],
            "disponible": False,
            "verificado": True,
            "mensaje": "Ningún dominio disponible encontrado"
        }
    
    def crear_metadata_sitio(
        self,
        estilo_nombre: Optional[str] = None,
        verificar_dominio: bool = True
    ) -> Dict[str, any]:
        """
        Crea metadatos completos para un sitio
        
        Args:
            estilo_nombre: Estilo de nombre o None para aleatorio
            verificar_dominio: Si verificar disponibilidad del dominio
            
        Returns:
            dict: Metadatos completos del sitio
        """
        # Generar información básica
        sitio_info = self.name_generator.generar_sitio_completo(estilo_nombre)
        
        # Verificar y seleccionar dominio
        dominio_info = self.verificar_y_seleccionar_dominio(
            sitio_info['nombre'],
            verificar_whois=verificar_dominio
        )
        
        # Generar componentes adicionales
        colores = self.generar_colores_marca()
        
        # Construir metadata completa
        metadata = {
            # Información básica
            "id": f"site_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}",
            "nombre": sitio_info['nombre'],
            "tagline": sitio_info['tagline'],
            "estilo": sitio_info['estilo'],
            
            # Dominio
            "dominio": dominio_info['dominio'],
            "dominio_verificado": dominio_info.get('verificado', False),
            "dominio_disponible": dominio_info.get('disponible', False),
            
            # Marca visual
            "colores": colores,
            "logo": self.generar_metadata_logo(sitio_info['nombre'], colores),
            
            # Contenido
            "categorias": self.generar_categorias_noticias(),
            
            # Contacto y redes
            "contacto": self.generar_contacto(dominio_info['dominio'], sitio_info['nombre']),
            "redes_sociales": self.generar_redes_sociales(sitio_info['nombre'], dominio_info['dominio']),
            
            # SEO
            "seo": self.generar_metadata_seo(
                sitio_info['nombre'],
                sitio_info['tagline'],
                dominio_info['dominio']
            ),
            
            # Metadatos
            "fecha_creacion": datetime.now().isoformat(),
            "version": "1.0",
            "estado": "pre-creado"
        }
        
        return metadata
    
    def crear_batch_sitios(
        self,
        cantidad: int = 10,
        verificar_dominios: bool = False,
        guardar_archivo: bool = True
    ) -> List[Dict[str, any]]:
        """
        Crea múltiples metadatos de sitios
        
        Args:
            cantidad: Número de sitios a crear
            verificar_dominios: Si verificar disponibilidad con whois
            guardar_archivo: Si guardar en archivo JSON
            
        Returns:
            list: Lista de metadatos de sitios
        """
        print(f"\n🚀 Generando metadatos para {cantidad} sitios...")
        print("=" * 60)
        
        if verificar_dominios:
            # Verificar que whois esté disponible
            if not self.domain_verifier.verificar_whois_instalado():
                print("\n⚠️ whois no está instalado. Dominios no serán verificados.")
                print(self.domain_verifier.instalar_whois_instrucciones())
                verificar_dominios = False
        
        sitios_metadata = []
        
        for i in range(1, cantidad + 1):
            print(f"\n📝 Sitio {i}/{cantidad}")
            
            # Crear metadata
            metadata = self.crear_metadata_sitio(verificar_dominio=verificar_dominios)
            sitios_metadata.append(metadata)
            
            print(f"   Nombre: {metadata['nombre']}")
            print(f"   Dominio: {metadata['dominio']}")
            print(f"   Disponible: {'✅' if metadata['dominio_disponible'] else '❓'}")
        
        # Guardar en archivo si se solicita
        if guardar_archivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/sites_metadata_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(sitios_metadata, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Metadatos guardados en: {filename}")
        
        # Estadísticas
        verificados = sum(1 for s in sitios_metadata if s['dominio_verificado'])
        disponibles = sum(1 for s in sitios_metadata if s['dominio_disponible'])
        
        print(f"\n📊 Resumen:")
        print(f"   Total de sitios: {cantidad}")
        print(f"   Dominios verificados: {verificados}")
        print(f"   Dominios disponibles: {disponibles}")
        
        return sitios_metadata
    
    def cargar_metadata(self, filepath: str) -> List[Dict[str, any]]:
        """
        Carga metadatos desde archivo JSON
        
        Args:
            filepath: Ruta al archivo JSON
            
        Returns:
            list: Lista de metadatos
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def exportar_para_site_builder(
        self,
        metadata: Dict[str, any],
        output_file: Optional[str] = None
    ) -> str:
        """
        Exporta metadata en formato optimizado para site-builder
        
        Args:
            metadata: Metadatos del sitio
            output_file: Archivo de salida (opcional)
            
        Returns:
            str: Ruta del archivo generado
        """
        # Formato simplificado para site-builder
        builder_data = {
            "site_id": metadata['id'],
            "name": metadata['nombre'],
            "tagline": metadata['tagline'],
            "domain": metadata['dominio'],
            "colors": metadata['colores'],
            "logo_specs": metadata['logo'],
            "categories": metadata['categorias'],
            "contact": metadata['contacto'],
            "social": metadata['redes_sociales'],
            "seo": metadata['seo']
        }
        
        if not output_file:
            output_file = f"{self.output_dir}/builder_{metadata['id']}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(builder_data, f, indent=2, ensure_ascii=False)
        
        return output_file


def main():
    """Función principal de demostración"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Protocolo de Pre-Creación de Sitios de Noticias"
    )
    parser.add_argument(
        '--cantidad',
        type=int,
        default=5,
        help='Número de sitios a generar (default: 5)'
    )
    parser.add_argument(
        '--verificar-dominios',
        action='store_true',
        help='Verificar disponibilidad de dominios con whois'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='../data/sites_metadata',
        help='Directorio de salida para metadatos'
    )
    
    args = parser.parse_args()
    
    # Crear protocolo
    protocolo = SitePreCreation(output_dir=args.output)
    
    # Generar sitios
    sitios = protocolo.crear_batch_sitios(
        cantidad=args.cantidad,
        verificar_dominios=args.verificar_dominios,
        guardar_archivo=True
    )
    
    # Exportar primer sitio como ejemplo para site-builder
    if sitios:
        builder_file = protocolo.exportar_para_site_builder(sitios[0])
        print(f"\n📦 Ejemplo para site-builder: {builder_file}")
    
    print("\n✅ ¡Proceso completado!")


if __name__ == "__main__":
    main()

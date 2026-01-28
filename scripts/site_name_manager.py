#!/usr/bin/env python3
"""
Gestor de nombres de sitios para el orquestador
Permite asignar nombres manualmente o generarlos automáticamente
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime

from site_name_generator import SiteNameGenerator


class SiteNameManager:
    """Gestor de nombres de sitios para el orquestador"""
    
    def __init__(self, config_file: str = "data/sites_config.json"):
        """
        Inicializa el gestor de nombres de sitios
        
        Args:
            config_file: Archivo de configuración para nombres de sitios
        """
        self.config_file = Path(config_file)
        self.config_file.parent.mkdir(exist_ok=True)
        self.generator = SiteNameGenerator()
        self._load_config()
    
    def _load_config(self):
        """Carga la configuración desde el archivo JSON"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"⚠️  Error cargando configuración: {e}")
                self.config = self._get_default_config()
        else:
            self.config = self._get_default_config()
    
    def _save_config(self):
        """Guarda la configuración en el archivo JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  Error guardando configuración: {e}")
    
    def _get_default_config(self) -> Dict:
        """Obtiene la configuración por defecto"""
        return {
            "modo_asignacion": "automatico",  # "manual" o "automatico"
            "sitios_manuales": [],
            "preferencias_automatico": {
                "estilos": ["clasico", "moderno", "regional"],
                "excluir_nombres": [],
                "preferencias_tld": ["com", "mx", "news"]
            },
            "historial_generados": []
        }
    
    def set_modo_asignacion(self, modo: str):
        """
        Establece el modo de asignación de nombres
        
        Args:
            modo: "manual" o "automatico"
        """
        if modo not in ["manual", "automatico"]:
            raise ValueError("El modo debe ser 'manual' o 'automatico'")
        
        self.config["modo_asignacion"] = modo
        self._save_config()
        print(f"✅ Modo de asignación cambiado a: {modo}")
    
    def agregar_sitio_manual(self, nombre: str, tagline: Optional[str] = None, 
                           dominio: Optional[str] = None):
        """
        Agrega un sitio con nombre manual
        
        Args:
            nombre: Nombre del sitio
            tagline: Tagline del sitio (opcional)
            dominio: Dominio del sitio (opcional)
        """
        sitio = {
            "nombre": nombre,
            "tagline": tagline or self.generator.generar_tagline(nombre),
            "dominio": dominio,
            "fecha_agregado": datetime.now().isoformat(),
            "usado": False
        }
        
        self.config["sitios_manuales"].append(sitio)
        self._save_config()
        print(f"✅ Sitio agregado manualmente: {nombre}")
    
    def eliminar_sitio_manual(self, nombre: str):
        """
        Elimina un sitio de la lista manual
        
        Args:
            nombre: Nombre del sitio a eliminar
        """
        self.config["sitios_manuales"] = [
            s for s in self.config["sitios_manuales"] 
            if s["nombre"] != nombre
        ]
        self._save_config()
        print(f"✅ Sitio eliminado: {nombre}")
    
    def listar_sitios_manuales(self) -> List[Dict]:
        """Lista todos los sitios manuales"""
        return self.config["sitios_manuales"]
    
    def limpiar_sitios_manuales(self):
        """Limpia todos los sitios manuales"""
        self.config["sitios_manuales"] = []
        self._save_config()
        print("✅ Sitios manuales limpiados")
    
    def set_preferencias_automatico(self, estilos: List[str] = None, 
                                  excluir_nombres: List[str] = None,
                                  preferencias_tld: List[str] = None):
        """
        Configura las preferencias para la generación automática
        
        Args:
            estilos: Lista de estilos de nombres a usar
            excluir_nombres: Lista de nombres a excluir
            preferencias_tld: Lista de TLDs preferidos
        """
        if estilos:
            self.config["preferencias_automatico"]["estilos"] = estilos
        if excluir_nombres:
            self.config["preferencias_automatico"]["excluir_nombres"] = excluir_nombres
        if preferencias_tld:
            self.config["preferencias_automatico"]["preferencias_tld"] = preferencias_tld
        
        self._save_config()
        print("✅ Preferencias automáticas actualizadas")
    
    def obtener_siguiente_nombre(self, sitio_id: Optional[str] = None) -> Dict:
        """
        Obtiene el siguiente nombre de sitio según el modo configurado
        
        Args:
            sitio_id: Identificador del sitio (para seguimiento)
            
        Returns:
            Dict: Información del sitio con nombre, tagline y dominio
        """
        if self.config["modo_asignacion"] == "manual":
            return self._obtener_nombre_manual(sitio_id)
        else:
            return self._obtener_nombre_automatico(sitio_id)
    
    def _obtener_nombre_manual(self, sitio_id: Optional[str]) -> Dict:
        """Obtiene un nombre de la lista manual"""
        sitios_disponibles = [
            s for s in self.config["sitios_manuales"] 
            if not s.get("usado", False)
        ]
        
        if not sitios_disponibles:
            print("⚠️  No hay sitios manuales disponibles, generando uno automático")
            return self._obtener_nombre_automatico(sitio_id)
        
        # Seleccionar aleatoriamente entre los disponibles
        sitio = random.choice(sitios_disponibles)
        sitio["usado"] = True
        sitio["fecha_usado"] = datetime.now().isoformat()
        sitio["sitio_id"] = sitio_id
        
        self._save_config()
        
        return {
            "nombre": sitio["nombre"],
            "tagline": sitio["tagline"],
            "dominio": sitio["dominio"],
            "modo": "manual",
            "sitio_id": sitio_id
        }
    
    def _obtener_nombre_automatico(self, sitio_id: Optional[str]) -> Dict:
        """Genera un nombre automáticamente"""
        preferencias = self.config["preferencias_automatico"]
        
        # Generar nombre con preferencias
        estilo = random.choice(preferencias["estilos"])
        sitio_info = self.generator.generar_sitio_completo(estilo)
        
        # Verificar exclusiones
        intentos = 0
        while sitio_info["nombre"] in preferencias["excluir_nombres"] and intentos < 10:
            sitio_info = self.generator.generar_sitio_completo(estilo)
            intentos += 1
        
        # Guardar en historial
        sitio_info["fecha_generado"] = datetime.now().isoformat()
        sitio_info["sitio_id"] = sitio_id
        sitio_info["modo"] = "automatico"
        
        self.config["historial_generados"].append(sitio_info)
        
        # Limitar historial a 100 entradas
        if len(self.config["historial_generados"]) > 100:
            self.config["historial_generados"] = self.config["historial_generados"][-100:]
        
        self._save_config()
        
        return sitio_info
    
    def resetear_uso_manual(self):
        """Reinicia el estado de uso de los sitios manuales"""
        for sitio in self.config["sitios_manuales"]:
            sitio["usado"] = False
            if "fecha_usado" in sitio:
                del sitio["fecha_usado"]
        
        self._save_config()
        print("✅ Estado de uso de sitios manuales reiniciado")
    
    def get_config(self) -> Dict:
        """Obtiene la configuración actual"""
        return self.config.copy()
    
    def exportar_configuracion(self, output_file: str):
        """Exporta la configuración a un archivo JSON"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
        print(f"✅ Configuración exportada a: {output_file}")
    
    def importar_configuracion(self, input_file: str):
        """Importa la configuración desde un archivo JSON"""
        with open(input_file, 'r', encoding='utf-8') as f:
            nueva_config = json.load(f)
        
        self.config = nueva_config
        self._save_config()
        print(f"✅ Configuración importada desde: {input_file}")


def main():
    """Función de prueba y demostración"""
    print("🔧 Gestor de Nombres de Sitios")
    print("=" * 50)
    
    manager = SiteNameManager()
    
    # Mostrar configuración actual
    config = manager.get_config()
    print(f"\n📋 Configuración actual:")
    print(f"   Modo: {config['modo_asignacion']}")
    print(f"   Sitios manuales: {len(config['sitios_manuales'])}")
    print(f"   Historial generado: {len(config['historial_generados'])}")
    
    # Ejemplo de uso manual
    print(f"\n📝 Ejemplo de uso manual:")
    manager.set_modo_asignacion("manual")
    manager.agregar_sitio_manual("El Diario de Prueba", "Noticias confiables", "dprueba.com")
    manager.agregar_sitio_manual("Noticias Test", "Actualidad en tiempo real")
    
    sitio_manual = manager.obtener_siguiente_nombre("test_001")
    print(f"   Sitio obtenido: {sitio_manual['nombre']}")
    
    # Ejemplo de uso automático
    print(f"\n🤖 Ejemplo de uso automático:")
    manager.set_modo_asignacion("automatico")
    
    sitio_auto = manager.obtener_siguiente_nombre("test_002")
    print(f"   Sitio generado: {sitio_auto['nombre']}")
    print(f"   Tagline: {sitio_auto['tagline']}")
    print(f"   Dominio: {sitio_auto['dominio_completo']}")
    
    # Mostrar configuración final
    print(f"\n📊 Configuración final:")
    config_final = manager.get_config()
    print(f"   Sitios manuales: {len(config_final['sitios_manuales'])}")
    print(f"   Historial generado: {len(config_final['historial_generados'])}")


if __name__ == "__main__":
    main()
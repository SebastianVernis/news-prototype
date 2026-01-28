#!/usr/bin/env python3
"""
Verificador de disponibilidad de dominios usando APILayer WHOIS API
API Documentation: https://apilayer.com/marketplace/whois-api
"""

import os
import time
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class DomainVerifierAPILayer:
    """Verificador de disponibilidad de dominios usando APILayer WHOIS API"""
    
    def __init__(self, api_key: Optional[str] = None, rate_limit_delay: float = 1.0):
        """
        Inicializa el verificador
        
        Args:
            api_key: API key de APILayer (si no se provee, se lee de .env)
            rate_limit_delay: Segundos entre consultas para evitar rate limiting
        """
        self.api_key = api_key or os.getenv('APILAYER_API_KEY')
        if not self.api_key:
            raise ValueError("API key de APILayer no encontrada. Configura APILAYER_API_KEY en .env")
        
        self.base_url = "https://api.apilayer.com/whois/query"
        self.rate_limit_delay = rate_limit_delay
        self.last_query_time = 0
        self.verificaciones_cache = {}
        
    def _rate_limit(self):
        """Implementa rate limiting entre consultas"""
        tiempo_actual = time.time()
        tiempo_desde_ultima = tiempo_actual - self.last_query_time
        
        if tiempo_desde_ultima < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - tiempo_desde_ultima)
        
        self.last_query_time = time.time()
    
    def consultar_whois(self, dominio: str) -> tuple[bool, Dict]:
        """
        Consulta WHOIS para un dominio usando APILayer
        
        Args:
            dominio: Nombre de dominio completo (ej: example.com)
            
        Returns:
            tuple: (exito, datos_whois o error_msg)
        """
        # Rate limiting
        self._rate_limit()
        
        url = f"{self.base_url}?domain={dominio}"
        headers = {
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                # APILayer envuelve los datos en {"result": {...}}
                if 'result' in data:
                    return (True, data['result'])
                return (True, data)
            elif response.status_code == 404:
                # 404 significa que el dominio no está registrado (disponible)
                return (True, {"domain_not_found": True})
            elif response.status_code == 401:
                return (False, {"error": "API key inválida"})
            elif response.status_code == 429:
                return (False, {"error": "Rate limit excedido"})
            else:
                return (False, {"error": f"Error HTTP {response.status_code}: {response.text}"})
                
        except requests.exceptions.Timeout:
            return (False, {"error": "Timeout al consultar API"})
        except requests.exceptions.RequestException as e:
            return (False, {"error": f"Error de red: {str(e)}"})
        except Exception as e:
            return (False, {"error": f"Error inesperado: {str(e)}"})
    
    def analizar_disponibilidad(self, datos_whois: Dict, dominio: str) -> Dict:
        """
        Analiza los datos de WHOIS para determinar disponibilidad
        
        Args:
            datos_whois: Respuesta JSON de APILayer
            dominio: Dominio consultado
            
        Returns:
            dict: Información de disponibilidad
        """
        # APILayer retorna datos estructurados
        # Campos comunes: domain_name, registrar, creation_date, expiration_date, 
        # name_servers, status, registrant_name, etc.
        
        # Si hay error en la respuesta
        if 'error' in datos_whois:
            return {
                "dominio": dominio,
                "estado": "error",
                "disponible": None,
                "registrado": None,
                "error": datos_whois['error']
            }
        
        # Si la API retornó 404, el dominio está disponible
        if 'domain_not_found' in datos_whois:
            return {
                "dominio": dominio,
                "estado": "disponible",
                "disponible": True,
                "registrado": False,
                "info_adicional": {},
                "datos_raw": datos_whois
            }
        
        # Verificar si el dominio está registrado
        # Un dominio registrado tendrá campos como domain_name, registrar, etc.
        registrado = False
        info_adicional = {}
        
        # Campos que indican que el dominio está registrado
        campos_registro = ['domain_name', 'registrar', 'creation_date', 'name_servers']
        
        for campo in campos_registro:
            if campo in datos_whois and datos_whois[campo]:
                registrado = True
                break
        
        if registrado:
            # Extraer información relevante
            if 'registrar' in datos_whois:
                info_adicional['registrar'] = datos_whois['registrar']
            
            if 'creation_date' in datos_whois:
                info_adicional['fecha_creacion'] = datos_whois['creation_date']
            
            if 'expiration_date' in datos_whois:
                info_adicional['fecha_expiracion'] = datos_whois['expiration_date']
            
            if 'status' in datos_whois:
                info_adicional['estado'] = datos_whois['status']
            
            if 'name_servers' in datos_whois:
                info_adicional['name_servers'] = datos_whois['name_servers']
            
            estado = "registrado"
            disponible = False
        else:
            # Si no hay campos de registro, probablemente está disponible
            estado = "disponible"
            disponible = True
        
        return {
            "dominio": dominio,
            "estado": estado,
            "disponible": disponible,
            "registrado": registrado,
            "info_adicional": info_adicional,
            "datos_raw": datos_whois
        }
    
    def verificar_dominio(self, dominio: str, usar_cache: bool = True) -> Dict:
        """
        Verifica la disponibilidad de un dominio
        
        Args:
            dominio: Dominio completo (ej: example.com)
            usar_cache: Si usar caché de verificaciones anteriores
            
        Returns:
            dict: Información de verificación
        """
        # Verificar cache
        if usar_cache and dominio in self.verificaciones_cache:
            resultado = self.verificaciones_cache[dominio].copy()
            resultado['desde_cache'] = True
            return resultado
        
        # Consultar WHOIS
        exito, datos = self.consultar_whois(dominio)
        
        if not exito:
            return {
                "dominio": dominio,
                "estado": "error",
                "disponible": None,
                "error": datos.get('error', 'Error desconocido')
            }
        
        # Analizar disponibilidad
        resultado = self.analizar_disponibilidad(datos, dominio)
        resultado['desde_cache'] = False
        
        # Guardar en cache
        if usar_cache:
            self.verificaciones_cache[dominio] = resultado.copy()
        
        return resultado
    
    def verificar_dominios_batch(self, dominios: list, max_errores: int = 3) -> list:
        """
        Verifica múltiples dominios
        
        Args:
            dominios: Lista de dominios a verificar
            max_errores: Máximo de errores consecutivos antes de abortar
            
        Returns:
            list: Lista de resultados de verificación
        """
        resultados = []
        errores_consecutivos = 0
        
        for i, dominio in enumerate(dominios, 1):
            print(f"Verificando {i}/{len(dominios)}: {dominio}...", end=" ")
            
            resultado = self.verificar_dominio(dominio)
            resultados.append(resultado)
            
            if resultado['estado'] == 'error':
                errores_consecutivos += 1
                print(f"❌ ERROR: {resultado.get('error', 'Desconocido')}")
                
                if errores_consecutivos >= max_errores:
                    print(f"\n⚠️ Demasiados errores consecutivos. Abortando.")
                    break
            else:
                errores_consecutivos = 0
                if resultado.get('disponible'):
                    print("✅ DISPONIBLE")
                elif resultado.get('registrado'):
                    print("⛔ REGISTRADO")
                else:
                    print("❓ DESCONOCIDO")
            
            # Rate limiting entre dominios
            if i < len(dominios):
                time.sleep(self.rate_limit_delay)
        
        return resultados
    
    def limpiar_cache(self):
        """Limpia el caché de verificaciones"""
        self.verificaciones_cache = {}
    
    def verificar_api_key(self) -> tuple[bool, str]:
        """
        Verifica que la API key sea válida haciendo una consulta de prueba
        
        Returns:
            tuple: (valida, mensaje)
        """
        try:
            exito, datos = self.consultar_whois("google.com")
            if exito:
                return (True, "API key válida")
            else:
                error = datos.get('error', 'Error desconocido')
                if 'API key inválida' in error or '401' in error:
                    return (False, "API key inválida")
                return (True, "API key válida (dominio de prueba retornó error esperado)")
        except Exception as e:
            return (False, f"Error al verificar API key: {str(e)}")


def main():
    """Función de prueba"""
    print("🔍 Verificador de Disponibilidad de Dominios (APILayer WHOIS)")
    print("=" * 70)
    
    try:
        verifier = DomainVerifierAPILayer(rate_limit_delay=1.0)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\n📝 Configura tu API key en el archivo .env:")
        print("   APILAYER_API_KEY=\"tu_api_key_aqui\"")
        print("\n🔗 Obtén tu API key en: https://apilayer.com/marketplace/whois-api")
        return
    
    # Verificar API key
    print("\n🔑 Verificando API key...", end=" ")
    valida, mensaje = verifier.verificar_api_key()
    if valida:
        print(f"✅ {mensaje}")
    else:
        print(f"❌ {mensaje}")
        return
    
    # Dominios de prueba
    dominios_prueba = [
        "google.com",           # Debe estar registrado
        "ejemplo-no-existe-xyz123456789.com",  # Probablemente disponible
    ]
    
    print(f"\n🧪 Probando con {len(dominios_prueba)} dominios:\n")
    
    resultados = verifier.verificar_dominios_batch(dominios_prueba)
    
    print("\n📊 Resumen de Resultados:\n")
    
    for resultado in resultados:
        print(f"Dominio: {resultado['dominio']}")
        print(f"Estado: {resultado['estado'].upper()}")
        
        if resultado.get('disponible'):
            print("✅ DISPONIBLE para registro")
        elif resultado.get('registrado'):
            print("⛔ YA REGISTRADO")
            if resultado.get('info_adicional'):
                print("\n📋 Información adicional:")
                for key, value in resultado['info_adicional'].items():
                    if isinstance(value, list):
                        print(f"   {key}: {', '.join(str(v) for v in value[:3])}")
                    else:
                        print(f"   {key}: {value}")
        elif resultado['estado'] == 'error':
            print(f"❌ Error: {resultado.get('error')}")
        
        print("-" * 70)
    
    # Estadísticas finales
    total = len(resultados)
    disponibles = sum(1 for r in resultados if r.get('disponible'))
    registrados = sum(1 for r in resultados if r.get('registrado'))
    errores = sum(1 for r in resultados if r['estado'] == 'error')
    
    print("\n📈 Estadísticas:")
    print(f"   Total verificados: {total}")
    print(f"   Disponibles: {disponibles}")
    print(f"   Registrados: {registrados}")
    print(f"   Errores: {errores}")


if __name__ == "__main__":
    main()

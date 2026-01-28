#!/usr/bin/env python3
"""
Verificador de disponibilidad de dominios
Soporta dos métodos:
1. Local whois (comando del sistema)
2. APILayer WHOIS API (https://apilayer.com/marketplace/whois-api)
"""

import subprocess
import re
import time
import os
import requests
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class DomainVerifier:
    """Verificador de disponibilidad de dominios con soporte para whois local y APILayer"""
    
    def __init__(self, rate_limit_delay=1.0, usar_api=False, api_key=None):
        """
        Inicializa el verificador
        
        Args:
            rate_limit_delay: Segundos entre consultas para evitar rate limiting
            usar_api: Si True, usa APILayer WHOIS API. Si False, usa whois local
            api_key: API key de APILayer (opcional, se lee de .env si no se provee)
        """
        self.rate_limit_delay = rate_limit_delay
        self.last_query_time = 0
        self.verificaciones_cache = {}
        self.usar_api = usar_api
        
        # Configurar API si está habilitada
        if self.usar_api:
            self.api_key = api_key or os.getenv('APILAYER_API_KEY')
            if not self.api_key:
                print("⚠️ API key de APILayer no encontrada. Cambiando a whois local.")
                self.usar_api = False
            else:
                self.base_url = "https://api.apilayer.com/whois/query"
    
    def _rate_limit(self):
        """Implementa rate limiting entre consultas"""
        tiempo_actual = time.time()
        tiempo_desde_ultima = tiempo_actual - self.last_query_time
        
        if tiempo_desde_ultima < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - tiempo_desde_ultima)
        
        self.last_query_time = time.time()
    
    def verificar_whois_instalado(self) -> bool:
        """
        Verifica si whois está instalado en el sistema
        
        Returns:
            bool: True si whois está disponible
        """
        try:
            result = subprocess.run(
                ['which', 'whois'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def instalar_whois_instrucciones(self) -> str:
        """
        Retorna instrucciones para instalar whois
        
        Returns:
            str: Instrucciones de instalación
        """
        return """
Para instalar whois:

Ubuntu/Debian:
    sudo apt-get update && sudo apt-get install whois

Fedora/CentOS/RHEL:
    sudo dnf install whois

MacOS:
    whois viene preinstalado en MacOS

Arch Linux:
    sudo pacman -S whois
"""
    
    def consultar_whois_api(self, dominio: str) -> Tuple[bool, Dict]:
        """
        Consulta WHOIS usando APILayer API
        
        Args:
            dominio: Nombre de dominio completo (ej: example.com)
            
        Returns:
            tuple: (exito, datos_whois o error_dict)
        """
        # Rate limiting
        self._rate_limit()
        
        url = f"{self.base_url}?domain={dominio}"
        headers = {'apikey': self.api_key}
        
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
                return (False, {"error": f"Error HTTP {response.status_code}"})
                
        except requests.exceptions.Timeout:
            return (False, {"error": "Timeout al consultar API"})
        except Exception as e:
            return (False, {"error": f"Error: {str(e)}"})
    
    def consultar_whois_local(self, dominio: str, servidor_whois: Optional[str] = None) -> Tuple[bool, str]:
        """
        Consulta whois local para un dominio
        
        Args:
            dominio: Nombre de dominio completo (ej: example.com)
            servidor_whois: Servidor whois específico (opcional)
            
        Returns:
            tuple: (exito, salida_whois)
        """
        # Rate limiting
        self._rate_limit()
        
        # Preparar comando
        cmd = ['whois']
        if servidor_whois:
            cmd.extend(['-h', servidor_whois])
        cmd.append(dominio)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return (True, result.stdout)
            else:
                return (False, result.stderr)
                
        except subprocess.TimeoutExpired:
            return (False, "Timeout al consultar whois")
        except Exception as e:
            return (False, f"Error: {str(e)}")
    
    def consultar_whois(self, dominio: str, servidor_whois: Optional[str] = None) -> Tuple[bool, any]:
        """
        Consulta whois (API o local según configuración)
        
        Args:
            dominio: Nombre de dominio completo (ej: example.com)
            servidor_whois: Servidor whois específico (solo para whois local)
            
        Returns:
            tuple: (exito, datos)
        """
        if self.usar_api:
            return self.consultar_whois_api(dominio)
        else:
            return self.consultar_whois_local(dominio, servidor_whois)
    
    def analizar_disponibilidad_api(self, datos_whois: Dict, dominio: str) -> Dict:
        """
        Analiza datos de APILayer para determinar disponibilidad
        
        Args:
            datos_whois: Respuesta JSON de APILayer
            dominio: Dominio consultado
            
        Returns:
            dict: Información de disponibilidad
        """
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
                "metodo": "api"
            }
        
        # Verificar campos de registro
        registrado = False
        info_adicional = {}
        campos_registro = ['domain_name', 'registrar', 'creation_date', 'name_servers']
        
        for campo in campos_registro:
            if campo in datos_whois and datos_whois[campo]:
                registrado = True
                break
        
        if registrado:
            if 'registrar' in datos_whois:
                info_adicional['registrar'] = datos_whois['registrar']
            if 'creation_date' in datos_whois:
                info_adicional['fecha_creacion'] = datos_whois['creation_date']
            if 'expiration_date' in datos_whois:
                info_adicional['fecha_expiracion'] = datos_whois['expiration_date']
            if 'status' in datos_whois:
                info_adicional['estado'] = datos_whois['status']
        
        return {
            "dominio": dominio,
            "estado": "registrado" if registrado else "disponible",
            "disponible": not registrado,
            "registrado": registrado,
            "info_adicional": info_adicional,
            "metodo": "api"
        }
    
    def analizar_disponibilidad_local(self, salida_whois: str, dominio: str) -> Dict:
        """
        Analiza la salida de whois local para determinar disponibilidad
        
        Args:
            salida_whois: Salida del comando whois
            dominio: Dominio consultado
            
        Returns:
            dict: Información de disponibilidad
        """
        salida_lower = salida_whois.lower()
        
        # Patrones que indican dominio NO disponible (registrado)
        patrones_registrado = [
            r'domain name:',
            r'registrar:',
            r'registrant',
            r'creation date:',
            r'created:',
            r'status: active',
            r'status: ok',
            r'name server',
            r'nserver:'
        ]
        
        # Patrones que indican dominio disponible
        patrones_disponible = [
            r'no match',
            r'not found',
            r'no entries found',
            r'no data found',
            r'domain not found',
            r'no se encontr[oó]',
            r'objeto no existe',
            r'available',
            r'disponible'
        ]
        
        # Verificar si está registrado
        registrado = False
        for patron in patrones_registrado:
            if re.search(patron, salida_lower):
                registrado = True
                break
        
        # Verificar si está disponible
        disponible = False
        for patron in patrones_disponible:
            if re.search(patron, salida_lower):
                disponible = True
                break
        
        # Extraer información adicional si está registrado
        info_adicional = {}
        
        if registrado:
            # Buscar registrar
            match_registrar = re.search(r'registrar:\s*(.+)', salida_lower)
            if match_registrar:
                info_adicional['registrar'] = match_registrar.group(1).strip()
            
            # Buscar fecha de creación
            match_creation = re.search(r'(?:creation date|created):\s*(.+)', salida_lower)
            if match_creation:
                info_adicional['fecha_creacion'] = match_creation.group(1).strip()
            
            # Buscar estado
            match_status = re.search(r'status:\s*(.+)', salida_lower)
            if match_status:
                info_adicional['estado'] = match_status.group(1).strip()
        
        # Determinar disponibilidad final
        if disponible and not registrado:
            estado = "disponible"
        elif registrado and not disponible:
            estado = "registrado"
        else:
            estado = "desconocido"
        
        return {
            "dominio": dominio,
            "estado": estado,
            "disponible": estado == "disponible",
            "registrado": estado == "registrado",
            "info_adicional": info_adicional,
            "metodo": "local",
            "salida_raw": salida_whois[:500]
        }
    
    def analizar_disponibilidad(self, datos: any, dominio: str) -> Dict:
        """
        Analiza disponibilidad según el método usado
        
        Args:
            datos: Datos de whois (string para local, dict para API)
            dominio: Dominio consultado
            
        Returns:
            dict: Información de disponibilidad
        """
        if self.usar_api and isinstance(datos, dict):
            return self.analizar_disponibilidad_api(datos, dominio)
        else:
            return self.analizar_disponibilidad_local(datos, dominio)
    
    def verificar_dominio(self, dominio: str, usar_cache: bool = True) -> Dict[str, any]:
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
        
        # Verificar requisitos según método
        if not self.usar_api:
            if not self.verificar_whois_instalado():
                return {
                    "dominio": dominio,
                    "estado": "error",
                    "disponible": None,
                    "error": "whois no está instalado",
                    "instrucciones": self.instalar_whois_instrucciones()
                }
        
        # Consultar whois
        exito, datos = self.consultar_whois(dominio)
        
        if not exito:
            error_msg = datos.get('error', datos) if isinstance(datos, dict) else datos
            return {
                "dominio": dominio,
                "estado": "error",
                "disponible": None,
                "error": error_msg
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
                print(f"❌ ERROR")
                
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


def main():
    """Función de prueba"""
    print("🔍 Verificador de Disponibilidad de Dominios")
    print("=" * 70)
    
    # Detectar si hay API key disponible
    api_key = os.getenv('APILAYER_API_KEY')
    usar_api = bool(api_key)
    
    if usar_api:
        print("\n🔑 API key de APILayer detectada - Usando WHOIS API")
        verifier = DomainVerifier(rate_limit_delay=1.0, usar_api=True)
    else:
        print("\n🖥️  API key no encontrada - Usando whois local")
        verifier = DomainVerifier(rate_limit_delay=2.0, usar_api=False)
        
        # Verificar que whois esté instalado
        if not verifier.verificar_whois_instalado():
            print("\n❌ whois no está instalado en el sistema")
            print(verifier.instalar_whois_instrucciones())
            print("\n💡 Alternativamente, configura APILAYER_API_KEY en .env para usar la API")
            return
        
        print("✅ whois local está instalado")
    
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
        print(f"Método: {resultado.get('metodo', 'desconocido').upper()}")
        
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
    
    # Estadísticas
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

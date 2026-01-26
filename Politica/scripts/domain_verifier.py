#!/usr/bin/env python3
"""
Verificador de disponibilidad de dominios
Usa whois para verificar si un dominio está disponible
"""

import subprocess
import re
import time
from typing import Dict, Optional, Tuple

class DomainVerifier:
    """Verificador de disponibilidad de dominios"""
    
    def __init__(self, rate_limit_delay=1.0):
        """
        Inicializa el verificador
        
        Args:
            rate_limit_delay: Segundos entre consultas para evitar rate limiting
        """
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
    
    def consultar_whois(self, dominio: str, servidor_whois: Optional[str] = None) -> Tuple[bool, str]:
        """
        Consulta whois para un dominio
        
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
    
    def analizar_disponibilidad(self, salida_whois: str, dominio: str) -> Dict[str, any]:
        """
        Analiza la salida de whois para determinar disponibilidad
        
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
            # Ambiguo o error
            estado = "desconocido"
        
        return {
            "dominio": dominio,
            "estado": estado,
            "disponible": estado == "disponible",
            "registrado": estado == "registrado",
            "info_adicional": info_adicional,
            "salida_raw": salida_whois[:500]  # Primeros 500 caracteres
        }
    
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
        
        # Verificar que whois esté instalado
        if not self.verificar_whois_instalado():
            return {
                "dominio": dominio,
                "estado": "error",
                "disponible": None,
                "error": "whois no está instalado",
                "instrucciones": self.instalar_whois_instrucciones()
            }
        
        # Consultar whois
        exito, salida = self.consultar_whois(dominio)
        
        if not exito:
            return {
                "dominio": dominio,
                "estado": "error",
                "disponible": None,
                "error": salida
            }
        
        # Analizar disponibilidad
        resultado = self.analizar_disponibilidad(salida, dominio)
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
    print("=" * 60)
    
    verifier = DomainVerifier(rate_limit_delay=2.0)
    
    # Verificar que whois esté instalado
    if not verifier.verificar_whois_instalado():
        print("\n❌ whois no está instalado en el sistema")
        print(verifier.instalar_whois_instrucciones())
        return
    
    print("\n✅ whois está instalado")
    
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
                for key, value in resultado['info_adicional'].items():
                    print(f"   {key}: {value}")
        elif resultado['estado'] == 'error':
            print(f"❌ Error: {resultado.get('error')}")
        
        print("-" * 60)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Generador de nombres convincentes para sitios de noticias
Crea nombres aleatorios realistas con verificación de disponibilidad
"""

import random
import string

# Componentes para nombres de sitios de noticias
PREFIJOS = [
    "El", "La", "Los", "Las", 
    "Diario", "Periódico", "Informativo",
    "Noticias", "Crónica", "Reporte"
]

NUCLEOS = [
    "Nacional", "Universal", "Global", "Regional",
    "Actual", "Digital", "Express", "Directo",
    "Informador", "Observador", "Monitor", "Radar",
    "Tiempo", "Momento", "Ahora", "Hoy",
    "Verdad", "Realidad", "Contexto", "Perspectiva",
    "Horizonte", "Visión", "Enfoque", "Mirada",
    "Tribuna", "Vocero", "Altavoz", "Pulso"
]

SUFIJOS = [
    "Noticias", "News", "Info", "Press",
    "Media", "Report", "Daily", "Times",
    "Post", "Journal", "Herald", "Gazette",
    "Tribune", "Chronicle", "Bulletin", "Wire"
]

# Modificadores adicionales
MODIFICADORES = [
    "24", "24/7", "Online", "Digital",
    "Live", "Plus", "Pro", "Prime",
    "First", "Total", "Integral", "Central"
]

# Países y regiones para sitios especializados
REGIONES = [
    "México", "MX", "Mexicano", "Azteca",
    "Latino", "Hispano", "Ibero", "América",
    "CDMX", "Bajío", "Norte", "Sur"
]

# Estilos de nombres
ESTILOS_NOMBRE = [
    "clasico",      # El Diario Nacional
    "moderno",      # NotiMX Digital
    "tecnico",      # InfoPress24
    "regional",     # El Mexicano Hoy
    "compuesto",    # DiarioNacionalMX
    "abreviado",    # DNM News
    "descriptivo",  # Noticias de México
    "innovador"     # MX360 Media
]

# TLDs comunes para noticias
TLDS = [
    "com", "mx", "com.mx", "news",
    "info", "net", "org", "media",
    "press", "online", "digital", "today"
]

class SiteNameGenerator:
    """Generador de nombres de sitios de noticias"""
    
    def __init__(self):
        self.nombres_generados = set()
    
    def generar_nombre_clasico(self):
        """Genera nombre estilo clásico: El Diario Nacional"""
        prefijo = random.choice(PREFIJOS)
        nucleo = random.choice(NUCLEOS)
        
        if random.random() > 0.7:
            sufijo = random.choice(SUFIJOS)
            return f"{prefijo} {nucleo} {sufijo}"
        
        return f"{prefijo} {nucleo}"
    
    def generar_nombre_moderno(self):
        """Genera nombre estilo moderno: NotiMX Digital"""
        base = random.choice(NUCLEOS)
        region = random.choice(REGIONES[:4])  # Abreviados
        modificador = random.choice(MODIFICADORES)
        
        opciones = [
            f"Noti{region} {modificador}",
            f"Info{region} {base}",
            f"{region}{base} {modificador}",
            f"{base}{region} Online"
        ]
        
        return random.choice(opciones)
    
    def generar_nombre_tecnico(self):
        """Genera nombre estilo técnico: InfoPress24"""
        prefijo = random.choice(["Info", "News", "Noti", "Press", "Media"])
        nucleo = random.choice(NUCLEOS[:8])
        modificador = random.choice(MODIFICADORES[:4])
        
        return f"{prefijo}{nucleo}{modificador}".replace(" ", "")
    
    def generar_nombre_regional(self):
        """Genera nombre con enfoque regional: El Mexicano Hoy"""
        articulo = random.choice(["El", "La", "Los"])
        region = random.choice(REGIONES)
        tiempo = random.choice(["Hoy", "Ahora", "Actual", "Digital"])
        
        opciones = [
            f"{articulo} {region} {tiempo}",
            f"Noticias {region} {tiempo}",
            f"{region} {tiempo}"
        ]
        
        return random.choice(opciones)
    
    def generar_nombre_compuesto(self):
        """Genera nombre compuesto: DiarioNacionalMX"""
        partes = [
            random.choice(PREFIJOS),
            random.choice(NUCLEOS),
            random.choice(REGIONES[:4])
        ]
        
        # Capitalizar primera letra de cada parte
        nombre = "".join([p.capitalize() for p in partes])
        return nombre
    
    def generar_nombre_abreviado(self):
        """Genera nombre con abreviatura: DNM News"""
        palabras = [
            random.choice(PREFIJOS),
            random.choice(NUCLEOS),
            random.choice(REGIONES[:4])
        ]
        
        # Crear iniciales
        iniciales = "".join([p[0].upper() for p in palabras])
        sufijo = random.choice(SUFIJOS)
        
        return f"{iniciales} {sufijo}"
    
    def generar_nombre_descriptivo(self):
        """Genera nombre descriptivo: Noticias de México"""
        base = random.choice(["Noticias", "Información", "Actualidad", "Reportes"])
        region = random.choice(REGIONES)
        
        opciones = [
            f"{base} de {region}",
            f"{base} {region}",
            f"{region} {base}"
        ]
        
        return random.choice(opciones)
    
    def generar_nombre_innovador(self):
        """Genera nombre innovador: MX360 Media"""
        region = random.choice(REGIONES[:4])
        numero = random.choice(["24", "360", "365", "7x24", "100"])
        tipo = random.choice(SUFIJOS)
        
        opciones = [
            f"{region}{numero} {tipo}",
            f"{numero}{region} {tipo}",
            f"{region} {numero}{tipo}"
        ]
        
        return random.choice(opciones).replace(" ", "")
    
    def generar_nombre(self, estilo=None):
        """
        Genera un nombre de sitio de noticias
        
        Args:
            estilo: Estilo específico o None para aleatorio
            
        Returns:
            str: Nombre del sitio generado
        """
        if not estilo:
            estilo = random.choice(ESTILOS_NOMBRE)
        
        generadores = {
            "clasico": self.generar_nombre_clasico,
            "moderno": self.generar_nombre_moderno,
            "tecnico": self.generar_nombre_tecnico,
            "regional": self.generar_nombre_regional,
            "compuesto": self.generar_nombre_compuesto,
            "abreviado": self.generar_nombre_abreviado,
            "descriptivo": self.generar_nombre_descriptivo,
            "innovador": self.generar_nombre_innovador
        }
        
        nombre = generadores[estilo]()
        
        # Evitar duplicados en esta sesión
        intentos = 0
        while nombre in self.nombres_generados and intentos < 10:
            nombre = generadores[estilo]()
            intentos += 1
        
        self.nombres_generados.add(nombre)
        return nombre
    
    def generar_tagline(self, nombre):
        """
        Genera un tagline apropiado para el nombre del sitio
        
        Args:
            nombre: Nombre del sitio
            
        Returns:
            str: Tagline generado
        """
        taglines_genericos = [
            "La Verdad en Cada Historia",
            "Tu Fuente de Información Confiable",
            "Noticias que Importan",
            "Mantente Informado",
            "Las Noticias más Recientes",
            "Periodismo de Calidad",
            "Rápido, Preciso, Confiable",
            "Información al Instante",
            "Noticias 24/7",
            "Tu Conexión con el Mundo",
            "Siempre Informado",
            "Actualidad en Tiempo Real",
            "Donde las Noticias Cobran Vida",
            "Información Que Transforma",
            "El Pulso de la Actualidad"
        ]
        
        # Taglines específicos según palabras clave
        if any(x in nombre.lower() for x in ["digital", "online", "24"]):
            taglines_especificos = [
                "Noticias 24 Horas al Día",
                "Información Digital en Tiempo Real",
                "Siempre Online, Siempre Actualizado",
                "La Nueva Era del Periodismo"
            ]
        elif any(x in nombre.lower() for x in ["méxico", "mx", "mexicano", "latino"]):
            taglines_especificos = [
                "La Voz de México",
                "Noticias desde el Corazón de México",
                "México en Primera Plana",
                "Información para Todos los Mexicanos"
            ]
        elif any(x in nombre.lower() for x in ["nacional", "país", "república"]):
            taglines_especificos = [
                "Información Nacional de Primera",
                "El Acontecer Nacional",
                "México Unido por la Información",
                "La Realidad Nacional"
            ]
        else:
            taglines_especificos = taglines_genericos
        
        # 70% específico, 30% genérico
        if random.random() > 0.3 and taglines_especificos != taglines_genericos:
            return random.choice(taglines_especificos)
        else:
            return random.choice(taglines_genericos)
    
    def generar_dominio(self, nombre):
        """
        Genera un nombre de dominio basado en el nombre del sitio
        
        Args:
            nombre: Nombre del sitio
            
        Returns:
            tuple: (nombre_dominio, tld)
        """
        # Limpiar nombre para dominio
        nombre_limpio = nombre.lower()
        
        # Remover artículos y palabras comunes
        articulos = ["el ", "la ", "los ", "las ", "de ", "del "]
        for articulo in articulos:
            nombre_limpio = nombre_limpio.replace(articulo, "")
        
        # Remover caracteres especiales
        nombre_limpio = nombre_limpio.replace(" ", "")
        nombre_limpio = "".join(c for c in nombre_limpio if c.isalnum())
        
        # Limitar longitud
        if len(nombre_limpio) > 20:
            # Intentar abreviar
            palabras = nombre.split()
            if len(palabras) > 2:
                nombre_limpio = "".join([p[0] for p in palabras]).lower()
            else:
                nombre_limpio = nombre_limpio[:20]
        
        # Seleccionar TLD apropiado
        tld = random.choice(TLDS)
        
        # Si el sitio es mexicano, preferir TLDs .mx
        if any(x in nombre.lower() for x in ["méxico", "mx", "mexicano"]):
            tld = random.choice(["mx", "com.mx", "com", "news"])
        
        return (nombre_limpio, tld)
    
    def generar_sitio_completo(self, estilo=None):
        """
        Genera información completa de un sitio
        
        Args:
            estilo: Estilo de nombre o None para aleatorio
            
        Returns:
            dict: Información completa del sitio
        """
        nombre = self.generar_nombre(estilo)
        tagline = self.generar_tagline(nombre)
        dominio, tld = self.generar_dominio(nombre)
        
        return {
            "nombre": nombre,
            "tagline": tagline,
            "dominio": dominio,
            "tld": tld,
            "dominio_completo": f"{dominio}.{tld}",
            "estilo": estilo or "aleatorio"
        }


def main():
    """Función de prueba"""
    print("🎨 Generador de Nombres de Sitios de Noticias")
    print("=" * 60)
    
    generator = SiteNameGenerator()
    
    print("\n📋 Generando 10 nombres de sitios de ejemplo:\n")
    
    for i, estilo in enumerate(ESTILOS_NOMBRE + ["aleatorio", "aleatorio"], 1):
        estilo_param = estilo if estilo != "aleatorio" else None
        sitio = generator.generar_sitio_completo(estilo_param)
        
        print(f"{i}. {sitio['nombre']}")
        print(f"   Tagline: {sitio['tagline']}")
        print(f"   Dominio: {sitio['dominio_completo']}")
        print(f"   Estilo: {sitio['estilo']}")
        print()


if __name__ == "__main__":
    main()

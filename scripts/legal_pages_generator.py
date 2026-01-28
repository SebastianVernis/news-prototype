#!/usr/bin/env python3
"""
Generador de Páginas Legales para Sitios de Noticias
Genera Términos y Condiciones, Política de Privacidad, FAQs y Secciones adicionales
"""

import random
from typing import Dict, List, Optional
from datetime import datetime


class LegalPagesGenerator:
    """Generador de contenido legal y páginas informativas"""
    
    # Nombres de autores ficticios para artículos
    AUTORES = [
        "Ana García López",
        "Carlos Mendoza",
        "María Elena Rodríguez",
        "José Luis Martínez",
        "Laura Patricia Hernández",
        "Roberto Sánchez",
        "Diana Torres",
        "Fernando Ramírez",
        "Gabriela Morales",
        "Eduardo Castro",
        "Sofía Jiménez",
        "Miguel Ángel Ruiz",
        "Valentina Cruz",
        "Alejandro Vargas",
        "Camila Reyes",
        "Diego Flores",
        "Isabella Gutiérrez",
        "Sebastián Ortiz",
        "Lucía Navarro",
        "Andrés Domínguez"
    ]
    
    def generar_autor_aleatorio(self) -> str:
        """Genera un nombre de autor aleatorio"""
        return random.choice(self.AUTORES)
    
    def generar_terminos_condiciones(self, site_name: str, domain: str) -> str:
        """
        Genera página de Términos y Condiciones
        
        Args:
            site_name: Nombre del sitio
            domain: Dominio del sitio
            
        Returns:
            str: HTML completo de Términos y Condiciones
        """
        year = datetime.now().year
        
        return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Términos y Condiciones - {site_name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <h1 class="logo"><a href="index.html">{site_name}</a></h1>
            <nav class="nav">
                <a href="index.html" class="nav-link">Inicio</a>
            </nav>
        </div>
    </header>
    
    <main class="legal-page">
        <div class="container">
            <div class="legal-content">
                <h1>Términos y Condiciones de Uso</h1>
                <p class="last-updated">Última actualización: {datetime.now().strftime('%d de %B de %Y')}</p>
                
                <section class="legal-section">
                    <h2>1. Aceptación de los Términos</h2>
                    <p>Al acceder y utilizar {site_name} ({domain}), usted acepta estar sujeto a estos Términos y Condiciones de Uso, todas las leyes y regulaciones aplicables, y acepta que es responsable del cumplimiento de todas las leyes locales aplicables.</p>
                    <p>Si no está de acuerdo con alguno de estos términos, tiene prohibido usar o acceder a este sitio.</p>
                </section>
                
                <section class="legal-section">
                    <h2>2. Uso del Servicio</h2>
                    <h3>2.1 Licencia de Uso</h3>
                    <p>Se le concede permiso para descargar temporalmente una copia de los materiales (información o software) en {site_name} solo para visualización transitoria personal y no comercial.</p>
                    
                    <h3>2.2 Restricciones</h3>
                    <p>Esta licencia no le permite:</p>
                    <ul>
                        <li>Modificar o copiar los materiales</li>
                        <li>Usar los materiales para cualquier propósito comercial o para exhibición pública</li>
                        <li>Intentar descompilar o realizar ingeniería inversa de cualquier software contenido en el sitio</li>
                        <li>Eliminar cualquier derecho de autor u otras notaciones de propiedad de los materiales</li>
                        <li>Transferir los materiales a otra persona o "reflejar" los materiales en cualquier otro servidor</li>
                    </ul>
                </section>
                
                <section class="legal-section">
                    <h2>3. Contenido del Usuario</h2>
                    <p>Ciertos contenidos del sitio pueden permitir que los usuarios publiquen comentarios, opiniones y otra información. {site_name} no filtra, edita, publica ni revisa los comentarios antes de su presencia en el sitio web.</p>
                    <p>Los comentarios no reflejan las opiniones de {site_name}, sus agentes o afiliados. Los comentarios reflejan las opiniones de la persona que publica.</p>
                </section>
                
                <section class="legal-section">
                    <h2>4. Propiedad Intelectual</h2>
                    <p>Todo el contenido incluido en este sitio, como texto, gráficos, logotipos, imágenes, clips de audio, descargas digitales y software, es propiedad de {site_name} o de sus proveedores de contenido y está protegido por las leyes de derechos de autor de México e internacionales.</p>
                </section>
                
                <section class="legal-section">
                    <h2>5. Limitación de Responsabilidad</h2>
                    <p>En ningún caso {site_name} o sus proveedores serán responsables de ningún daño (incluidos, sin limitación, daños por pérdida de datos o ganancias, o debido a la interrupción del negocio) que surja del uso o la imposibilidad de usar los materiales en {site_name}.</p>
                </section>
                
                <section class="legal-section">
                    <h2>6. Precisión de los Materiales</h2>
                    <p>Los materiales que aparecen en {site_name} pueden incluir errores técnicos, tipográficos o fotográficos. {site_name} no garantiza que ninguno de los materiales en su sitio web sea preciso, completo o actual.</p>
                    <p>{site_name} puede realizar cambios en los materiales contenidos en su sitio web en cualquier momento sin previo aviso.</p>
                </section>
                
                <section class="legal-section">
                    <h2>7. Enlaces</h2>
                    <p>{site_name} no ha revisado todos los sitios vinculados a su sitio web y no es responsable de los contenidos de ningún sitio vinculado. La inclusión de cualquier enlace no implica respaldo por parte de {site_name} del sitio.</p>
                </section>
                
                <section class="legal-section">
                    <h2>8. Modificaciones</h2>
                    <p>{site_name} puede revisar estos términos de servicio para su sitio web en cualquier momento sin previo aviso. Al usar este sitio web, usted acepta estar sujeto a la versión actual de estos términos de servicio.</p>
                </section>
                
                <section class="legal-section">
                    <h2>9. Ley Aplicable</h2>
                    <p>Estos términos y condiciones se rigen e interpretan de acuerdo con las leyes de México y usted se somete irrevocablemente a la jurisdicción exclusiva de los tribunales en esa ubicación.</p>
                </section>
                
                <section class="legal-section">
                    <h2>10. Contacto</h2>
                    <p>Si tiene preguntas sobre estos Términos y Condiciones, puede contactarnos en:</p>
                    <p><strong>Email:</strong> legal@{domain.replace('.com', '').replace('.mx', '').replace('.net', '')}.com<br>
                    <strong>Dirección:</strong> Ciudad de México, México</p>
                </section>
            </div>
        </div>
    </main>
    
    <footer class="footer">
        <div class="container">
            <p><a href="index.html">← Volver al inicio</a></p>
            <p>&copy; {year} {site_name}. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>"""
    
    def generar_politica_privacidad(self, site_name: str, domain: str) -> str:
        """
        Genera página de Política de Privacidad
        
        Args:
            site_name: Nombre del sitio
            domain: Dominio del sitio
            
        Returns:
            str: HTML completo de Política de Privacidad
        """
        year = datetime.now().year
        
        return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Política de Privacidad - {site_name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <h1 class="logo"><a href="index.html">{site_name}</a></h1>
            <nav class="nav">
                <a href="index.html" class="nav-link">Inicio</a>
            </nav>
        </div>
    </header>
    
    <main class="legal-page">
        <div class="container">
            <div class="legal-content">
                <h1>Política de Privacidad</h1>
                <p class="last-updated">Última actualización: {datetime.now().strftime('%d de %B de %Y')}</p>
                
                <section class="legal-section">
                    <h2>1. Introducción</h2>
                    <p>En {site_name}, accesible desde {domain}, una de nuestras principales prioridades es la privacidad de nuestros visitantes. Este documento de Política de Privacidad contiene tipos de información que se recopila y registra por {site_name} y cómo la usamos.</p>
                </section>
                
                <section class="legal-section">
                    <h2>2. Información que Recopilamos</h2>
                    <h3>2.1 Información Personal</h3>
                    <p>Podemos recopilar información personal que usted nos proporciona directamente, incluyendo:</p>
                    <ul>
                        <li>Nombre y apellidos</li>
                        <li>Dirección de correo electrónico</li>
                        <li>Número de teléfono</li>
                        <li>Comentarios y opiniones</li>
                    </ul>
                    
                    <h3>2.2 Información de Uso</h3>
                    <p>Recopilamos automáticamente cierta información cuando visita nuestro sitio, incluyendo:</p>
                    <ul>
                        <li>Dirección IP</li>
                        <li>Tipo de navegador</li>
                        <li>Páginas visitadas</li>
                        <li>Tiempo de permanencia</li>
                        <li>Dispositivo utilizado</li>
                    </ul>
                </section>
                
                <section class="legal-section">
                    <h2>3. Uso de la Información</h2>
                    <p>Utilizamos la información recopilada de las siguientes maneras:</p>
                    <ul>
                        <li>Proporcionar, operar y mantener nuestro sitio web</li>
                        <li>Mejorar, personalizar y ampliar nuestro sitio web</li>
                        <li>Entender y analizar cómo usa nuestro sitio web</li>
                        <li>Desarrollar nuevos productos, servicios, características y funcionalidades</li>
                        <li>Comunicarnos con usted para actualizaciones y promociones</li>
                        <li>Enviarle correos electrónicos</li>
                        <li>Encontrar y prevenir fraudes</li>
                    </ul>
                </section>
                
                <section class="legal-section">
                    <h2>4. Cookies y Tecnologías de Seguimiento</h2>
                    <p>Utilizamos cookies y tecnologías de seguimiento similares para rastrear la actividad en nuestro servicio y almacenar cierta información. Las cookies son archivos con una pequeña cantidad de datos que pueden incluir un identificador único anónimo.</p>
                    <p>Puede instruir a su navegador para que rechace todas las cookies o para que indique cuándo se envía una cookie. Sin embargo, si no acepta cookies, es posible que no pueda usar algunas partes de nuestro servicio.</p>
                </section>
                
                <section class="legal-section">
                    <h2>5. Compartir Información con Terceros</h2>
                    <p>No vendemos, comercializamos ni transferimos su información personal a terceros, excepto en los siguientes casos:</p>
                    <ul>
                        <li>Proveedores de servicios de confianza que nos ayudan a operar nuestro sitio web</li>
                        <li>Cuando la ley lo requiera</li>
                        <li>Para proteger nuestros derechos, propiedad o seguridad</li>
                    </ul>
                </section>
                
                <section class="legal-section">
                    <h2>6. Seguridad de los Datos</h2>
                    <p>La seguridad de su información personal es importante para nosotros. Implementamos medidas de seguridad diseñadas para proteger su información personal contra acceso no autorizado, alteración, divulgación o destrucción.</p>
                </section>
                
                <section class="legal-section">
                    <h2>7. Derechos del Usuario</h2>
                    <p>Usted tiene derecho a:</p>
                    <ul>
                        <li>Acceder a su información personal</li>
                        <li>Corregir información inexacta</li>
                        <li>Solicitar la eliminación de su información</li>
                        <li>Oponerse al procesamiento de sus datos</li>
                        <li>Solicitar la transferencia de sus datos</li>
                        <li>Retirar su consentimiento en cualquier momento</li>
                    </ul>
                </section>
                
                <section class="legal-section">
                    <h2>8. Privacidad de los Niños</h2>
                    <p>Nuestro servicio no está dirigido a menores de 13 años. No recopilamos conscientemente información personal identificable de niños menores de 13 años. Si descubrimos que un niño menor de 13 años nos ha proporcionado información personal, la eliminaremos de nuestros servidores.</p>
                </section>
                
                <section class="legal-section">
                    <h2>9. Cambios a esta Política</h2>
                    <p>Podemos actualizar nuestra Política de Privacidad de vez en cuando. Le notificaremos cualquier cambio publicando la nueva Política de Privacidad en esta página y actualizando la fecha de "Última actualización".</p>
                </section>
                
                <section class="legal-section">
                    <h2>10. Contacto</h2>
                    <p>Si tiene preguntas sobre esta Política de Privacidad, puede contactarnos:</p>
                    <p><strong>Email:</strong> privacidad@{domain.replace('.com', '').replace('.mx', '').replace('.net', '')}.com<br>
                    <strong>Teléfono:</strong> +52 55 1234 5678<br>
                    <strong>Dirección:</strong> Ciudad de México, México</p>
                </section>
            </div>
        </div>
    </main>
    
    <footer class="footer">
        <div class="container">
            <p><a href="index.html">← Volver al inicio</a></p>
            <p>&copy; {year} {site_name}. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>"""
    
    def generar_faqs(self, site_name: str) -> str:
        """
        Genera página de Preguntas Frecuentes
        
        Args:
            site_name: Nombre del sitio
            
        Returns:
            str: HTML completo de FAQs
        """
        year = datetime.now().year
        
        faqs = [
            {
                "pregunta": "¿Cómo puedo suscribirme al boletín de noticias?",
                "respuesta": f"Puede suscribirse a nuestro boletín ingresando su dirección de correo electrónico en el formulario de suscripción ubicado en la parte inferior de cualquier página o en la barra lateral de los artículos. Recibirá un correo de confirmación para validar su suscripción."
            },
            {
                "pregunta": "¿Con qué frecuencia se actualiza el contenido?",
                "respuesta": f"{site_name} se actualiza constantemente durante todo el día. Nuestro equipo de periodistas trabaja las 24 horas para mantenerle informado de las últimas noticias y acontecimientos."
            },
            {
                "pregunta": "¿Puedo compartir artículos en redes sociales?",
                "respuesta": "Sí, todos nuestros artículos pueden compartirse fácilmente en redes sociales utilizando los botones de compartir ubicados al final de cada artículo."
            },
            {
                "pregunta": "¿Cómo puedo contactar a la redacción?",
                "respuesta": f"Puede contactar a nuestro equipo editorial enviando un correo a redaccion@{site_name.lower().replace(' ', '')}.com o utilizando el formulario de contacto en nuestra página."
            },
            {
                "pregunta": "¿Tienen una aplicación móvil?",
                "respuesta": f"Actualmente, {site_name} está optimizado para navegación móvil a través de cualquier navegador web. Estamos trabajando en aplicaciones nativas para iOS y Android que estarán disponibles próximamente."
            },
            {
                "pregunta": "¿Cómo verifican la información de las noticias?",
                "respuesta": "Nuestro equipo editorial sigue estrictos estándares periodísticos. Todas las noticias son verificadas con múltiples fuentes antes de su publicación y se citan las fuentes originales cuando es aplicable."
            },
            {
                "pregunta": "¿Puedo cancelar mi suscripción al boletín?",
                "respuesta": "Sí, puede darse de baja en cualquier momento haciendo clic en el enlace 'Cancelar suscripción' que aparece al final de cada correo electrónico que le enviamos."
            },
            {
                "pregunta": "¿Ofrecen contenido en otros idiomas?",
                "respuesta": "Actualmente nuestro contenido está disponible en español. Estamos considerando expandir a otros idiomas en el futuro."
            },
            {
                "pregunta": "¿Cómo reporto un error en un artículo?",
                "respuesta": f"Si encuentra un error en alguno de nuestros artículos, por favor contáctenos inmediatamente a correcciones@{site_name.lower().replace(' ', '')}.com con el enlace del artículo y la descripción del error."
            },
            {
                "pregunta": "¿Aceptan contribuciones de periodistas externos?",
                "respuesta": f"Sí, {site_name} acepta artículos de colaboradores externos. Si está interesado en contribuir, envíe su propuesta a colaboraciones@{site_name.lower().replace(' ', '')}.com."
            }
        ]
        
        faqs_html = []
        for i, faq in enumerate(faqs, 1):
            faqs_html.append(f"""
                <div class="faq-item">
                    <h3 class="faq-question">{i}. {faq['pregunta']}</h3>
                    <p class="faq-answer">{faq['respuesta']}</p>
                </div>""")
        
        return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preguntas Frecuentes - {site_name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <h1 class="logo"><a href="index.html">{site_name}</a></h1>
            <nav class="nav">
                <a href="index.html" class="nav-link">Inicio</a>
            </nav>
        </div>
    </header>
    
    <main class="legal-page faq-page">
        <div class="container">
            <div class="legal-content">
                <h1>Preguntas Frecuentes</h1>
                <p class="page-intro">Encuentra respuestas a las preguntas más comunes sobre {site_name}.</p>
                
                <div class="faq-list">
{''.join(faqs_html)}
                </div>
            </div>
        </div>
    </main>
    
    <footer class="footer">
        <div class="container">
            <p><a href="index.html">← Volver al inicio</a></p>
            <p>&copy; {year} {site_name}. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>"""
    
    def generar_acerca_de(self, site_name: str, tagline: str, domain: str) -> str:
        """
        Genera página Acerca de Nosotros
        
        Args:
            site_name: Nombre del sitio
            tagline: Tagline del sitio
            domain: Dominio del sitio
            
        Returns:
            str: HTML completo de Acerca de
        """
        year = datetime.now().year
        
        return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acerca de Nosotros - {site_name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <h1 class="logo"><a href="index.html">{site_name}</a></h1>
            <nav class="nav">
                <a href="index.html" class="nav-link">Inicio</a>
            </nav>
        </div>
    </header>
    
    <main class="legal-page about-page">
        <div class="container">
            <div class="legal-content">
                <h1>Acerca de {site_name}</h1>
                <p class="tagline-large">{tagline}</p>
                
                <section class="legal-section">
                    <h2>Nuestra Misión</h2>
                    <p>{site_name} nació con el objetivo de proporcionar información confiable, precisa y oportuna a lectores de habla hispana en todo el mundo. Nos comprometemos a mantener los más altos estándares de periodismo y ética editorial.</p>
                    <p>Creemos que el acceso a información de calidad es fundamental para una sociedad informada y democrática. Por eso, trabajamos incansablemente para ofrecerte las noticias más relevantes del momento.</p>
                </section>
                
                <section class="legal-section">
                    <h2>Nuestros Valores</h2>
                    <ul class="values-list">
                        <li><strong>Veracidad:</strong> Verificamos todas nuestras fuentes y nos comprometemos con la precisión.</li>
                        <li><strong>Independencia:</strong> Mantenemos independencia editorial en todas nuestras publicaciones.</li>
                        <li><strong>Transparencia:</strong> Somos claros sobre nuestras fuentes y métodos de investigación.</li>
                        <li><strong>Imparcialidad:</strong> Presentamos múltiples perspectivas en temas controversiales.</li>
                        <li><strong>Integridad:</strong> Seguimos códigos éticos estrictos en todo nuestro trabajo.</li>
                    </ul>
                </section>
                
                <section class="legal-section">
                    <h2>Nuestro Equipo</h2>
                    <p>Contamos con un equipo diverso de periodistas, editores, diseñadores y desarrolladores apasionados por contar historias que importan. Nuestros profesionales tienen experiencia en medios nacionales e internacionales.</p>
                </section>
                
                <section class="legal-section">
                    <h2>Cobertura</h2>
                    <p>Cubrimos una amplia gama de temas incluyendo:</p>
                    <ul>
                        <li>Política nacional e internacional</li>
                        <li>Economía y negocios</li>
                        <li>Tecnología e innovación</li>
                        <li>Deportes</li>
                        <li>Entretenimiento y cultura</li>
                        <li>Ciencia y salud</li>
                    </ul>
                </section>
                
                <section class="legal-section">
                    <h2>Contacto</h2>
                    <p>Nos encantaría saber de ti. Puedes contactarnos en:</p>
                    <p><strong>Email general:</strong> contacto@{domain.replace('.com', '').replace('.mx', '').replace('.net', '')}.com<br>
                    <strong>Redacción:</strong> redaccion@{domain.replace('.com', '').replace('.mx', '').replace('.net', '')}.com<br>
                    <strong>Publicidad:</strong> publicidad@{domain.replace('.com', '').replace('.mx', '').replace('.net', '')}.com<br>
                    <strong>Teléfono:</strong> +52 55 1234 5678<br>
                    <strong>Dirección:</strong> Ciudad de México, México</p>
                </section>
            </div>
        </div>
    </main>
    
    <footer class="footer">
        <div class="container">
            <p><a href="index.html">← Volver al inicio</a></p>
            <p>&copy; {year} {site_name}. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>"""


def main():
    """Función de prueba"""
    print("📄 Generador de Páginas Legales")
    print("=" * 60)
    
    generator = LegalPagesGenerator()
    
    # Ejemplo de uso
    site_name = "Noticias Ejemplo"
    domain = "noticiasejemplo.com"
    
    print(f"\n✅ Generando Términos y Condiciones...")
    terms = generator.generar_terminos_condiciones(site_name, domain)
    print(f"   Generado: {len(terms)} caracteres")
    
    print(f"\n✅ Generando Política de Privacidad...")
    privacy = generator.generar_politica_privacidad(site_name, domain)
    print(f"   Generado: {len(privacy)} caracteres")
    
    print(f"\n✅ Generando FAQs...")
    faqs = generator.generar_faqs(site_name)
    print(f"   Generado: {len(faqs)} caracteres")
    
    print(f"\n✅ Generando Acerca de...")
    about = generator.generar_acerca_de(site_name, "Tu fuente de noticias confiables", domain)
    print(f"   Generado: {len(about)} caracteres")
    
    print(f"\n✅ Autor aleatorio generado: {generator.generar_autor_aleatorio()}")
    
    print("\n" + "=" * 60)
    print("✅ Generación de páginas legales completada")


if __name__ == "__main__":
    main()

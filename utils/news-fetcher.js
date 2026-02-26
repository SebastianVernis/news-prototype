// utils/news-fetcher.js
// Script to fetch new news and add them to the site

// Function to fetch news from an external API (simulated)
async function fetchNewsFromExternalAPI() {
  // In a real implementation, you would fetch from an actual news API
  // For this example, we'll return simulated news data
  return [
    {
      title: "Descubren nueva especie de mariposa en selva tropical",
      slug: "descubren-nueva-especie-mariposa-selva",
      content: "Científicos del Instituto de Biología de la UNAM han descubierto una nueva especie de mariposa en la selva Lacandona. La nueva especie, bautizada como Morpho aurora, destaca por sus colores azules intensos con reflejos dorados. El hallazgo fue resultado de un proyecto de investigación de tres años que busca documentar la biodiversidad de la región. Los expertos señalan que esta especie juega un papel crucial en la polinización de varias plantas endémicas de la zona.",
      excerpt: "Científicos del Instituto de Biología de la UNAM han descubierto una nueva especie de mariposa en la selva Lacandona...",
      category: "ciencia",
      author: "Dr. Miguel Torres",
      publishedAt: new Date().toISOString(),
      imageUrl: "https://placehold.co/800x450/4facfe/ffffff?text=Mariposa+Nueva",
      featured: false,
      views: 0,
      tags: ["ciencia", "biodiversidad", "mariposa", "selva"]
    },
    {
      title: "Inauguran primera planta solar flotante en presa de Chiapas",
      slug: "inauguran-planta-solar-flotante-chiapas",
      content: "Este martes se inauguró la primera planta solar flotante de México en la presa Miguel Alemán, en Chiapas. El proyecto, que representa una inversión de 150 millones de pesos, generará energía limpia para abastecer a más de 25,000 hogares. La tecnología flotante permite un mayor aprovechamiento del recurso solar al tiempo que reduce la evaporación del agua. Autoridades destacaron que este modelo podría replicarse en otras presas del país.",
      excerpt: "Se inauguró la primera planta solar flotante de México en la presa Miguel Alemán, en Chiapas...",
      category: "tecnologia",
      author: "Laura Jiménez",
      publishedAt: new Date().toISOString(),
      imageUrl: "https://placehold.co/800x450/00dbde/ffffff?text=Solar+Flotante",
      featured: false,
      views: 0,
      tags: ["tecnología", "energía", "solar", "Chiapas"]
    },
    {
      title: "Joven mexicana gana medalla de oro en Olimpiada Internacional de Matemáticas",
      slug: "joven-mexicana-oro-olimpiada-matematicas",
      content: "Ana Sofía Ramírez, estudiante de 17 años de la Universidad Nacional Autónoma de México, obtuvo la medalla de oro en la Olimpiada Internacional de Matemáticas celebrada en París. Su solución innovadora a un problema de teoría de números fue elogiada por el jurado internacional. Esta es la segunda medalla de oro para México en los últimos cinco años. Ana Sofía expresó su entusiasmo por seguir estudiando matemáticas puras y eventualmente contribuir a la investigación científica del país.",
      excerpt: "Ana Sofía Ramírez, estudiante de 17 años, obtuvo la medalla de oro en la Olimpiada Internacional de Matemáticas...",
      category: "educacion",
      author: "José Hernández",
      publishedAt: new Date().toISOString(),
      imageUrl: "https://placehold.co/800x450/f093fb/ffffff?text=Oro+Matemáticas",
      featured: false,
      views: 0,
      tags: ["educación", "matemáticas", "jóvenes", "premios"]
    },
    {
      title: "Inician pruebas clínicas de nueva vacuna contra tuberculosis",
      slug: "inician-pruebas-vacuna-tuberculosis",
      content: "El Instituto Nacional de Enfermedades Respiratorias (INER) dio inicio a las pruebas clínicas fase III de una nueva vacuna contra la tuberculosis. El ensayo involucra a 15,000 participantes en siete estados del país. La vacuna, desarrollada íntegramente por investigadores mexicanos, promete ser más efectiva que la BCG tradicional, especialmente en adultos. Si los resultados son positivos, la vacuna podría estar disponible para la población general en 2027.",
      excerpt: "El INER dio inicio a las pruebas clínicas fase III de una nueva vacuna contra la tuberculosis...",
      category: "salud",
      author: "Dra. Carmen Vázquez",
      publishedAt: new Date().toISOString(),
      imageUrl: "https://placehold.co/800x450/4facfe/ffffff?text=Vacuna+TBC",
      featured: false,
      views: 0,
      tags: ["salud", "vacunas", "investigación", "tuberculosis"]
    },
    {
      title: "Arqueólogos descubren tumba maya con jeroglíficos inéditos",
      slug: "arqueologos-descubren-tumba-maya-jeroglificos",
      content: "Un equipo de arqueólogos del INAH ha descubierto una tumba maya del periodo Clásico en las cercanías de Palenque, Chiapas. La cripta contiene jeroglíficos que aún no han sido descifrados completamente, pero que podrían revelar información sobre un gobernante desconocido. El hallazgo incluye cerámica, jade y otros objetos que datan del siglo VII d.C. Los expertos consideran que este descubrimiento podría cambiar la comprensión actual sobre la organización política de los antiguos mayas.",
      excerpt: "Arqueólogos del INAH han descubierto una tumba maya del periodo Clásico en las cercanías de Palenque...",
      category: "cultura",
      author: "Dr. Raúl Méndez",
      publishedAt: new Date().toISOString(),
      imageUrl: "https://placehold.co/800x450/764ba2/ffffff?text=Tumba+Maya",
      featured: false,
      views: 0,
      tags: ["cultura", "arqueología", "mayas", "história"]
    },
    {
      title: "Inauguran primer corredor turístico binacional México-Guatemala",
      slug: "inauguran-corredor-turistico-mexico-guatemala",
      content: "Este lunes se inauguró oficialmente el primer corredor turístico binacional entre México y Guatemala, que conecta sitios arqueológicos y áreas naturales protegidas en ambos países. El proyecto, resultado de un acuerdo firmado en 2024, busca incrementar el flujo turístico y generar empleo en comunidades fronterizas. El corredor incluye Tikal, Yaxha y Bonampak, entre otros destinos. Autoridades estiman que el proyecto generará más de 10,000 empleos directos en los próximos cinco años.",
      excerpt: "Se inauguró el primer corredor turístico binacional entre México y Guatemala...",
      category: "nacional",
      author: "Patricia Rojas",
      publishedAt: new Date().toISOString(),
      imageUrl: "https://placehold.co/800x450/667eea/ffffff?text=Corredor+Turístico",
      featured: false,
      views: 0,
      tags: ["turismo", "México", "Guatemala", "cooperación"]
    },
    {
      title: "Presentan robots autónomos para limpieza de playas contaminadas",
      slug: "presentan-robots-autonomos-limpieza-playas",
      content: "Investigadores del CICESE presentaron una flota de robots autónomos diseñados específicamente para la limpieza de playas contaminadas con plástico y otros residuos. Los robots pueden operar durante 12 horas continuas recolectando microplásticos y desechos orgánicos. El proyecto piloto se implementará en las playas de Ensenada y Puerto Peñasco. Los desarrolladores afirman que cada robot puede recolectar hasta 50 kilogramos de basura diariamente, lo que equivale al trabajo de 5 personas.",
      excerpt: "Investigadores presentaron robots autónomos diseñados para la limpieza de playas contaminadas...",
      category: "tecnologia",
      author: "Ing. David López",
      publishedAt: new Date().toISOString(),
      imageUrl: "https://placehold.co/800x450/00dbde/ffffff?text=Robot+Playa",
      featured: false,
      views: 0,
      tags: ["tecnología", "robot", "playas", "contaminación"]
    },
    {
      title: "Firma mexicana desarrolla bioplástico a partir de cáscaras de camarón",
      slug: "empresa-desarrolla-bioplastico-cascara-camaron",
      content: "Una empresa emergente de Guadalajara ha desarrollado un bioplástico biodegradable a partir de quitina extraída de cáscaras de camarón. El material, que tarda solo 6 meses en degradarse, podría sustituir al plástico convencional en diversos usos. El proceso industrial ya ha sido patentado y se encuentra en etapa de producción piloto. La startup espera iniciar la comercialización en 2026, con proyecciones de ventas por 50 millones de pesos en el primer año.",
      excerpt: "Empresa desarrolla bioplástico biodegradable a partir de quitina extraída de cáscaras de camarón...",
      category: "ciencia",
      author: "Dra. Elena Serrano",
      publishedAt: new Date().toISOString(),
      imageUrl: "https://placehold.co/800x450/4facfe/ffffff?text=Bioplástico",
      featured: false,
      views: 0,
      tags: ["ciencia", "bioplástico", "sustentabilidad", "innovación"]
    },
    {
      title: "Inauguran centro de investigación para cultivo de alimentos en Marte",
      slug: "inauguran-centro-investigacion-alimentos-marte",
      content: "La Agencia Espacial Mexicana inauguró el Centro de Investigación para Alimentación en Condiciones Extremas, dedicado al desarrollo de técnicas para cultivar alimentos en Marte. El centro, ubicado en Chihuahua, recrea condiciones similares a las del planeta rojo para probar diferentes cultivos. Los primeros experimentos se centran en tomate, patata y algas comestibles. El proyecto es resultado de una colaboración con universidades de Estados Unidos y Japón, y representa una inversión de 200 millones de pesos.",
      excerpt: "Se inauguró el Centro de Investigación para Alimentación en Condiciones Extremas...",
      category: "ciencia",
      author: "Dr. Francisco Morales",
      publishedAt: new Date().toISOString(),
      imageUrl: "https://placehold.co/800x450/764ba2/ffffff?text=Marte+Alimentos",
      featured: false,
      views: 0,
      tags: ["ciencia", "espacio", "alimentos", "Marte"]
    }
  ];
}

module.exports = { fetchNewsFromExternalAPI };
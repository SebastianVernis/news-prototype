// Cloudflare Worker para Cron Jobs de Publicación de Noticias
// Publica 1 noticia por hora automáticamente

export default {
  async scheduled(event, env, ctx) {
    console.log('⏰ Cron job ejecutado:', event.scheduledTime);
    
    try {
      // Verificar si es hora de publicar (cada hora)
      const now = new Date();
      const hour = now.getUTCHours();
      
      // Publicar en el minuto 0 de cada hora
      if (now.getUTCMinutes() === 0) {
        console.log('📰 Publicando noticia programada...');
        
        // Hacer fetch al endpoint de publicación
        const response = await fetch('https://noticias-hoy.pages.dev/api/publish', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${env.PUBLISHER_TOKEN}`,
            'Content-Type': 'application/json'
          }
        });
        
        const result = await response.json();
        
        console.log('✅ Resultado:', result);
        
        return new Response(JSON.stringify({
          success: true,
          message: 'Noticia publicada',
          result: result
        }), {
          headers: { 'Content-Type': 'application/json' }
        });
      }
      
      return new Response(JSON.stringify({
        success: true,
        message: 'Esperando siguiente hora'
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
      
    } catch (error) {
      console.error('❌ Error en cron job:', error);
      
      return new Response(JSON.stringify({
        success: false,
        error: error.message
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  }
};
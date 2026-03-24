import { handleArticleRequest } from '../../_shared/article-middleware.js';

export async function onRequest(context) {
  const { pathname } = new URL(context.request.url);
  
  // Only process /articulo/* routes
  if (!pathname.startsWith('/articulo')) {
    return await context.next();
  }
  
  return handleArticleRequest(context, 'puntonoticias');
}

import { handleArticleRequest } from '../../_shared/article-middleware.js';

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const { pathname } = url;
  
  console.log('[Middleware] Request:', {
    url: url.toString(),
    pathname,
    host: url.host,
    slug: url.searchParams.get('slug')
  });
  
  if (!pathname.startsWith('/articulo')) {
    return await context.next();
  }
  
  console.log('[Middleware] Processing article request for:', url.searchParams.get('slug'));
  return handleArticleRequest(context, 'pulsodiario');
}

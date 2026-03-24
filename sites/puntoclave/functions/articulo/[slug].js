import { handleArticleRequest } from '../../../_shared/article-middleware.js';

export async function onRequest(context) {
  const { params } = context;
  const slug = params.slug;
  
  const url = new URL(context.request.url);
  url.searchParams.set('slug', slug);
  
  const modifiedRequest = new Request(url, {
    method: context.request.method,
    headers: context.request.headers,
    body: context.request.body
  });
  
  const modifiedContext = {
    ...context,
    request: modifiedRequest
  };
  
  return handleArticleRequest(modifiedContext, 'puntoclave');
}

import { handleArticleRequest } from '../../../_shared/article-middleware.js';

export async function onRequest(context) {
  return handleArticleRequest(context, 'radioabc');
}

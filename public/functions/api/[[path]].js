export async function onRequest(context) {
  const { request } = context;
  const apiUrl = new URL(request.url);
  apiUrl.hostname = 'news-api.sebastianvernis.workers.dev';
  apiUrl.protocol = 'https:';
  
  const newRequest = new Request(apiUrl, {
    method: request.method,
    headers: request.headers,
    body: request.body,
  });
  
  try {
    const response = await fetch(newRequest);
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: response.headers
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

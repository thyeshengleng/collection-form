addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  // Configure CORS headers
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Credentials': 'true'
  }

  // Handle OPTIONS request for CORS preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: corsHeaders
    })
  }

  // Serve the static HTML for the root path
  if (new URL(request.url).pathname === '/') {
    // Check if user is authenticated
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
      return Response.redirect('https://collection-form.streamlit.app/login', 302);
    }

    return new Response(`
      <!DOCTYPE html>
      <html>
      <head>
          <title>Collection Action List</title>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <script>
              // Include auth token in redirect
              const authToken = '${authHeader.split(' ')[1]}';
              window.location.href = 'https://collection-form.streamlit.app?token=' + authToken;
          </script>
      </head>
      <body style="font-family: Arial, sans-serif; text-align: center; padding-top: 50px;">
          <h1>Collection Action List</h1>
          <p>Loading application...</p>
      </body>
      </html>
    `, {
      headers: {
        'Content-Type': 'text/html',
        ...corsHeaders
      }
    })
  }

  // Handle API requests
  try {
    const url = new URL(request.url)
    const path = url.pathname

    // Add your API endpoints here
    if (path.startsWith('/api/')) {
      // Handle different API routes
      const response = await handleApiRequest(request)
      return new Response(JSON.stringify(response), {
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders
        }
      })
    }

    // Return 404 for unknown paths
    return new Response('Not Found', {
      status: 404,
      headers: corsHeaders
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        ...corsHeaders
      }
    })
  }
}

async function handleApiRequest(request) {
  // Implement your API logic here
  return { message: 'API endpoint ready' }
}
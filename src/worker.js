export default {
  async fetch(request, env) {
    try {
      const url = new URL(request.url);
      
      // Handle form data storage using KV
      if (url.pathname === '/api/form') {
        const corsHeaders = {
          'Access-Control-Allow-Origin': '*',  // Allow all origins for now
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        };

        // Handle OPTIONS request
        if (request.method === 'OPTIONS') {
          return new Response(null, { headers: corsHeaders });
        }

        // Make sure FORM_DATA is available
        if (!env.FORM_DATA) {
          throw new Error('KV namespace FORM_DATA not found');
        }

        if (request.method === 'POST') {
          const formData = await request.json();
          await env.FORM_DATA.put('collection_records', JSON.stringify(formData));
          return new Response('Data saved successfully', { 
            status: 200,
            headers: corsHeaders
          });
        } 
        
        if (request.method === 'GET') {
          const data = await env.FORM_DATA.get('collection_records');
          return new Response(data || '[]', {
            headers: {
              ...corsHeaders,
              'Content-Type': 'application/json'
            }
          });
        }
      }

      // Return the HTML page for other routes
      return new Response(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Collection Action List</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <script>
                window.location.href = 'https://share.streamlit.io/thyeshengleng/collection-form/main/app.py';
            </script>
        </head>
        <body>
            <h1>Collection Action List</h1>
            <p>Loading application...</p>
        </body>
        </html>
      `, {
        headers: { 'Content-Type': 'text/html' }
      });

    } catch (e) {
      return new Response(`Error: ${e.message}`, { 
        status: 500,
        headers: { 'Content-Type': 'text/plain' }
      });
    }
  }
}; 
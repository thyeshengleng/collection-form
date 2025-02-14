export default {
  async fetch(request, env) {
    try {
      const url = new URL(request.url);
      
      // Handle form data storage using KV
      if (url.pathname === '/api/form') {
        const corsHeaders = {
          'Access-Control-Allow-Origin': 'https://share.streamlit.io',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Allow-Credentials': 'true'
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

      // Redirect to Streamlit
      return Response.redirect('https://share.streamlit.io/thyeshengleng/collection-form/main/app.py', 301);

    } catch (e) {
      return new Response(`Error: ${e.message}`, { 
        status: 500,
        headers: { 'Content-Type': 'text/plain' }
      });
    }
  }
}; 
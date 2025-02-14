// Update this URL to your actual Streamlit app URL
return new Response(`
  <!DOCTYPE html>
  <html>
  <head>
      <title>Collection Action List</title>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <script>
          window.location.href = 'https://collection-form.streamlit.app';
      </script>
  </head>
  <body style="font-family: Arial, sans-serif; text-align: center; padding-top: 50px;">
      <h1>Collection Action List</h1>
      <p>Loading application...</p>
  </body>
  </html>
`, {
  headers: { 'Content-Type': 'text/html' }
}); 
import streamlit.components.v1 as components
import streamlit as st
from src.shared.helpers import DEV_MODE

swagger_url = "http://localhost:8000/openapi.json"

swagger_html = f"""
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui.css">
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui-bundle.js"></script>
    <style>
      #swagger-ui {{
        background-color: #f0f0f0;  /* Background color */
        padding: 20px;
        border-radius: 8px;
        height: 100%;  /* Allow it to expand vertically */
        overflow: auto;  /* Make it scrollable if content overflows */
      }}
      body {{
        margin: 0;
      }}
    </style>
    <script>
      window.onload = function() {{
        const ui = SwaggerUIBundle({{
          url: '{swagger_url}',
          dom_id: '#swagger-ui',
          deepLinking: true,
          presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIBundle.SwaggerUIStandalonePreset
          ],
          layout: "BaseLayout",
        }});
      }};
    </script>
  </head>
  <body>
    <div id="swagger-ui"></div>
  </body>
</html>
"""

if DEV_MODE:
    docs_url = 'http://localhost:8000/docs'
    st.link_button('Documentación API', docs_url)

components.html(swagger_html, height=900, scrolling=True)

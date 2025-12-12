FROM node:20-slim

WORKDIR /app

# Instalar el servidor oficial de Notion MCP
RUN npm install -g @notionhq/notion-mcp-server

# El servidor se ejecuta con stdio por defecto
ENTRYPOINT ["notion-mcp-server"]
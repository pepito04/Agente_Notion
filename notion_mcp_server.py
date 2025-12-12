#!/usr/bin/env python3
"""
Servidor MCP para Notion - Comunica vía stdio con el cliente
"""

import os
import sys
import json
from typing import Any
from notion_client import Client

# Configurar token
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
if not NOTION_TOKEN:
    raise ValueError("NOTION_TOKEN no está configurado")

notion = Client(auth=NOTION_TOKEN)

class NotionMCPServer:
    """Servidor MCP simple para Notion"""
    
    def __init__(self):
        self.tools = {
            "search": self.search_pages,
            "get_page": self.get_page,
            "create_page": self.create_page,
            "update_page": self.update_page,
            "list_databases": self.list_databases,
        }
    
    def search_pages(self, query: str) -> dict:
        """Busca páginas en Notion"""
        try:
            response = notion.search(
                query=query,
                filter={"property": "object", "value": "page"}
            )
            return {
                "success": True,
                "results": [
                    {
                        "id": page["id"],
                        "title": page.get("properties", {}).get("title", {}).get("title", [{}])[0].get("plain_text", "Sin título"),
                        "url": page.get("url", "")
                    }
                    for page in response.get("results", [])
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_page(self, page_id: str) -> dict:
        """Obtiene contenido de una página"""
        try:
            # Remover guiones del ID
            page_id_clean = page_id.replace("-", "")
            
            page = notion.pages.retrieve(page_id_clean)
            blocks = notion.blocks.children.list(page_id_clean)
            
            content = []
            for block in blocks.get("results", []):
                block_type = block.get("type")
                content.append({
                    "type": block_type,
                    "content": block.get(block_type, {})
                })
            
            return {
                "success": True,
                "page_id": page_id,
                "title": page.get("properties", {}).get("title", {}).get("title", [{}])[0].get("plain_text", "Sin título"),
                "content_blocks": content
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_page(self, parent_id: str, title: str, content: str = "") -> dict:
        """Crea una página nueva"""
        try:
            parent_id_clean = parent_id.replace("-", "")
            
            page = notion.pages.create(
                parent={"page_id": parent_id_clean},
                properties={
                    "title": {
                        "title": [{"text": {"content": title}}]
                    }
                }
            )
            
            # Agregar contenido si existe
            if content:
                notion.blocks.children.append(
                    block_id=page["id"],
                    children=[
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [
                                    {"type": "text", "text": {"content": content}}
                                ]
                            }
                        }
                    ]
                )
            
            return {
                "success": True,
                "page_id": page["id"],
                "title": title,
                "url": page.get("url", "")
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_page(self, page_id: str, title: str = None) -> dict:
        """Actualiza una página"""
        try:
            page_id_clean = page_id.replace("-", "")
            
            properties = {}
            if title:
                properties["title"] = {
                    "title": [{"text": {"content": title}}]
                }
            
            if not properties:
                return {"success": False, "error": "No hay propiedades para actualizar"}
            
            notion.pages.update(page_id_clean, properties=properties)
            
            return {"success": True, "page_id": page_id, "updated_title": title}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_databases(self) -> dict:
        """Lista bases de datos compartidas"""
        try:
            response = notion.search(
                filter={"property": "object", "value": "database"}
            )
            
            databases = [
                {
                    "id": db["id"],
                    "title": db.get("title", [{}])[0].get("plain_text", "Sin título") if db.get("title") else "Sin título",
                    "url": db.get("url", "")
                }
                for db in response.get("results", [])
            ]
            
            return {"success": True, "databases": databases}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def process_request(self, request: dict) -> dict:
        """Procesa una solicitud MCP"""
        tool_name = request.get("method")
        params = request.get("params", {})
        
        if tool_name not in self.tools:
            return {"error": f"Herramienta no encontrada: {tool_name}"}
        
        tool = self.tools[tool_name]
        return tool(**params)
    
    def run(self):
        """Loop principal del servidor"""
        print("✅ Servidor MCP Notion iniciado", file=sys.stderr)
        
        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                
                request = json.loads(line)
                response = self.process_request(request)
                print(json.dumps(response))
                sys.stdout.flush()
        
        except KeyboardInterrupt:
            print("⏹️ Servidor detenido", file=sys.stderr)
        except Exception as e:
            print(f"❌ Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    server = NotionMCPServer()
    server.run()
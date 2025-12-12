import os
import json
import subprocess
import time
from dotenv import load_dotenv
from langchain.tools import tool
from notion_client import Client

load_dotenv()

# Token de Notion
NOTION_TOKEN = os.getenv("NOTION_TOKEN")

# Cliente directo de Notion (para búsquedas rápidas)
notion_client = None
if NOTION_TOKEN:
    try:
        notion_client = Client(auth=NOTION_TOKEN)
        print("✅ Cliente de Notion inicializado")
    except Exception as e:
        print(f"⚠️ Error: {e}")

# Cache para bases de datos y páginas
_databases_cache = None
_pages_cache = None

def get_databases():
    """Obtiene y cachea las bases de datos disponibles"""
    global _databases_cache
    
    if _databases_cache is not None:
        return _databases_cache
    
    if not notion_client:
        return []
    
    try:
        response = notion_client.search(
            filter={"property": "object", "value": "data_source"}
        )
        _databases_cache = response.get("results", [])
        return _databases_cache
    except Exception as e:
        print(f"Error obteniendo bases de datos: {e}")
        return []

def get_first_parent_id():
    """Obtiene el ID de la primera base de datos o página disponible"""
    # Primero intentar obtener una base de datos
    databases = get_databases()
    if databases:
        return databases[0]["id"]
    
    # Si no hay bases de datos, obtener la primera página
    if not notion_client:
        return None
    
    try:
        response = notion_client.search()
        results = response.get("results", [])
        for item in results:
            if item.get("id"):
                return item["id"]
    except Exception as e:
        print(f"Error obteniendo páginas: {e}")
    
    return None

def find_database_by_name(name: str):
    """Busca una base de datos por nombre"""
    databases = get_databases()
    for db in databases:
        title = "Sin título"
        if db.get("title"):
            title = db["title"][0].get("plain_text", "Sin título")
        
        if name.lower() in title.lower():
            return db
    return None

def find_page_by_title(title: str):
    """Busca una página por título"""
    if not notion_client:
        return None
    
    try:
        response = notion_client.search(
            query=title,
            filter={"property": "object", "value": "page"}
        )
        
        results = response.get("results", [])
        for page in results:
            props = page.get("properties", {})
            page_title = "Sin título"
            
            for prop_name, prop_value in props.items():
                if prop_value.get("type") == "title":
                    rich_text = prop_value.get("title", [])
                    if rich_text:
                        page_title = rich_text[0].get("plain_text", "Sin título")
                    break
            
            if title.lower() == page_title.lower():
                return page
        
        # Si no hay coincidencia exacta, retornar el primero
        if results:
            return results[0]
    
    except Exception as e:
        print(f"Error buscando página: {e}")
    
    return None

# ============================================
# HERRAMIENTAS LANGCHAIN
# ============================================

@tool
def search_notion(query: str) -> str:
    """
    Busca páginas en Notion por palabra clave.
    
    Args:
        query: Término de búsqueda
    
    Returns:
        Resultados formateados
    """
    if not notion_client:
        return "❌ Notion no está configurado"
    
    try:
        response = notion_client.search(
            query=query,
            filter={"property": "object", "value": "page"}
        )
        
        results = response.get("results", [])
        if not results:
            return f"❌ No se encontraron páginas para: '{query}'"
        
        output = f"📋 Resultados de búsqueda para '{query}':\n\n"
        
        for page in results:
            props = page.get("properties", {})
            title = "Sin título"
            
            for prop_name, prop_value in props.items():
                if prop_value.get("type") == "title":
                    rich_text = prop_value.get("title", [])
                    if rich_text:
                        title = rich_text[0].get("plain_text", "Sin título")
                    break
            
            page_id = page["id"]
            url = page.get("url", "")
            
            output += f"• {title}\n"
            output += f"  ID: {page_id}\n"
            output += f"  URL: {url}\n\n"
        
        return output
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

@tool
def get_page_notion(page_id: str) -> str:
    """
    Obtiene el contenido de una página de Notion.
    
    Args:
        page_id: ID de la página
    
    Returns:
        Contenido formateado
    """
    if not notion_client:
        return "❌ Notion no está configurado"
    
    try:
        page_id_clean = page_id.replace("-", "")
        
        page = notion_client.pages.retrieve(page_id_clean)
        blocks = notion_client.blocks.children.list(page_id_clean)
        
        props = page.get("properties", {})
        title = "Sin título"
        
        for prop_name, prop_value in props.items():
            if prop_value.get("type") == "title":
                rich_text = prop_value.get("title", [])
                if rich_text:
                    title = rich_text[0].get("plain_text", "Sin título")
                break
        
        content = f"📄 {title}\n"
        content += f"ID: {page_id_clean}\n"
        content += f"URL: {page.get('url', '')}\n"
        content += f"Bloques: {len(blocks.get('results', []))}\n"
        
        return content
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

@tool
def create_page_notion(title: str, content: str = "", parent_id: str = None, database_name: str = None, parent_page_title: str = None) -> str:
    """
    Crea una página nueva en Notion.
    
    Args:
        title: Título de la página (REQUERIDO)
        content: Contenido de texto (opcional)
        parent_id: ID de página padre o database (opcional)
        database_name: Nombre de la base de datos donde crear (opcional)
        parent_page_title: Título de la página padre para crear una subpágina (opcional)
    
    Returns:
        Confirmación de creación
    """
    if not notion_client:
        return "❌ Notion no está configurado"
    
    try:
        # Determinar el parent_id
        if not parent_id:
            if parent_page_title:
                page = find_page_by_title(parent_page_title)
                if page:
                    parent_id = page["id"]
                else:
                    return f"❌ Página padre '{parent_page_title}' no encontrada"
            elif database_name:
                db = find_database_by_name(database_name)
                if db:
                    parent_id = db["id"]
                else:
                    return f"❌ Base de datos '{database_name}' no encontrada"
            else:
                parent_id = get_first_parent_id()
                if not parent_id:
                    return "❌ No hay bases de datos ni páginas disponibles"
        
        parent_id_clean = parent_id.replace("-", "")
        
        # Crear página
        page = notion_client.pages.create(
            parent={"page_id": parent_id_clean},
            properties={
                "title": {
                    "title": [{"text": {"content": title}}]
                }
            }
        )
        
        page_id = page["id"]
        
        # Actualizar título con ID
        title_with_id = f"{title} {page_id}"
        notion_client.pages.update(
            page_id,
            properties={
                "title": {
                    "title": [{"text": {"content": title_with_id}}]
                }
            }
        )
        
        # Agregar contenido si existe
        if content:
            notion_client.blocks.children.append(
                block_id=page_id,
                children=[{
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    }
                }]
            )
        
        output = f"✅ Página creada\n"
        output += f"Título: {title_with_id}\n"
        output += f"URL: {page.get('url', '')}\n"
        
        return output
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

@tool
def list_databases_notion() -> str:
    """
    Lista todas las bases de datos compartidas.
    
    Returns:
        Lista de bases de datos
    """
    if not notion_client:
        return "❌ Notion no está configurado"
    
    try:
        databases = get_databases()
        
        if not databases:
            return "❌ No hay bases de datos compartidas"
        
        output = f"📚 Bases de datos ({len(databases)}):\n\n"
        
        for db in databases:
            title = "Sin título"
            if db.get("title"):
                title = db["title"][0].get("plain_text", "Sin título")
            
            db_id = db["id"]
            url = db.get("url", "")
            
            output += f"• {title}\n"
            output += f"  ID: {db_id}\n"
            output += f"  URL: {url}\n\n"
        
        return output
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

@tool
def update_page_notion(page_id: str, title: str = None, content: str = None) -> str:
    """
    Actualiza el título y/o contenido de una página en Notion.
    
    Args:
        page_id: ID de la página
        title: Nuevo título (opcional)
        content: Contenido a agregar al final de la página (opcional)
    
    Returns:
        Confirmación
    """
    if not notion_client:
        return "❌ Notion no está configurado"
    
    try:
        if not title and not content:
            return "❌ Debes proporcionar al menos un título o contenido"
        
        page_id_clean = page_id.replace("-", "")
        resultado = []
        
        # Actualizar título si se proporciona
        if title:
            notion_client.pages.update(
                page_id_clean,
                properties={
                    "title": {
                        "title": [{"text": {"content": title}}]
                    }
                }
            )
            resultado.append(f"✅ Título actualizado: {title}")
        
        # Agregar contenido si se proporciona
        if content:
            notion_client.blocks.children.append(
                block_id=page_id_clean,
                children=[
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": content}
                                }
                            ]
                        }
                    }
                ]
            )
            resultado.append(f"✅ Contenido agregado exitosamente")
        
        return "\n".join(resultado)
    
    except Exception as e:
        return f"❌ Error: {str(e)}"


@tool
def get_subpages_notion(page_title: str) -> str:
    """
    Obtiene información sobre las subpáginas de una página existente.
    
    Args:
        page_title: Título de la página padre
    
    Returns:
        Información sobre la página
    """
    if not notion_client:
        return "❌ Notion no está configurado"
    
    try:
        page = find_page_by_title(page_title)
        
        if not page:
            return f"❌ Página '{page_title}' no encontrada"
        
        page_id = page["id"]
        blocks = notion_client.blocks.children.list(page_id)
        
        output = f"📄 Página: {page_title}\n"
        output += f"Bloques encontrados: {len(blocks.get('results', []))}\n\n"
        
        return output
    
    except Exception as e:
        return f"❌ Error: {str(e)}"
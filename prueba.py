#!/usr/bin/env python3
"""Prueba las herramientas de Notion"""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("🧪 TEST DE HERRAMIENTAS NOTION")
print("=" * 70)

# Importar herramientas
try:
    from mcpTools import (
        search_notion, 
        get_page_notion, 
        create_page_notion, 
        list_databases_notion,
        
    )
    print("\n✅ Herramientas importadas correctamente")
except Exception as e:
    print(f"\n❌ Error importando herramientas: {e}")
    exit(1)

# Test 1: Listar bases de datos
print("\n" + "=" * 70)
print("TEST 1: Listar bases de datos")
print("=" * 70)

try:
    resultado = list_databases_notion.invoke(input={})
    print(resultado)
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Buscar en Notion
print("\n" + "=" * 70)
print("TEST 2: Buscar en Notion")
print("=" * 70)

try:
    resultado = search_notion.invoke(input={"query": "test"})
    print(resultado)
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Obtener información de la página encontrada
print("\n" + "=" * 70)
print("TEST 3: Obtener página")
print("=" * 70)

try:
    # Primero buscar para obtener un ID
    from notion_client import Client
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    response = notion.search()
    
    if response.get("results"):
        page_id = response["results"][0]["id"]
        print(f"Usando página ID: {page_id}")
        resultado = get_page_notion.invoke(input={"page_id": page_id})
        print(resultado)
    else:
        print("❌ No hay páginas para probar")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
print("✅ TESTS COMPLETADOS")
print("=" * 70)
print("\nSi todos los tests pasaron, las herramientas funcionan correctamente.")
print("Ahora puedes usar el agente con seguridad en main.py")
# 📋 Guía de Configuración de Variables de Entorno

## 🎯 Objetivo
Este documento describe todas las variables de entorno necesarias para ejecutar el proyecto **Agente Notion** correctamente.

---

## 📌 Variables Obligatorias

### 1. **NOTION_TOKEN**
- **Descripción**: Token de autenticación de la API de Notion
- **Dónde obtenerlo**: https://www.notion.so/my-integrations
- **Cómo obtenerlo**:
  1. Ve a tu página de integraciones de Notion
  2. Haz clic en "Create new integration"
  3. Dale un nombre (ej: "Agente IA")
  4. Copia el token que aparece bajo "Internal Integration Token"
  5. Pégalo en `.env` como `NOTION_TOKEN=xxx`
- **Usado en**: 
  - `mcpTools.py` (línea 12)
  - `notion_mcp_server.py` (línea 13)
  - `prueba.py` (línea 57)
- **Ejemplo**: `NOTION_TOKEN=secret_abc123def456ghi789`

### 2. **OPEN_ROUTER_API_KEY**
- **Descripción**: Clave API de OpenRouter para acceso a múltiples modelos de IA
- **Dónde obtenerlo**: https://openrouter.ai/keys
- **Cómo obtenerlo**:
  1. Crea una cuenta en OpenRouter.ai
  2. Ve a la sección de API Keys
  3. Crea una nueva clave
  4. Cópiala y pégala en `.env` como `OPEN_ROUTER_API_KEY=xxx`
- **Usado en**: 
  - `main.py` (línea 145) - Para modelos de OpenRouter
- **Modelos disponibles**:
  - `meta-llama/llama-3.3-70b-instruct:free`
  - `google/gemma-3-4b-it:free`
  - `nex-agi/deepseek-v3.1-nex-n1:free`
- **Ejemplo**: `OPEN_ROUTER_API_KEY=sk-or-abc123def456`

---

## 📌 Variables Opcionales

### 3. **GOOGLE_API_KEY**
- **Descripción**: Clave API de Google para usar modelos Gemini
- **Dónde obtenerlo**: https://console.cloud.google.com/ o https://aistudio.google.com/
- **Cuándo es necesario**: Solo si usas modelos de Google Gemini
- **Modelos disponibles**:
  - `gemini-2.5-flash`
  - `gemini-2.5-pro`
  - `gemini-2.5-flash-lite`
  - `gemini-3-pro-preview`
- **Usado en**: 
  - `main.py` (línea 139) - ChatGoogleGenerativeAI
- **Ejemplo**: `GOOGLE_API_KEY=AIza...`

### 4. **LANGFUSE_API_KEY**
- **Descripción**: Clave API de LangFuse para trazabilidad y análisis de llamadas a IA
- **Dónde obtenerlo**: https://cloud.langfuse.com/
- **Cuándo es necesario**: Si necesitas logging y análisis de las llamadas a modelos
- **Variables relacionadas**:
  - `LANGFUSE_PUBLIC_KEY`: Clave pública de LangFuse
  - `LANGFUSE_HOST`: URL del servidor LangFuse (por defecto: https://cloud.langfuse.com)
- **Ejemplo**:
  ```
  LANGFUSE_API_KEY=sk-lf-...
  LANGFUSE_PUBLIC_KEY=pk-lf-...
  LANGFUSE_HOST=https://cloud.langfuse.com
  ```

---

## 📂 Variables de Configuración

### 5. **RAG_DB_PATH**
- **Descripción**: Ruta donde se almacena la base de datos vectorial del RAG
- **Valor por defecto**: `./rag_db`
- **Usado en**: `ragManager.py`

### 6. **RAG_DOCUMENTS_PATH**
- **Descripción**: Ruta donde se guardan los documentos para el RAG
- **Valor por defecto**: `./documentos_rag`
- **Usado en**: `ragManager.py`

### 7. **LLM_TEMPERATURE**
- **Descripción**: Parámetro de temperatura para los modelos (creatividad vs. determinismo)
- **Rango**: 0.0 - 1.0
- **Valor por defecto**: `0.7`
- **Usado en**: `main.py` (línea 19)

### 8. **GRADIO_PORT**
- **Descripción**: Puerto en el que se ejecuta la interfaz web
- **Valor por defecto**: `7860`
- **Usado en**: `main.py`

### 9. **GRADIO_SHARE**
- **Descripción**: Si True, Gradio generará un URL público compartible
- **Valores**: `True` o `False`
- **Valor por defecto**: `False`

---

## 🔧 Pasos de Configuración Rápida

### 1. Copiar el archivo de plantilla
```bash
cp .env.example .env
```

### 2. Editar el archivo `.env`
Abre el archivo `.env` con tu editor de texto favorito y completa:

```env
NOTION_TOKEN=your_notion_token_here
OPEN_ROUTER_API_KEY=your_openrouter_api_key_here
```

### 3. Verificar la configuración
```bash
python prueba.py
```

Este script probará la conexión a Notion y confirmará que todo está configurado correctamente.

---

## ⚠️ Medidas de Seguridad

1. **NUNCA** subas el archivo `.env` a repositorios públicos
2. Usa `.gitignore` para excluir `.env` (ya incluido en el proyecto)
3. En producción, usa variables de entorno del sistema operativo
4. Rota regularmente tus tokens y claves
5. Revisa los permisos de tu integración de Notion (usa la mínima autorización necesaria)

---

## 📝 Ejemplo de archivo `.env` completo

```env
# Obligatorios
NOTION_TOKEN=secret_abc123def456ghi789
OPEN_ROUTER_API_KEY=sk-or-abc123def456

# Opcionales
GOOGLE_API_KEY=AIza...
LANGFUSE_API_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...

# Configuración
RAG_DB_PATH=./rag_db
RAG_DOCUMENTS_PATH=./documentos_rag
LLM_TEMPERATURE=0.7
GRADIO_PORT=7860
GRADIO_SHARE=False
```

---

## 🐛 Solución de Problemas

### Error: "NOTION_TOKEN no está configurado"
- Verifica que `NOTION_TOKEN` está en el archivo `.env`
- Asegúrate de que el archivo está en la raíz del proyecto
- Comprueba que no hay espacios extra alrededor del `=`

### Error: "OPEN_ROUTER_API_KEY" no encontrada
- Verifica que tienes una cuenta en OpenRouter.ai
- Comprueba que tu clave API es correcta
- Asegúrate de que tienes saldo/créditos disponibles

### Los modelos de Google no funcionan
- `GOOGLE_API_KEY` es opcional, pero necesario para modelos Gemini
- Si no lo tienes, usa modelos de OpenRouter que son gratuitos

### Problemas con el RAG
- Verifica que las carpetas `RAG_DB_PATH` y `RAG_DOCUMENTS_PATH` existen
- Asegúrate de tener permisos de lectura/escritura

---

## 📚 Referencias Útiles

- [Notion API Documentation](https://developers.notion.com/)
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Google Generative AI](https://ai.google.dev/)
- [LangFuse Documentation](https://docs.langfuse.com/)

---

**Última actualización**: Enero 2026

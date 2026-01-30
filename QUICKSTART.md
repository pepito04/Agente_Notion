# 🚀 GUÍA RÁPIDA - PRIMEROS PASOS

## 1️⃣ Configuración Inicial (5 minutos)

### Paso 1: Obtener Notion Token
```
1. Ve a: https://www.notion.so/my-integrations
2. Haz clic en "Create new integration"
3. Copia el "Internal Integration Token"
```

### Paso 2: Obtener OpenRouter API Key
```
1. Ve a: https://openrouter.ai/keys
2. Crea una cuenta si no tienes
3. Copia tu API key
```

### Paso 3: Editar .env
```
Abre: c:\Users\PC\Desktop\GIT\Agente_Notion\.env
Reemplaza:
  NOTION_TOKEN=your_notion_token_here → NOTION_TOKEN=sk-proj-abc123...
  OPEN_ROUTER_API_KEY=your_openrouter_api_key_here → OPEN_ROUTER_API_KEY=sk-or-def456...
```

---

## 2️⃣ Verificación (2 minutos)

```bash
cd c:\Users\PC\Desktop\GIT\Agente_Notion
python prueba.py
```

Si ves ✅ en la salida, ¡está todo configurado!

---

## 3️⃣ Ejecutar la Aplicación

```bash
python main.py
```

Se abrirá en: http://localhost:7860

---

## 📋 Archivos Generados Automáticamente

| Archivo | Propósito |
|---------|-----------|
| `.env` | Configuración de credenciales (NO compartir) |
| `.gitignore` | Evita subir `.env` a Git |
| `QUICKSTART.md` | Este archivo (guía rápida) |

---

## ❓ ¿Qué variable es obligatoria?

✅ **NOTION_TOKEN** - Obligatorio
✅ **OPEN_ROUTER_API_KEY** - Obligatorio (para acceso a IA)
⭐ **GOOGLE_API_KEY** - Opcional (solo si usas Google Gemini)
⭐ **LANGFUSE_*** - Opcional (solo si quieres trazabilidad)

---

## 🐛 Errores Comunes

### ❌ "NOTION_TOKEN no está configurado"
→ El valor sigue siendo `your_notion_token_here`
→ Reemplázalo con tu token real

### ❌ "OPEN_ROUTER_API_KEY no encontrada"
→ No está en el `.env` o está mal escrito
→ Verifica que esté en la línea correcta

### ❌ Los modelos de Google no funcionan
→ Necesitas `GOOGLE_API_KEY` si usas esos modelos
→ Usa modelos de OpenRouter (son gratis)

---

## 📞 Support

- **Notion API Docs**: https://developers.notion.com/
- **OpenRouter Docs**: https://openrouter.ai/docs
- **Proyecto README**: Ver `README.md`
- **Documentación Completa**: Ver `ENVIRONMENT_SETUP.md`

---

¡Listo para empezar! 🎉

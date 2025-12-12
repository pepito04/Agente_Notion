import gradio as gr 
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
import mimetypes as mt
from langchain.tools import tool
import cargaArchivos as ca
import ragManager
from ragManager import rag
from mcpTools import search_notion, get_page_notion, create_page_notion, list_databases_notion, update_page_notion, get_subpages_notion

load_dotenv()
rag.agregar_carpeta_completa()

# Variables
temp = 0.7
modeloGoogle = ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-2.5-flash-lite', 'gemini-3-pro-preview']
modeloOpenRouter = ['meta-llama/llama-3.3-70b-instruct:free', 'google/gemma-3-4b-it:free', 'nex-agi/deepseek-v3.1-nex-n1:free']

historial = []
fileTypes = [
    ".txt", ".md", ".py", ".log", ".html", ".css", ".js", ".png", ".jpg", ".jpeg",
    ".json", ".csv", ".xls", ".xlsx", ".pdf"
]

def agregar_archivo_a_rag(ruta_archivo):
    """Agrega archivos al RAG"""
    if isinstance(ruta_archivo, str):
        rutas = [ruta_archivo]
    else:
        rutas = ruta_archivo
    
    for ruta in rutas:
        resultado = ragManager.rag.agregar_archivo(ruta)
        print(f"RAG: {resultado}")
    return resultado

# INPUTS
inputs = [
    gr.TextArea(label="Pregunta lo que quieras"),
    gr.Checkbox(label="Thinking Mode"),
    gr.Dropdown(choices=modeloGoogle + modeloOpenRouter),
    gr.File(
        label="📁 Cargar archivo",
        file_types=fileTypes,
        type="filepath",
        file_count="multiple"
    ),
    gr.Checkbox(label="Subir archivos a RAG")
]

# OUTPUTS
outputs = [
    gr.TextArea(label="Respuesta"),
    gr.TextArea(label="Historial")
]

# TOOLS
@tool
def cargar_archivo(archivos: str) -> str:
    """
    Procesa y carga archivos locales.
    Lee el contenido según el tipo de archivo.
    
    Args:
        archivos: Ruta del archivo o lista de rutas
    
    Returns:
        Contenido del archivo procesado
    """
    if not archivos:
        return "No se ha subido ningún archivo."
    
    if isinstance(archivos, str):
        archivos = [archivos]
    
    resultados = []
    
    for ruta in archivos:
        nombre = os.path.basename(ruta)
        extension = os.path.splitext(nombre)[1].lower()
        
        try:
            if extension in [".txt", ".md", ".py", ".log", ".html", ".css", ".js"]:
                contenido = ca.leerTexto(ruta)
            elif extension == ".pdf":
                contenido = ca.leerPdf(ruta)
            elif extension == ".json":
                contenido = ca.leerJSON(ruta)
            elif extension == ".csv":
                contenido = ca.leerCSV(ruta)
            elif extension == ".xlsx" or extension == ".xls":
                contenido = ca.leerExcel(ruta)
            elif extension in [".png", ".jpg", ".jpeg"]:
                contenido = ca.leerImagen(ruta)
            else:
                contenido = f"Tipo no soportado: {extension}"
            
            contenido_str = str(contenido)[:1000]  # Limitar a 1000 caracteres
            resultados.append(f"--- {nombre} ---\n{contenido_str}")
        except Exception as e:
            resultados.append(f"Error con {nombre}: {e}")
    
    return "\n\n".join(resultados)

@tool
def buscar_en_rag(consulta: str) -> str:
    """
    Busca información en la base de datos de conocimiento local (RAG).
    
    Args:
        consulta: La pregunta o término a buscar
    
    Returns:
        Contexto relevante encontrado
    """
    try:
        contexto = rag.obtener_contexto(consulta, k=3)
        return contexto
    except Exception as e:
        return f"Error buscando en RAG: {str(e)}"

def chatbot(entrada, boton, modelo, archivo, agregar_rag):
    """Función principal del chatbot"""
    global historial
    
    # Agregar archivos a RAG si se solicita
    if archivo and agregar_rag:
        for f in archivo:
            agregar_archivo_a_rag(f)
    
    # Instrucción de thinking
    think = "Muestra tu razonamiento entre [THINKING] y [/THINKING]." if boton else ""
    
    # Seleccionar modelo
    if modelo in modeloGoogle:
        model_instance = ChatGoogleGenerativeAI(model=modelo)
    elif modelo in modeloOpenRouter:
        model_instance = ChatOpenAI(
            model=modelo,
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=os.getenv("OPEN_ROUTER_API_KEY"),
        )
    else:
        return "ERROR: Debes elegir un modelo válido", str(historial)
    
    # Procesar archivos si existen
    contenido_mensaje = [{"type": "text", "text": entrada}]
    if archivo and len(archivo) > 0:
        contenido_mensaje[0]["text"] += f"\n\nArchivos cargados:\n{archivo}"
    
    mensajes = [HumanMessage(content=contenido_mensaje)]
    listaIds = ["2c5a65414e2f80f59110fe1792e9ed80"]
    # Crear agente con herramientas RAG y Notion
    agente = create_agent(
        model=model_instance,
        tools=[
            search_notion,
            get_page_notion,
            get_subpages_notion,
            create_page_notion,
            list_databases_notion,
            update_page_notion,
            cargar_archivo,
            buscar_en_rag,
        ],
        system_prompt=(
            f"Eres un asistente inteligente que habla en español. {think} "
            "Tienes acceso a varias herramientas:\n"
            "1. Herramientas de Notion: para buscar, crear y actualizar páginas\n"
            "2. Herramienta cargar_archivo: para procesar archivos subidos\n"
            "3. Herramienta buscar_en_rag: para buscar en la base de datos de conocimiento local\n\n"
            "Cuando el usuario suba archivos, SIEMPRE usa primero la herramienta 'cargar_archivo'.\n"
            "Cuando busques información general, usa 'buscar_en_rag' para consultar la base de datos local.\n"
            "Para operaciones con Notion, busca por nombres en lugar de pedir IDs.\n"
            "Si el usuario no especifica dónde crear una página, crea en la primera base de datos/página disponible."
            f"Si necesitas IDs de páginas o bases de datos, usa las herramientas de Notion para obtenerlos o revisa en esta lista: {listaIds}."
            "Siempre que el usuario te pida hacer algo en notion, busca en el rag las notaciones correspòndientes"
            ),
    )
    
    try:
        response = agente.invoke({"messages": mensajes})
        respuesta = response["messages"][-1].content
    except Exception as e:
        return f"Error: {str(e)}", str(historial)
    
    # Actualizar historial
    historial.append({"role": "user", "content": entrada})
    historial.append({"role": "assistant", "content": respuesta})
    
    return respuesta, str(historial)

# INTERFAZ GRADIO
interfaz = gr.Interface(
    fn=chatbot,
    inputs=inputs,
    outputs=outputs,
    title="Agente Notion",
    description="Chatbot con herramientas MCP de Notion"
)

print("=" * 50)
print("🚀 Iniciando interfaz Gradio...")
print("=" * 50)
interfaz.launch()
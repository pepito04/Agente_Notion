import pandas as pd
import json
import PyPDF2
from PIL import Image
import numpy as np
import io
import base64


# def leerTexto(uploaded_file):
#     """
#     Lee archivos de texto subidos desde Gradio.
#     """
#     try:
#         contenido = uploaded_file.file.read().decode("utf-8", errors="ignore")
#         return contenido
#     except Exception as e:
#         return f"Error al leer texto: {e}"


# def leerCSV(uploaded_file):
#     """
#     Lee archivos CSV subidos desde Gradio.
#     """
#     try:
#         df = pd.read_csv(uploaded_file.file)
#         return df
#     except Exception as e:
#         return f"Error al leer CSV: {e}"


# def leerJSON(uploaded_file):
#     """
#     Lee archivos JSON subidos desde Gradio.
#     """
#     try:
#         data = json.load(uploaded_file.file)
#         return data
#     except Exception as e:
#         return f"Error al leer JSON: {e}"


# def leerExcel(uploaded_file):
#     """
#     Lee archivos Excel subidos desde Gradio.
#     """
#     try:
#         df = pd.read_excel(uploaded_file.file)
#         return df
#     except Exception as e:
#         return f"Error al leer Excel: {e}"


# def leerPdf(uploaded_file):
#     """
#     Lee archivos PDF y extrae texto desde Gradio.
#     """
#     try:
#         texto = ""
#         lector = PyPDF2.PdfReader(uploaded_file.file)
#         for pagina in lector.pages:
#             texto += pagina.extract_text() or ""
#         return texto
#     except Exception as e:
#         return f"Error al leer PDF: {e}"


# def leerImagen(uploaded_file):
#     """
#     Procesa imágenes subidas desde Gradio.
#     """
#     try:
#         # Abrir desde file-like object
#         img = Image.open(uploaded_file.file)

#         img = img.convert("RGB")
#         matriz = np.array(img)

#         return {
#             "array": matriz,
#             "ancho": img.width,
#             "alto": img.height,
#             "modo": img.mode,
#         }

#     except Exception as e:
#         return {"error": f"No se pudo procesar la imagen: {e}"}


def leerTexto(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            return f.read()

def leerCSV(ruta):
    df = pd.read_csv(ruta)
    return df

def leerJSON(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def leerExcel(ruta):
    df = pd.read_excel(ruta)
    return df   

def leerPdf(ruta):
    texto = ""
    with open(ruta, 'rb') as f:
        lector = PyPDF2.PdfReader(f)
        for pagina in lector.pages:
            texto += pagina.extract_text()
    return texto

def leerImagen(ruta):
    try:
        with open(ruta, "rb") as f:
            imagen_bytes = f.read()
        
        # Convertir a base64
        imagen_base64 = base64.b64encode(imagen_bytes).decode('utf-8')
        
        # Detectar tipo MIME
        img = Image.open(ruta)
        formato = img.format.lower() if img.format else "jpeg"
        mime_type = f"image/{formato}"
        
        # Crear data URI
        data_uri = f"data:{mime_type};base64,{imagen_base64}"
        
        return {
            "tipo": "imagen",
            "data_uri": data_uri,
            "ancho": img.width,
            "alto": img.height,
            "modo": img.mode,
            "formato": formato
        }
    except Exception as e:
        return f"Error: No se pudo procesar la imagen: {e}"
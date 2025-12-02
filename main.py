import gradio as gr 
import numpy as np 
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

# Variables personalizacion
temp = 0.7
boton = False # REEMPLAZAR ESTA VARIABLE POR UN ACTIVADOR
modelo = 'gemini-2.5-flash'

# Variables 
historial = ""

client = genai.Client(api_key = os.getenv("GOOGLE_API_KEY"))

# INPUTS
inputs = [
    gr.TextArea(label="Pregunta lo que quieras"), #entrada
    gr.Checkbox(label="Thinking Mode"), #boton
    gr.Dropdown(choices = ['gemini-2.5-flash', 'gemini-2.5-pro'])
]

#OUTPUTS
outputs = [
    gr.TextArea(label = "Respuesta"),
    gr.TextArea(label = "historial")
]

def chatbot(entrada, boton, modelo):
    think = ""
    # Personalización del modelo
    chat = client.chats.create(
        model=modelo,
        config={
            'temperature': 0.7,  # Creatividad (0.0 - 2.0)
            'system_instruction': f'Eres un asistente útil, correcto y educado. Idoneo para un entorno corporativo. {think}'
            # 'system_instruction' : 'Eres un asistente amigable que trata al usuario como su "bro"'
        }
    )
    print(modelo)
    if boton: 
        think = "Muestra tu razonamiento entre [THINKING] y [/THINKING]."
    else: 
        think = ""
    
    response = chat.send_message(entrada)
    global historial 
    historial = list(historial) + chat.get_history()
    return response.text, historial

interfaz = gr.Interface(
    fn=chatbot,
    inputs= inputs,
    outputs= outputs
)

interfaz.launch()



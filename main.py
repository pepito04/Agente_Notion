import gradio as gr 
import numpy as np 
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    print("OK")
else: 
    print("ERROR")

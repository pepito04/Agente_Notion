# En este documento os contaré sobre el chatbot para Notion

He creado un chatbot que utiliza un RAG para que podamos subirle todos los archivos necesarios tanto de manera manual a su carpeta como a traves de su interfaz en gradio. 

Procesa el lenguaje natural creando paginas, bases de datos y casi cualquier cosa que requiramos siempre y cuando se lo pidamos amablemente. Podemos pasar archivos a Notion, crear paginas nuevas, que nos haga listas y, ademas, podemos hacer que todo un equipo de trabajo lo utilice ya que Notion permite espacios de trabajo grupales. 

Esto es util tanto para el uso personal y diario, como para cualquier empresa que tenga una "base de datos" centralizada y quiere resolver cuestiones a traves de ella con la ayuda de nuestro agente. Ademas nos podrá crear resúmenes, documentacion, apis para lenguajes de programacion, anotaciones, comentarios y un sinfin de tareas mas.

Los modelos utilizados son principalmente los proporcionados por google: 
- gemini-2.5-flash 
- gemini-2.5-pro 
- gemini-2.5-flash-lite 

Pero tambien hemos añadido desde OpenRouter algunos gratuitos para que no tengamos problemas si nos quedamos sin consultas: 
- meta-llama/llama-3.3-70b-instruct:free 
- google/gemma-3-4b-it:free
- nex-agi/deepseek-v3.1-nex-n1:free'

## Diagrama Conversacional
<img src="Diagrama conversacional.png" alt="Descripción" width="300">


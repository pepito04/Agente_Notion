import os
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document 
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb
from chromadb.config import Settings
import cargaArchivos as ca

# ===========================================================
#   AQUI SE ENCUENTRA LA RUTA DE LA CARPETA
# ===========================================================
class RAGManager:
    def __init__(self, carpeta_persistencia="./rag_db", carpeta_documentos="./documentos_rag"):
        """
        Inicializa el RAG Manager.
        
        Args:
            carpeta_persistencia: Donde se guarda la base de datos vectorial
            carpeta_documentos: Carpeta local con los documentos fuente
        """
        self.carpeta_documentos = carpeta_documentos
        self.carpeta_persistencia = carpeta_persistencia
        
        # Crear carpetas si no existen
        os.makedirs(carpeta_documentos, exist_ok=True)
        os.makedirs(carpeta_persistencia, exist_ok=True)
        
        # Embeddings (modelo gratuito de HuggingFace)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Base de datos vectorial Chroma
        self.vectorstore = Chroma(
            collection_name="documentos_rag",
            embedding_function=self.embeddings,
            persist_directory=carpeta_persistencia
        )
        
        # Splitter para dividir documentos grandes
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def agregar_archivo(self, ruta_archivo):
        """
        Agrega un archivo al RAG.
        
        Args:
            ruta_archivo: Ruta del archivo a agregar
        
        Returns:
            str: Mensaje de éxito o error
        """
        try:
            nombre = os.path.basename(ruta_archivo)
            extension = os.path.splitext(nombre)[1].lower()
            # Leer contenido según tipo de archivo
            if extension in [".txt", ".md", ".py", ".log"]:
                contenido = ca.leerTexto(ruta_archivo)
            elif extension == ".pdf":
                contenido = ca.leerPdf(ruta_archivo)
            elif extension == ".json":
                contenido = ca.leerJSON(ruta_archivo)
            elif extension == ".csv":
                contenido = ca.leerCSV(ruta_archivo)
            else:
                return f"Tipo de archivo no soportado para RAG: {extension}"
            
            # Crear documento
            documento = Document(
                page_content=contenido,
                metadata={
                    "fuente": nombre,
                    "ruta": ruta_archivo,
                    "tipo": extension
                }
            )
            
            # Dividir en chunks
            chunks = self.text_splitter.split_documents([documento])
            
            # Agregar a vectorstore
            self.vectorstore.add_documents(chunks)
            
            return f"✅ Archivo '{nombre}' agregado al RAG ({len(chunks)} chunks)"
        
        except Exception as e:
            return f"❌ Error al agregar archivo: {str(e)}"
    
    def agregar_carpeta_completa(self):
        """
        Agrega todos los archivos de la carpeta de documentos al RAG.
        
        Returns:
            str: Resumen de archivos agregados
        """
        archivos_procesados = []
        
        for archivo in os.listdir(self.carpeta_documentos):
            ruta_completa = os.path.join(self.carpeta_documentos, archivo)
            
            if os.path.isfile(ruta_completa):
                resultado = self.agregar_archivo(ruta_completa)
                archivos_procesados.append(resultado)
        
        return "\n".join(archivos_procesados)
    
    def buscar(self, consulta, k=5):
        """
        Busca documentos relevantes en el RAG.
        
        Args:
            consulta: Texto de búsqueda
            k: Número de resultados a devolver
        
        Returns:
            list: Lista de documentos relevantes
        """
        try:
            resultados = self.vectorstore.similarity_search(consulta, k=k)
            return resultados
        except Exception as e:
            return []
    
    def buscar_con_scores(self, consulta, k=5):
        """
        Busca con scores de relevancia.
        
        Returns:
            list: [(Document, score), ...]
        """
        try:
            resultados = self.vectorstore.similarity_search_with_score(consulta, k=k)
            return resultados
        except Exception as e:
            return []
    
    def obtener_contexto(self, consulta, k=5):
        """
        Obtiene contexto formateado para el agente.
        
        Returns:
            str: Contexto relevante como texto
        """
        resultados = self.buscar(consulta, k=k)
        
        if not resultados:
            return "No se encontró información relevante en el RAG."
        
        contexto = "### Información relevante del RAG:\n\n"
        
        for i, doc in enumerate(resultados, 1):
            fuente = doc.metadata.get("fuente", "desconocida")
            contexto += f"**[{i}] Fuente: {fuente}**\n{doc.page_content}\n\n"
        
        return contexto


# Instancia global
rag = RAGManager()

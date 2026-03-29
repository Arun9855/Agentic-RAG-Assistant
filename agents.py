import os
import multiprocessing
from langchain_community.llms import LlamaCpp
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

# --- Local Configurations ---
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_PATH = os.path.abspath("model.gguf")

# --- Custom RAG Retrieval ---
def search_catalog_data(query: str) -> str:
    try:
        embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        results = db.similarity_search(query, k=4)
        
        response = ""
        for i, doc in enumerate(results):
            source = doc.metadata.get('source', 'Unknown source')
            response += f"--- Result {i+1} [Source: {source}] ---\n"
            response += doc.page_content + "\n\n"
        return response if response else "No information found in the USC catalog."
    except Exception as e:
        return f"Retrieval Error: {e}"

# --- Initialize Local Model via Native LlamaCpp ---
print(f"Initializing Local GGUF Engine: {MODEL_PATH}...")
llm = LlamaCpp(
    model_path=MODEL_PATH,
    temperature=0.1,
    max_tokens=1024,
    n_ctx=4096,
    n_threads=max(1, multiprocessing.cpu_count() - 2),
    verbose=False,
    # Stop tokens to prevent repetition
    stop=["###", "Question:", "MANDATORY OUTPUT FORMAT:"]
)

# --- Final Reasoning Controller ---
class CourseAdvisor:
    def answer(self, query: str):
        # 1. Local Retrieval
        context = search_catalog_data(query)
        
        # 2. Local Reasoning with Strict Prompt Template
        # Using a simple prompt format that works well with local models
        prompt = f"""### Instructions:
You are a USC Academic Advisor. Answer the question using ONLY the catalog snippets provided below.
Strictly adhere to the output format provided. If info is missing, say you don't know and suggest what to check next.

### Catalog Data:
{context}

### Question:
{query}

### Response Format:
Answer / Plan: [Response]
Why (requirements/prereqs satisfied): [Strategic justification]
Citations: [URL from source]
Clarifying questions (if needed): [Profile questions]
Assumptions / Not in catalog: [Limitations]

### Actual Response:"""
        
        # Run inference and clean up output
        response = llm.invoke(prompt)
        return response.strip()

advisor = CourseAdvisor()

# Mocking get_crew for eval.py/main.py compatibility
def get_crew(query: str):
    class MockResult:
        def __init__(self, content): 
            # Strip preamble if any
            if "### Actual Response:" in content:
                self.content = content.split("### Actual Response:")[-1].strip()
            else:
                self.content = content.strip()
        def __str__(self): return self.content
    
    return type('MockCrew', (), {
        'kickoff': lambda: MockResult(advisor.answer(query))
    })

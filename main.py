from flask import Flask, request, jsonify
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

app = Flask(__name__)

OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'http://host.docker.internal:11434')

try:
    llm = ChatOllama(
        base_url=OLLAMA_HOST,
        model="mistral:instruct",
    )
    llm.invoke("Test Connection")
    print(f"Berhasil terhubung ke Ollama di {OLLAMA_HOST}")
except Exception as e:
    print(f"Peringatan! gagal terhubung ke Ollama (via LangChain) di {OLLAMA_HOST}. Error: {e}")
    print("Pastikan Ollama berjalan di terminal WSL lain dengan perintah 'ollama run mistral:instruct'")
    llm = None

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{prompt}"),
])

output_parser = StrOutputParser()

@app.route('/')

def hello():
    return "Server API LLM Telah berjalan! Silahkan gunakan endpoint POST /ask untuk bertanya atau berinteraksi."

@app.route('/ask', methods=['POST'])
def ask_mistral():
    if llm is None:
        return jsonify({"error": f"Tidak dapat terhubung ke server ollama di {OLLAMA_HOST}"}), 503
    
    try:
        # Mengambil data JSON dari request
        data = request.json
        if not data or 'prompt' not in data:
            return jsonify({"error": "JSON 'prompt' tidak ditemukan didalam body"}), 400
        
        user_prompt = data['prompt']
        model_name = data.get('model', 'mistral:instruct')

        if model_name == llm.model:
            current_llm = llm
        else:
            current_llm = ChatOllama(
                base_url=OLLAMA_HOST,
                model=model_name,
            )
        
        chain = prompt_template | current_llm | output_parser

        # Mengirim prompt ke ollama dengan model mistral
        print(f"Menerima prompt: {user_prompt} dengan model: {model_name}")

        # Mengambil jawaban dan mengirim kembali sebagai JSON
        answer = chain.invoke({"prompt": user_prompt})
        print(f"Mendapat jawaban: {answer}")

        return jsonify({
            "prompt": user_prompt,
            "answer": answer,
            "model used": model_name
            })
    
    except Exception as e:
        print(f"Terjadi Error: {e}")
        return jsonify({"error": str(e)}), 500
    
# --- Placeholder untuk LlamaIndex (RAG) ---
# Ini adalah tempat Anda akan menggunakan LlamaIndex nanti
@app.route("/ask_rag", methods=['POST'])
def ask_rag_placeholder():
    # Di sinilah Anda akan:
    # 1. Memuat 'index' LlamaIndex Anda (yang sudah Anda bangun dari dokumen)
    # 2. Membuat 'query_engine' dari index tersebut
    # 3. Mengambil 'prompt' dari request.json
    # 4. Menjalankan 'response = query_engine.query(prompt)'
    # 5. Mengembalikan 'response.response' sebagai JSON
    
    return jsonify({
        "info": "Endpoint RAG (LlamaIndex) ini belum diimplementasikan.",
        "tip": "Implementasikan loading index dan query engine di sini."
    }), 501 # 501 = Not Implemented

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
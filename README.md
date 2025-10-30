Project RAG API Bank Mas

Ini adalah project API RAG (Retrieval-Augmented Generation) sederhana yang menggunakan Docker, Flask, LangChain, LlamaIndex, dan Ollama.

API ini memiliki dua endpoint:

/ask: Menjawab pertanyaan umum menggunakan pengetahuan bawaan model.

/ask_rag: Menjawab pertanyaan secara spesifik berdasarkan dokumen di folder /data.

1. Struktur Project

Pastikan Anda memiliki semua file berikut:

bankmas_llm/
├── data/                 # Folder pengetahuan kustom
│   ├── file_produk.txt
│   └── file_layanan.txt
├── main.py               # Kode API Flask (LangChain & LlamaIndex)
├── Dockerfile            # Resep untuk membangun image aplikasi
├── docker-compose.yml    # Instruksi untuk menjalankan aplikasi
├── requirements.txt      # Daftar library Python
├── .dockerignore         # File yang diabaikan oleh Docker
├── .gitignore            # File yang diabaikan oleh Git
└── README.md             # Instruksi ini


2. Prasyarat (Harus Di-install)

Sebelum memulai, pastikan Anda memiliki:

WSL (Windows Subsystem for Linux): Semua perintah dijalankan di dalam WSL.

Docker Desktop (Windows): Pastikan WSL Integration di-enable di:
Settings > Resources > WSL Integration > (Nyalakan distro Anda)

Ollama (Ter-install di WSL):

Install Ollama di dalam terminal WSL Anda menggunakan:

curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh


3. Cara Menjalankan (Reproduksi)

Ikuti dua langkah ini menggunakan dua terminal WSL terpisah.

Langkah 1: Jalankan Server Model (Terminal 1)

Server model (Ollama) harus berjalan di host WSL Anda agar container Docker dapat terhubung dengannya.

Buka terminal WSL.

Tarik dan jalankan model yang Anda inginkan (misalnya mistral:instruct):

ollama run mistral:instruct


Biarkan terminal ini tetap berjalan. Ini adalah server LLM Anda.

Langkah 2: Jalankan Server Aplikasi (Terminal 2)

Buka terminal WSL kedua.

Clone repositori ini (atau navigasikan ke folder project Anda):

# git clone [https://github.com/Marco-andana/llm_rag_1.git](https://github.com/Marco-andana/llm_rag_1.git)
cd bankmas_llm


Bangun (build) dan jalankan container Docker menggunakan Docker Compose:

docker-compose up --build


Aplikasi Anda sekarang berjalan di http://localhost:5000.

4. Cara Menggunakan (Tes API)

Buka terminal ketiga untuk mengirim permintaan curl.

Tes Endpoint Q&A Standar (/ask)

Ini menggunakan pengetahuan umum model.

curl -X POST http://localhost:5000/ask \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Ceritakan lelucon singkat tentang programmer", "model": "mistral:instruct"}'


Tes Endpoint RAG (/ask_rag)

Ini akan menjawab berdasarkan file .txt di dalam folder data/.

Pertanyaan 1 (dari file_produk.txt):

curl -X POST http://localhost:5000/ask_rag \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Berapa setoran awal untuk Tabungan Emas?"}'


Jawaban yang Diharapkan: Setoran awal untuk Tabungan Emas adalah Rp 100.000.
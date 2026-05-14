# MedIntel AI 🏥

## Your Medical Memory, Insurance Decoder, and Hospital Bill Watchdog

MedIntel AI is a premium AI-powered healthcare intelligence and financial protection platform built for patients. Upload your medical documents, and let AI help you understand your health records, decode insurance policies, and detect suspicious billing patterns.

![MedIntel AI](https://img.shields.io/badge/MedIntel-AI%20Healthcare-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)

---

## 🌟 Key Features

### 1. Medical Memory Chat
- Upload prescriptions, lab reports, discharge summaries
- AI extracts and organizes medical information
- Ask questions from your own documents using RAG
- Source-backed answers with confidence scores

### 2. Lab Trend Intelligence
- Extract lab values from uploaded reports
- Track trends over time with interactive charts
- Identify abnormal values with reference ranges
- AI-generated health insights

### 3. Insurance Policy Decoder
- Upload insurance policy documents
- AI extracts key clauses (waiting periods, caps, exclusions)
- Simple explanations of complex insurance terms
- Financial risk assessment
- Questions to ask your insurer

### 4. Hospital Bill Watchdog
- Upload hospital bills for AI analysis
- Detect duplicate charges, inflated costs
- Hybrid anomaly detection (AI + rules)
- Questions to ask the billing desk
- Estimate vs final bill comparison

### 5. Doctor-Ready Summaries
- Generate comprehensive health summaries
- Downloadable PDF reports
- Key questions for your next consultation

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend/Backend | Streamlit |
| OCR | pytesseract, pdf2image |
| PDF Parsing | PyMuPDF, pdfplumber |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Search | FAISS |
| LLM | Groq API (Llama 3.1) |
| Database | SQLite |
| Charts | Plotly |
| PDF Generation | ReportLab |

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Tesseract OCR installed on your system
- Poppler (for pdf2image)

### Install Tesseract OCR

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install tesseract
brew install poppler
```

**Windows:**
- Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
- Download Poppler from: https://github.com/osber/poppler-for-windows

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/your-repo/medintel-ai.git
cd medintel-ai
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Run the application:**
```bash
streamlit run app.py
```

6. **Open in browser:**
```
http://localhost:8501
```

---

## 🔑 API Key Setup

### Groq API (Recommended)
1. Visit https://console.groq.com
2. Create an account and generate an API key
3. Add to `.env`: `GROQ_API_KEY=your_key_here`

### Alternative: OpenAI
1. Visit https://platform.openai.com
2. Generate an API key
3. Add to `.env`: `OPENAI_API_KEY=your_key_here`

---

## 📁 Project Structure

```
medintel_ai/
│
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── README.md                 # Documentation
│
├── data/
│   ├── uploads/              # Uploaded documents
│   ├── extracted_text/       # Extracted text files
│   ├── vector_store/         # FAISS indices
│   ├── reports/              # Generated PDF reports
│   └── medintel.db           # SQLite database
│
├── modules/
│   ├── document_loader.py    # File handling and text extraction
│   ├── ocr_engine.py         # OCR processing
│   ├── text_chunker.py       # Text chunking for embeddings
│   ├── vector_store.py       # FAISS vector operations
│   ├── llm_client.py         # LLM API integration
│   ├── rag_engine.py         # RAG pipeline
│   ├── structured_extractor.py # LLM-based entity extraction
│   ├── lab_analyzer.py       # Lab report analysis
│   ├── insurance_decoder.py  # Insurance policy parsing
│   ├── bill_watchdog.py      # Hospital bill analysis
│   ├── summary_generator.py  # Report generation
│   ├── pdf_generator.py      # PDF creation
│   └── database.py           # SQLite operations
│
├── utils/
│   ├── prompts.py            # AI prompt templates
│   ├── safety.py             # Safety rules and disclaimers
│   ├── ui_components.py      # Reusable UI components
│   ├── config.py             # Configuration management
│   └── helpers.py            # Utility functions
│
└── sample_docs/              # Sample documents for demo
```

---

## 🎯 Demo Instructions

### For Hackathon Judges

1. **Start the application** and navigate to the Home page
2. **Upload documents** on the "Upload & Process" page:
   - Try uploading a prescription PDF
   - Upload a lab report
   - Upload an insurance policy document
   - Upload a hospital bill
3. **Ask questions** on the "Medical Memory Chat" page:
   - "What medicines were prescribed?"
   - "What was my blood sugar level?"
   - "What are the waiting periods in my policy?"
4. **View analysis** on respective pages:
   - Lab Trends for health metrics
   - Insurance Decoder for policy risks
   - Bill Watchdog for billing concerns
5. **Generate summary** and download PDF report

### Live Demo Flow
1. Judge uploads a new document (not pre-loaded)
2. System processes in real-time
3. OCR/extraction happens dynamically
4. RAG answers questions from the new document
5. All outputs are source-backed

---

## ⚠️ Safety & Disclaimers

- **Not a Medical Device**: MedIntel AI does not diagnose diseases or prescribe treatment
- **Doctor-in-the-Loop**: All outputs should be verified with healthcare professionals
- **No Medical Advice**: This system provides information assistance, not medical advice
- **Emergency Warning**: For emergencies, seek immediate medical attention
- **Privacy**: Documents are processed locally; review privacy policies before use
- **Billing Caution**: Bill analysis is indicative; verify with hospital billing department

---

## 🏆 Hackathon Differentiators

1. **Real AI, Not Demo**: Uses actual OCR, embeddings, vector search, RAG, and LLM
2. **Document-Grounded**: Every answer is backed by uploaded documents
3. **Hybrid Intelligence**: Combines AI extraction with rule-based validation
4. **Triple Protection**: Medical memory + Insurance decoder + Bill watchdog
5. **India-Specific**: Built for Indian healthcare context
6. **Financial Safety**: Protects patients from billing overcharges
7. **Source-Backed**: Shows evidence and confidence for all outputs

---

## 📞 Support

For issues or questions:
- Create a GitHub issue
- Contact the development team

---

## 📄 License

MIT License - See LICENSE file for details

---

**Built with ❤️ for AI Healthcare Hackathon**

*MedIntel AI - Making Healthcare Understandable, Accountable, and Financially Safer*

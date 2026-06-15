# BioMed AI — Bioinformatics A2A Agent System

3 AI agents jo milke gene analysis karte hain:
- DNA Research Agent — NCBI se gene data fetch karta hai
- Medical Report Writer — Doctor/patient ke liye report banata hai  
- Drug Discovery Agent — Related drugs aur side effects dhundhta hai

## Setup
1. Clone karo: git clone https://github.com/Laxmanrayka/BIO-A2A.git
2. Dependencies: uv add biopython groq python-dotenv requests fastapi uvicorn reportlab
3. .env file banao: GROQ_API_KEY=... aur NCBI_EMAIL=...
4. Chalao: uv run uvicorn app:app --reload

## Tech Stack
- Biopython, Groq LLM, FastAPI, ReportLab

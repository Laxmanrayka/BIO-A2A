from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import asyncio
import os

from agents.dna_research_agents import analyze_gene
from agents.report_writer_agent import write_medical_report
from agents.drug_discovery_agent import find_drugs
from pdf_generator import generate_pdf

app = FastAPI(title="BioMed AI")

class GeneRequest(BaseModel):
    gene_name: str

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>BioMed AI</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: Arial, sans-serif; background: #f0f4f0; }
            .container { max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #1a472a; text-align: center; font-size: 2.5em; margin-bottom: 10px; }
            .subtitle { text-align: center; color: #666; margin-bottom: 40px; }
            .card { background: white; border-radius: 15px; padding: 30px; 
                   box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
            input { width: 100%; padding: 15px; font-size: 16px; 
                   border: 2px solid #2d6a4f; border-radius: 8px; 
                   margin-bottom: 15px; outline: none; }
            button { width: 100%; padding: 15px; background: #2d6a4f; 
                    color: white; border: none; border-radius: 8px; 
                    font-size: 18px; cursor: pointer; }
            button:hover { background: #1a472a; }
            #loading { display: none; text-align: center; margin: 20px 0; color: #2d6a4f; }
            #result { display: none; margin-top: 30px; }
            .section { background: #f9f9f9; border-left: 4px solid #2d6a4f; 
                      padding: 15px; margin: 15px 0; border-radius: 5px; }
            .section h3 { color: #1a472a; margin-bottom: 10px; }
            .download-btn { display: inline-block; margin-top: 20px; padding: 12px 30px; 
                           background: #e63946; color: white; border-radius: 8px; 
                           text-decoration: none; font-size: 16px; text-align: center;
                           width: 100%; }
            .spinner { font-size: 2em; animation: spin 1s linear infinite; 
                      display: inline-block; }
            @keyframes spin { 0% { transform: rotate(0deg); } 
                             100% { transform: rotate(360deg); } }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧬 BioMed AI</h1>
            <p class="subtitle">Gene Analysis • Medical Reports • Drug Discovery</p>
            
            <div class="card">
                <input type="text" id="gene" placeholder="Gene ka naam likho (e.g. BRCA1, TP53, EGFR)" />
                <button onclick="analyze()">Analyze Karo</button>
                
                <div id="loading">
                    <span class="spinner">⚙️</span>
                    <p>Teen agents kaam kar rahe hain... thoda wait karo!</p>
                </div>
                
                <div id="result">
                    <div class="section">
                        <h3>📋 Medical Report</h3>
                        <div id="report"></div>
                    </div>
                    <div class="section">
                        <h3>💊 Drug Information</h3>
                        <div id="drugs"></div>
                    </div>
                    <a id="pdf-link" class="download-btn" href="#" download>
                        📥 PDF Download Karo
                    </a>
                </div>
            </div>
        </div>
        
        <script>
            async function analyze() {
                const gene = document.getElementById('gene').value.trim();
                if (!gene) { alert('Gene ka naam likho!'); return; }
                
                document.getElementById('loading').style.display = 'block';
                document.getElementById('result').style.display = 'none';
                
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({gene_name: gene})
                });
                
                const data = await response.json();
                
                document.getElementById('loading').style.display = 'none';
                document.getElementById('report').innerText = data.report;
                document.getElementById('drugs').innerText = data.drugs_info;
                document.getElementById('pdf-link').href = '/download/' + gene;
                document.getElementById('result').style.display = 'block';
            }
        </script>
    </body>
    </html>
    """

@app.post("/analyze")
async def analyze(request: GeneRequest):
    gene_name = request.gene_name.upper()
    
    gene_data = analyze_gene(gene_name)
    if "error" in gene_data:
        return {"error": gene_data["error"]}
    
    report = write_medical_report(gene_data)
    drugs = find_drugs(gene_data)
    generate_pdf(gene_name, report, drugs['drugs_info'])
    
    return {
        "gene_name": gene_name,
        "report": report,
        "drugs_info": drugs['drugs_info']
    }

@app.get("/download/{gene_name}")
async def download(gene_name: str):
    filepath = f"reports/{gene_name.upper()}_medical_report.pdf"
    if os.path.exists(filepath):
        return FileResponse(filepath, 
                          media_type="application/pdf",
                          filename=f"{gene_name}_report.pdf")
    return {"error": "PDF nahi mila"}

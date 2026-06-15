from Bio import Entrez, SeqIO
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

Entrez.email = os.getenv("NCBI_EMAIL")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_gene(gene_name: str) -> dict:
    print(f" {gene_name} ko NCBI mein search kar raha hoon...")
    
    #step 1: Gene ID dhundho
    handle = Entrez.esearch(db="gene",term=f"{gene_name}[Gene Name] AND Homo sapiens[Organism]")
    record = Entrez.read(handle)
    handle.close()
 
    if not record["IdList"]:
        return {"error" : f"{gene_name} nahi mila NCBI mein"}
    
    gene_id =record["IdList"][0]
    print(f" Gene ID mila: {gene_id}")

    #step 2 Gene ki details lo
    handle = Entrez.efetch(db="gene" ,id=gene_id,rettype="gene_table",retmode="text")
    gene_info = handle.read()
    handle.close()
    

    #step 3 : Groq AI se analysis lo
    print("AI se analysis le raha hoon...")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role":"user",
            "content":f"""
           Gene ka naam:{gene_name}
           Gene ID: {gene_id}
           Gene Information: {gene_info[:2000]}
          
         Is gene ke bare mein batao:
         1. ye gene kya kaam karta hai?
         2. Kaunsi bimari se related hai?
         3. Mutation hone pe kya hota hai?
         
        simple HINDI mein batao.
        """
    }]
)

    analysis = response.choices[0].message.content

    return {
        "gene_name": gene_name,
        "gene_id": gene_id,
        "analysis":analysis
     }

#Test karo 
if __name__ == "__main__":
    result=analyze_gene("BRCA1")
    print("\n" +"="*50)
    print("GENE ANALYSIS RESULT:")
    print("="*50)
    print(f"Gene :{result['gene_name']}")
    print(f"ID:{result['gene_id']}")
    print(f"\nAnalysis:\n{result['analysis']}")


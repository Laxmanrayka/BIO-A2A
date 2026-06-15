from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client=Groq(api_key=os.getenv("GROQ_API_KEY"))

def write_medical_report(gene_data:dict) -> str:
    print("Medical report likh raha hoon...")
    
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role":"user",
            "content":f"""
            Neche diye gene analysis ke basis pe ek simple medical report banao.
           
            Gene:{gene_data['gene_name']}
            Gene ID:{gene_data['gene_id']}
            Analysis :{gene_data['analysis']}
  
            Report ka format:
          
            MEDICAL REPORT
            ==============
            Patient Gene Analysis
   
            Gene Name:...
            Risk Level:(High/Medium/Low)

            Summary: (2-3 lines mein simple explanation)
            
            Doctor ke liye notes:(kya  dhyan rakhna chaiye)
            
            patient ke liye advice: (simple bhasha mein)
      
            simple aur clear bhasha mein likho.
            """
       }]
)

    return response.choices[0].message.content

if __name__ == "__main__":
    #DNA Research Agent ka data use karo
    test_data= {
        "gene_name" :"BRCA1",
        "gene_id" : "672",
        "analysis" : "BRCA1 gene DNA repair karta hai .Mutation hone pe breast aur  ovarion cancer ka risk badh jata hai."
    }

    report = write_medical_report(test_data)
    print("\n" + "="*50)
    print(report)


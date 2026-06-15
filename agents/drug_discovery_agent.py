from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client =Groq(api_key=os.getenv("GROQ_API_KEY"))

def find_drugs(gene_data:dict) -> dict:
    print(f"Drugs dhundh raha hoon {gene_data['gene_name']} ke liye...")
    
    response=client.chat.completions.create(
       model="llama-3.3-70b-versatile",
       messages=[{
           "role":"user",
           "content":f"""
           Gene :{gene_data['gene_name']}
           Gene ID:{gene_data['gene_id']}
           Analysis:{gene_data['analysis']}

           Is gene se related bimari ke liye
           1. Kaunsi approved drugs hai (naam aur kaam batao)
           2. Har drug ke side effects kya hai?
           3. Koi nai research ya drugs jo trial mein hain?
   
           Simple Hindi/English mein batao.
           """
       }]
    )

    drugs_info = response.choices[0].message.content

    return {
        "gene_name":gene_data['gene_name'],
        "drugs_info":drugs_info
    }

if __name__ =="__main__":
    test_data ={
         "gene_name": "BRCA1",
         "gene_id": "672",
         "analysis": "BRCA1 gene mutation se breast aur ovarion cancer ka risk badh jata hai"
  }

    result =find_drugs(test_data)
    print("\n"+"="*50)
    print("DRUGH DISCOVERY RESULT:")
    print("="*50)
    print(result['drugs_info'])

    

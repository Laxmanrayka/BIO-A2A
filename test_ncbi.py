from Bio import Entrez
from dotenv import load_dotenv
import os

load_dotenv()

Entrez.email = os.getenv("NCBI_EMAIL")

handle = Entrez.esearch(db="gene" , term ="BRCA1[Gene Name] AND Homo sapiens[Organism]")
record = Entrez.read(handle)
handle.close()

print("NCBI connected!")
print("BRCA1 Gene ID:",record["IdList"][0])


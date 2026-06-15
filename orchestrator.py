from agents.dna_research_agents import analyze_gene
from agents.report_writer_agent import write_medical_report
from agents.drug_discovery_agent import find_drugs

def run_pipeline(gene_name: str):
    print(f"\n{'='*50}")
    print(f"PIPELINE START: {gene_name}")
    print(f"{'='*50}\n")

    # Step 1: DNA Research Agent
    print("STEP 1: DNA Research Agent...")
    gene_data = analyze_gene(gene_name)

    if "error" in gene_data:
        print(f"Error: {gene_data['error']}")
        return

    # Step 2: Report Writer Agent
    print("\nSTEP 2: Report Writer Agent...")
    report = write_medical_report(gene_data)

    # Step 3: Drug Discovery Agent
    print("\nSTEP 3: Drug Discovery Agent...")
    drugs = find_drugs(gene_data)

    # Final Output
    print(f"\n{'='*50}")
    print("FINAL MEDICAL REPORT:")
    print(f"{'='*50}")
    print(report)
    print(f"\n{'='*50}")
    print("DRUG INFORMATION:")
    print(f"{'='*50}")
    print(drugs['drugs_info'])

if __name__ == "__main__":
    gene = input("Gene ka naam likho (e.g. BRCA1, TP53): ")
    run_pipeline(gene)


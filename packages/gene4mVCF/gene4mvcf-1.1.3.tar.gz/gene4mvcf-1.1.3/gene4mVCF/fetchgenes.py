import argparse
import subprocess
import os
import gzip
from tqdm import tqdm

def parse_bed_file(gene_identifier, genome_version):
    if "GRCh38" in genome_version:
        if gene_identifier.startswith("ENSG"):
            bed_file = "hg38.ensGene.bed"
        else:
            bed_file = "hg38.ncbiRefSeq.bed"
    elif "GRCh37" in genome_version or "hg19" in genome_version:
        if gene_identifier.startswith("ENSG"):
            bed_file = "hg19.ensGene.bed"
        else:
            bed_file = "hg19.ncbiRefSeq.bed"
    else:
        # Default to hg19 if genome version cannot be determined
        if gene_identifier.startswith("ENSG"):
            bed_file = "hg19.ensGene.bed"
        else:
            bed_file = "hg19.ncbiRefSeq.bed"
    
    #print("Detected genome version:", genome_version)
    print("Selected BED file:", bed_file)  # Add this line for debugging

    gene_regions = {}
    with open(bed_file, 'r') as file:
        for line in file:
            fields = line.strip().split('\t')
            chrom = fields[0].lstrip("chr")
            start = int(fields[1])
            end = int(fields[2])
            gene_name = fields[3]
            feature = fields[7]

            if gene_identifier.startswith("ENSG"):
                if fields[3] == gene_identifier:
                    gene_regions[(chrom, start, end)] = (gene_name, feature)
            else:
                if fields[3] == gene_identifier:
                    gene_regions[(chrom, start, end)] = (gene_name, feature)

    if not gene_regions:
        raise ValueError(f"Gene {gene_identifier} not found in {bed_file}")
    return gene_regions

def get_reference_genome(vcf_path):
    reference_genome = None
    with gzip.open(vcf_path, 'rt') as file:
        for line in file:
            if line.startswith("##contig="):
                if "assembly=gnomAD_GRCh38" in line:
                    reference_genome = "GRCh38"
                elif "assembly=GRCh38" in line:
                    reference_genome = "GRCh38"
                break
            elif line.startswith("#CHROM"):
                reference_genome = "GRCh38"  # Default to GRCh37, as genome version could not be determine from the given vcf file
                break
                
    if reference_genome is None:
        # Default to GRCh37 if genome version cannot be determined
        reference_genome = "GRCh37"
        print("Reference genome could not be determined from the VCF file, defaulting to GRCh37")

    return reference_genome

def get_gene_info(chrom, pos, gene_regions):
    for (region_chrom, start, end), (gene_name, feature) in gene_regions.items():
        if region_chrom == chrom and start <= pos <= end:
            return gene_name, feature
    return "", ""

def main():
    parser = argparse.ArgumentParser(description='Extract variant entries for a specific gene or list of genes from a VCF file.')
    parser.add_argument('-i', '--input', required=True, help='Input VCF file')
    parser.add_argument('-g', '--genes', required=True, help='Gene name, Ensembl gene ID, or path to a gene list file')

    args = parser.parse_args()

    genome_version = get_reference_genome(args.input)

    if genome_version:
        print(f"Reference genome version of the input vcf file: {genome_version}")

    if args.genes.endswith('.txt'):
        with open(args.genes, 'r') as gene_list_file:
            gene_list = [line.strip() for line in gene_list_file]
    else:
        gene_list = [args.genes]

    gene_regions = {}
    for gene_identifier in gene_list:
        gene_regions.update(parse_bed_file(gene_identifier, genome_version))

    # Create index file for the input VCF file
    index_file = args.input + ".tbi"
    if not os.path.exists(index_file):
        subprocess.run(["tabix", "-p", "vcf", args.input], check=True)

    output_vcf = f"{os.path.splitext(args.input)[0]}_{'_'.join(gene_list)}.vcf"
    region = ','.join([f'{chrom}:{start}-{end}' for (chrom, start, end) in gene_regions])
    cmd = f"bcftools view -r {region} -o {output_vcf} {args.input}"
    subprocess.run(cmd, shell=True, check=True)

    # Count the number of variants in the output VCF file
    variant_count = sum(1 for line in open(output_vcf) if not line.startswith("#"))

    output_tsv = f"{os.path.splitext(output_vcf)[0]}.tsv"
    with open(output_tsv, 'w') as tsv_out:
        tsv_out.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tGene_Name\tFeature\n")
        with open(output_vcf, 'r') as vcf_in:
            for line in vcf_in:
                if not line.startswith("#"):  # Skip header lines
                    fields = line.strip().split('\t')
                    chrom = fields[0]
                    pos = int(fields[1])
                    gene_name, feature = get_gene_info(chrom, pos, gene_regions)
                    tsv_out.write(f"{chrom}\t{pos}\t{fields[2]}\t{fields[3]}\t{fields[4]}\t{fields[5]}\t{fields[6]}\t{fields[7]}\t{gene_name}\t{feature}\n")

    os.remove(output_vcf)

    print(f"{variant_count} variants were found in the genes {', '.join(gene_list)} in the given input file.")

if __name__ == '__main__':
    main()


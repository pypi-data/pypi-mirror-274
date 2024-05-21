# gene4mVCF

## Introduction
`gene4mVCF` is a Python package that allows you to extract variant entries for specific genes or a list of genes from a VCF (Variant Call Format) file. It utilizes tools like `bcftools`, `tabix`, and Python libraries like `pysam`, `pandas`, `pybedtools`, `tqdm`, and `gffutils` to efficiently parse and extract variants.

## Installation

You can install `gene4mVCF` via pip:

`$ pip install gene4mVCF`

## Usage
usage: `$ gene4mVCF [-h] -i INPUT -g GENE`

Extract variant entries for a specific gene or list of genes from a VCF file.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input bgzip compressed VCF file
  -g GENES, --genes GENES
                        Gene name, Ensembl gene ID, or path to a gene list file

## Examples
Extract variants for a single gene using gene name:
`$ gene4mVCF -i input.vcf.gz -g EGFR`

Extract variants for a single using ensembl gene id:
`$ gene4mVCF -i input.vcf.gz -g ENSG00000168878`

Extract variants for multiple genes listed in a file:
`$ gene4mVCF -i input.vcf.gz -g genes.txt`

For more options and details, refer to the help message.

## Support
For any issues or inquiries, please open an issue on the GitHub repository https://github.com/VJ-Ulaganathan/gene4mVCF


## Installation

Installation via pip:

`$ pip install gene4mVCF`




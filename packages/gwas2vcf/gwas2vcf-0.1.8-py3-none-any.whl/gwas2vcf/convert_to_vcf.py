##code for converting UK BioBank GWAS file to standard VCF4.0 format.
##If you found our code useful, please consider following me on https://x.com/VK_Ulaganathan

import pandas as pd
import gzip
import argparse
from tqdm import tqdm

def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert GWAS file VCF format.")
    parser.add_argument("-i", "--input", required=True, help="please provide the path for the input file with the extension .bgz")
    parser.add_argument("-o", "--output", required=True, help="please provide desire output file name, tool will automatically append the .vcf.gz extension")
    return parser.parse_args()

def main():
    args = parse_arguments()
    input_file = args.input
    output_file = args.output

    # Ensure the output file has the correct .vcf.gz extension
    if not output_file.endswith(".vcf.gz"):
        output_file += ".vcf.gz"

    # Read the input file
    with gzip.open(input_file, 'rt') as f:
        df = pd.read_csv(f, sep='\t')

    # Split the 'variant' column into 'CHROM', 'POS', 'REF', and 'ALT'
    df[['CHROM', 'POS', 'REF', 'ALT']] = df['variant'].str.split(':', expand=True)

    # Define the VCF header
    vcf_header = [
        "##fileformat=VCFv4.0",
        "##source=GWAS",
        "##INFO=<ID=AC,Number=A,Type=Integer,Description=\"Alternate Allele Count\">",
        "##INFO=<ID=AF,Number=A,Type=Float,Description=\"Alternate Allele Frequency\">",
        "##INFO=<ID=AN,Number=1,Type=Integer,Description=\"Total Number of Alleles\">",
        "##INFO=<ID=low_confidence,Number=0,Type=Flag,Description=\"Low Confidence Variant\">",
        "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tsample"
    ]

    # Open the output VCF file for writing
    with gzip.open(output_file, 'wt') as vcf:
        # Write the VCF header
        for line in vcf_header:
            vcf.write(line + '\n')
        
        # Write the VCF body with progress bar
        for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing rows"):
            info_fields = [
                f"AC={int(row['AC'])}",
                f"AF={float(row['minor_AF'])}",
                f"AN={2 * int(row['n_complete_samples'])}"  # assuming diploid samples
            ]
            if row['low_confidence_variant'] == 'true':
                info_fields.append("low_confidence")
            
            info_str = ";".join(info_fields)
            format_str = "GT"
            sample_str = "./."

            vcf_row = [
                row['CHROM'],
                row['POS'],
                '.',
                row['REF'],
                row['ALT'],
                '.',
                'PASS' if row['low_confidence_variant'] == 'false' else 'LowQual',
                info_str,
                format_str,
                sample_str
            ]
            
            vcf.write("\t".join(vcf_row) + '\n')

if __name__ == "__main__":
    main()


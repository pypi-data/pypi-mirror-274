import argparse
import requests
import json

class Annobee:
    def __init__(self, endpoint='http://localhost:5000/api/interpret'):
        self.endpoint = endpoint

    def get_criteria(self, variant):
        """ Sends a POST request to the Flask API with the variant details. """
        try:
            response = requests.post(self.endpoint, json={
                'variant': variant,
                'genome_build': 'hg38',  # default genome build
                'adjustments': {}        # default adjustments if any
            })
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description='Genetic Variant Analysis CLI')
    parser.add_argument('variant', type=str, help='Variant in the format chr-pos-ref-alt, e.g., 1-12345-A-G')
    parser.add_argument('--endpoint', type=str, default='http://localhost:5000/api/interpret', help='API endpoint to use')

    # Add argument options for all individual and aggregate criteria
    criteria_keys = [
        'functional_consequence', 'hgvsp', 'aa_change', 'transcript_id', 'ucsc_trans_id',
        'exon_number', 'start', 'end', 'rmsk', 'clinvar_clnsig', 'clinvar_clnrevstat',
        'af_esp', 'af_exac', 'af_tgp', 'dbscsnv_rf_score', 'dbscsnv_ada_score', 'gerp_rs_score',
        'metasvm_score', 'sift_score', 'af_vep', 'va_pathogenicity', 'interpro_domain',
        'gene', 'ensembl_gene_id', 'vep_gene_id', 'max_af', 'hgnc_id', 'hgnc_src',
        'pvs1', 'ba1'
    ]

    # Add arguments for aggregate criteria
    aggregate_criteria = ['ps', 'pm', 'pp', 'bs', 'bp']
    for key in criteria_keys + aggregate_criteria:
        parser.add_argument(f'-{key}', action='store_true', help=f'Return {key.upper()} criteria')

    args = parser.parse_args()

    # Extract variant details from command-line arguments
    try:
        chrom, pos, ref, alt = args.variant.split('-')
        variant = {
            'CHROM': 'chr' + chrom,
            'POS': int(pos),
            'REF': ref,
            'ALT': alt
        }
    except ValueError:
        print("Error: Variant must be in the format 'chr-pos-ref-alt'. Example: chr1-12345-A-G")
        return

    annobee = Annobee(endpoint=args.endpoint)
    variant_info = annobee.get_criteria(variant)

    if 'error' in variant_info:
        print(variant_info['error'])
    else:
        results = {}
        info = variant_info.get('INFO', {})
        # Process and display requested information
        for key in criteria_keys + aggregate_criteria:
            if getattr(args, key):  # If the specific criteria flag is set
                if key in aggregate_criteria:
                    results[key.upper()] = info.get(key, [])
                else:
                    results[key.upper()] = info.get(key, 'Not available')

        print(json.dumps(results, indent=4))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
This program inserts WP3-mapped data from a provided json file
into the postgres database used by the reference Beacon 2.0 implementation.
"""
import argparse
import csv
import datetime
import json
import sys
import vcf
import dateutil.relativedelta

def vcf_samples(vcffile):
    """
    Samples from vcf file if present
    """
    try:
        vcf_reader = vcf.Reader(open(vcffile, 'r'))
        return vcf_reader.samples
    except Exception as error:
        print(f"Could not read vcffile {vcffile}: continuing without vcf data: {str(error)}")

    return []


def main():
    """
    Parse arguments, make database connection, read file, and start ingest
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("datafile", help="Name of JSON file containing WP3-mapped metadata")
    parser.add_argument("csvfile", help="Corrected CSV file")
    parser.add_argument("vcffile", help="VCF file with samples")
    args = parser.parse_args()

    samples = vcf_samples(args.vcffile)

    with open(args.datafile, 'r') as infile:
        data = json.load(infile)

    if not data:
        print(f"Error reading data file {args.datafile}.", file=sys.stderr)
        return

    now = datetime.datetime.now()
    with open(args.csvfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader):
            data[idx]["physiologicalMeasurements"]["anthropometry"]["weight"] = [float(row['birth_weight_g'])/1000., float(row['sbjt_weight_kg'])]
            data[idx]["physiologicalMeasurements"]["anthropometry"]["height"] = [float(row['height_cm']), float(row['sbjt_length_cm'])]
            data[idx]["physiologicalMeasurements"]["circulationAndRespiration"]["bloodPressure"] = [float(row['sbjt_blood_pressure_systolic'])]
            if len(samples) > idx:
                data[idx]["sample"] = samples[idx]

            dob = datetime.datetime.strptime(data[idx]["demographic"]["age"], "%d-%b-%y")
            data[idx]["demographic"]["age"] = dateutil.relativedelta.relativedelta(now, dob).years

    print(json.dumps(data))


if __name__ == "__main__":
    main()

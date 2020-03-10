#!/usr/bin/env python3
"""
This program inserts WP3-mapped data from a provided json file
into the postgres database used by the reference Beacon 2.0 implementation.
"""
import argparse
import sys
import psycopg2 as pg
import vcf


def clear_tables(connection, cursor):
    """
    Rmove initial data if any from existing tables
    """
    cursor.execute("TRUNCATE TABLE variants, calls")
    connection.commit()

    return


def ingest_variants(connection, cursor, vcffile, nvar):
    """
    Given the Postgres connection, and a cursor,
    insert the variants from the vcf file into the postgres database.
    """
    count = 0

    vcf_reader = vcf.Reader(open(vcffile, 'r'))
    for record in vcf_reader:
        has_var = [call.sample for call in record.samples if call.is_variant]
        if not has_var:
            continue

        allele_fraction = 0
        if "AF" in record.INFO:
            allele_fraction = record.INFO["AF"][0]

        gene = ""
        if "GENE" in record.INFO:
            gene = record.INFO["GENE"]

        startpos = record.POS
        chrom, ref, alt = record.CHROM, record.REF, str(record.ALT[0])
        endpos = startpos + len(ref) - 1
        cursor.execute("""INSERT INTO variants(variant_id, chromosome, reference, alternate, start, "end", gene, AF)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            RETURNING id""",
                        (record.ID, chrom, ref, alt, startpos, endpos, gene, allele_fraction))
        variant_id = cursor.fetchone()[0]

        samples_w_variant = [(variant_id, samp, '/'.join(record.genotype(samp).gt_alleles)) for samp in has_var]
        cursor.executemany("""INSERT INTO calls(variant_id, sample_id, call)
                                VALUES(%s,%s,%s)""", samples_w_variant)
        count += 1
        if count % 100 == 0:
            print(count)
        if count % nvar == 0:
            break

        connection.commit()


def main():
    """
    Parse arguments, make database connection, read file, and start ingest
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="Postgres server hostname", default="0.0.0.0")
    parser.add_argument("--port", help="Postgres server port", default=5432)
    parser.add_argument("--username", help="Postgres username", default="search")
    parser.add_argument("--password", help="Postgres password", default="secretpassword")
    parser.add_argument("--database", help="Postgres database", default="search")
    parser.add_argument("-n", help="Number of variants", type=int, default=1000)
    parser.add_argument("vcffile", help="VCF file", default=None)
    args = parser.parse_args()

    connection = None
    try:
        connection = pg.connect(user=args.username,
                                password=args.password,
                                host=args.server,
                                port=args.port,
                                database=args.database)
        cursor = connection.cursor()
    except (Exception, pg.Error) as error:
        print("Error while connecting to PostgreSQL", error, file=sys.stderr)
        if connection:
            cursor.close()
            connection.close()

    if not connection:
        return

    clear_tables(connection, cursor)
    ingest_variants(connection, cursor, args.vcffile, args.n)


if __name__ == "__main__":
    main()

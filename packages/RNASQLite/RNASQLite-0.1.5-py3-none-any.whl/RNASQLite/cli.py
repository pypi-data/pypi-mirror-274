import argparse
import os
import pkg_resources
from RNASQLite.db_utils import setup_database, insert_counts_into_db, get_count_files, fetch_all_samples
from RNASQLite.process_file import process_file

def main():
    parser = argparse.ArgumentParser(description='RNASQLite command line tool')
    parser.add_argument('-create', action='store_true', help='Create the SQLite database')
    parser.add_argument('-split', type=str, help='Process RNAseq counts file and split into count files')
    parser.add_argument('-load', action='store_true', help='Load counts files into the database')
    parser.add_argument('-fetch', action='store_true', help='Fetch all samples from the database')
    args = parser.parse_args()

    db_path = 'geo_rna_seq.db'  # SQLite 데이터베이스 파일 경로
    counts_dir = 'counts'  # Counts 파일이 저장될 디렉토리

    if args.create:
        setup_database(db_path)
    elif args.split:
        rna_seq_counts_path = args.split
        # 패키지 내부에서 gene_info.csv 파일 경로를 찾습니다
        gene_info_path = pkg_resources.resource_filename(__name__, 'gene_info.csv')
        if not os.path.isfile(gene_info_path):
            print(f"Error: {gene_info_path} file not found.")
            return
        process_file(gene_info_path, rna_seq_counts_path, counts_dir)
    elif args.load:
        count_files = get_count_files(counts_dir)
        insert_counts_into_db(db_path, count_files)
    elif args.fetch:
        fetch_all_samples(db_path)
    else:
        print("Invalid command. Use -create, -split <file>, -load, or -fetch.")

if __name__ == '__main__':
    main()

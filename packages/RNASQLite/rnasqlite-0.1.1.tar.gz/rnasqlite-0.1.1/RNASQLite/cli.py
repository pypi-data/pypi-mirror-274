import argparse
import os  # os 모듈을 임포트합니다.
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
        gene_info_path = os.path.join(os.path.dirname(__file__), '..', 'gene_info.csv')  # gene_info 파일 경로를 고정
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

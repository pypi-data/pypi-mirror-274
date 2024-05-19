import pandas as pd
import os

def process_file(gene_info_path, rna_seq_counts_path, output_dir='counts'):
    # gene_info 파일 읽기
    gene_info_df = pd.read_csv(gene_info_path)

    # rna_seq_counts 파일 확장자 확인
    file_extension = os.path.splitext(rna_seq_counts_path)[1]

    # 확장자에 따라 파일 읽기
    if file_extension == '.csv':
        rna_seq_counts_df = pd.read_csv(rna_seq_counts_path)
    elif file_extension == '.tsv':
        rna_seq_counts_df = pd.read_csv(rna_seq_counts_path, sep='\t')
    else:
        raise ValueError("지원하지 않는 파일 형식입니다. CSV 또는 TSV 파일을 사용해 주세요.")

    # gene_id 열이 ENSG 형식인지 여부를 판단
    is_ensg = rna_seq_counts_df['gene_id'].str.startswith('ENSG')

    # gene_id가 ENSG 형식이 아닌 경우, 이를 gene_name으로 간주
    rna_seq_counts_df['gene_name'] = rna_seq_counts_df['gene_id'].where(~is_ensg, None)
    rna_seq_counts_df['gene_id'] = rna_seq_counts_df['gene_id'].where(is_ensg, None)

    # gene_info 파일에서 gene_id와 gene_name을 매칭하여 채우기
    merged_df = rna_seq_counts_df.merge(gene_info_df[['gene_name', 'gene_id']], how='left', on='gene_name', suffixes=('', '_info'))
    merged_df['gene_id'] = merged_df['gene_id'].combine_first(merged_df['gene_id_info']).fillna('')
    merged_df.drop(columns=['gene_id_info'], inplace=True)

    # 빈 gene_name을 gene_info에서 채우기
    merged_df = merged_df.merge(gene_info_df[['gene_name', 'gene_id']], how='left', on='gene_id', suffixes=('', '_info'))
    merged_df['gene_name'] = merged_df['gene_name'].combine_first(merged_df['gene_name_info']).fillna('')
    merged_df.drop(columns=['gene_name_info'], inplace=True)

    # 열 순서 조정 (gene_id, gene_name을 첫 번째와 두 번째 열로 이동)
    merged_df = merged_df[['gene_id', 'gene_name'] + [col for col in merged_df.columns if col not in ['gene_id', 'gene_name']]]

    # Count 파일 저장 디렉토리 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 각 열을 개별 파일로 저장 (gene_id, gene_name 열 제외)
    base_filename = os.path.splitext(os.path.basename(rna_seq_counts_path))[0]
    count_files = {}

    for column in merged_df.columns[2:]:  # gene_id와 gene_name 열 제외
        output_path = os.path.join(output_dir, f"{base_filename}_{column}_counts.csv")
        single_column_df = merged_df[['gene_id', 'gene_name', column]]
        single_column_df.to_csv(output_path, index=False)
        count_files[column] = output_path

        # 두 번째 열 확인 후 숫자가 아니면 파일 삭제 및 경고 메시지 출력
        second_column_values = single_column_df[column]
        if not pd.api.types.is_numeric_dtype(second_column_values):
            print(f"경고: {output_path} 파일의 두 번째 열이 숫자가 아닙니다. 파일을 삭제합니다.")
            os.remove(output_path)
            del count_files[column]

    return count_files

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Process RNAseq counts file and gene info file.')
    parser.add_argument('rna_seq_counts_path', type=str, help='Path to the RNAseq counts file (CSV or TSV).')
    args = parser.parse_args()

    gene_info_path = os.path.join(os.path.dirname(__file__), '..', 'gene_info.csv')  # gene_info 파일 경로를 고정

    count_files = process_file(gene_info_path, args.rna_seq_counts_path)
    for sample, path in count_files.items():
        print(f"Sample: {sample}, File: {path}")

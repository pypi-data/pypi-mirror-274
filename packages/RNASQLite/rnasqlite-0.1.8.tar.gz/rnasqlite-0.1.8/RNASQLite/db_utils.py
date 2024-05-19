import sqlite3
import os
import pandas as pd

def setup_database(db_path):
    # 데이터베이스 연결 (db 파일이 없으면 새로 생성됨)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 테이블 생성
    c.execute('''
    CREATE TABLE IF NOT EXISTS samples (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        GSE_number TEXT,
        sample_ID TEXT,
        count_path TEXT,
        UNIQUE(GSE_number, sample_ID)
    )
    ''')

    # 변경사항 저장
    conn.commit()
    # 연결 종료
    conn.close()
    print("데이터베이스 생성이 완료되었습니다.")

def insert_counts_into_db(db_path, count_files):
    # 데이터베이스 연결
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 데이터 삽입
    for count_file_path in count_files:
        # 파일명에서 정보 추출
        filename = os.path.basename(count_file_path)
        parts = filename.split('_')
        
        if len(parts) >= 3:
            GSE_number = parts[0]
            sample_ID = parts[-2]
            count_path = count_file_path
        else:
            print(f"Invalid filename format: {filename}")
            continue

        # 중복 확인
        c.execute('''
            SELECT COUNT(*) FROM samples WHERE GSE_number = ? AND sample_ID = ?
        ''', (GSE_number, sample_ID))
        result = c.fetchone()

        if result[0] == 0:
            # 중복이 아닐 경우 데이터 삽입
            c.execute('''
                INSERT INTO samples (GSE_number, sample_ID, count_path)
                VALUES (?, ?, ?)
            ''', (GSE_number, sample_ID, count_path))
        else:
            print(f"Duplicate entry found for GSE_number: {GSE_number}, sample_ID: {sample_ID}. Skipping insertion.")

    # 변경사항 저장
    conn.commit()
    # 연결 종료
    conn.close()
    print("데이터베이스에 데이터 삽입이 완료되었습니다.")

def get_count_files(counts_dir):
    # counts 디렉토리의 모든 파일 경로 가져오기
    count_files = [os.path.join(counts_dir, f) for f in os.listdir(counts_dir) if os.path.isfile(os.path.join(counts_dir, f))]
    return count_files

def fetch_all_samples(db_path):
    # 데이터베이스 연결
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 데이터 조회
    c.execute('SELECT * FROM samples')
    rows = c.fetchall()

    # 데이터 출력
    for row in rows:
        print(row)

    # 연결 종료
    conn.close()
    
def fetch_filtered_samples(db_path, column_name, identifier_value):
    # SQLite 데이터베이스 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 특정 열 이름과 값에 따라 count_path 가져오기
    query = f"SELECT count_path FROM samples WHERE {column_name} = ?"
    cursor.execute(query, (identifier_value,))
    csv_files = [row[0] for row in cursor.fetchall()]

    # 데이터베이스 연결 종료
    conn.close()

    if not csv_files:
        print(f"No files found for {column_name} = {identifier_value}")
        return

    # 고정된 선택할 열 이름 지정
    columns_to_select = ["gene_id", "gene_name"]

    # 첫 번째 파일로 기준 데이터프레임 생성
    base_df = pd.read_csv(csv_files[0])
    base_df = base_df.sort_values(by=columns_to_select)
    base_first_two_cols = base_df[columns_to_select]

    # 다른 파일들과 공통된 부분 찾기
    for file in csv_files[1:]:
        df = pd.read_csv(file)
        df = df.sort_values(by=columns_to_select)
        first_two_cols = df[columns_to_select]
        
        # 공통된 부분 추출
        base_first_two_cols = pd.merge(base_first_two_cols, first_two_cols, on=columns_to_select)

    # 최종 공통된 부분을 기준으로 데이터 추출
    common_data = base_first_two_cols
    merged_df = common_data.copy()

    for file in csv_files:
        df = pd.read_csv(file)
        df = df.sort_values(by=columns_to_select)
        third_col = df.iloc[:, 2]
        
        # 공통된 부분에 대한 데이터 추출 및 결합
        third_col_common = pd.merge(common_data, df, on=columns_to_select)[df.columns[2]]
        
        # 추출한 데이터를 통합 데이터프레임에 추가
        merged_df = pd.concat([merged_df, third_col_common.reset_index(drop=True)], axis=1)

    # 열 이름 설정 (gene_id, gene_name, IDD-1, IDD-2, ...)
    columns = columns_to_select + [f'{csv_files[i].split("_")[-2]}' for i in range(len(csv_files))]
    merged_df.columns = columns

    # 통합 CSV 파일로 저장
    output_file = "filtered_output.csv"
    merged_df.to_csv(output_file, index=False)

    print(f"Filtered samples saved to '{output_file}'.")
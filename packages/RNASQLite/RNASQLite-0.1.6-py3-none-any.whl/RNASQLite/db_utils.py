import sqlite3
import os

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

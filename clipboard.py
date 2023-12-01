import sqlite3
import pandas as pd
import re
import os

def clipboardDB_wiping(destination_dir,folder_name,clipboard_name):
    # 데이터베이스 파일 경로 설정
    db_path = os.path.join(destination_dir,folder_name,clipboard_name) #수정필요

    # db_path = destination_dir+'./databases/ClipItem.db' #수정필요

    # 데이터베이스 연결
    conn = sqlite3.connect(db_path)

    # 커서 생성 및 쿼리 실행
    query = """
        SELECT 
            id, 
            strftime('%Y-%m-%d %H:%M:%S', datetime(time_stamp / 1000, 'unixepoch', 'localtime')) AS formatted_time_stamp,
            type, 
            text, 
            html, 
            uri, 
            uri_list,
            mime_type
        FROM clip_table
        WHERE type IN (1, 2, 4)
        ORDER BY time_stamp
    """
    cur = conn.cursor()
    cur.execute(query)

    # 결과를 DataFrame으로 변환
    rows = cur.fetchall()
    cols = [column[0] for column in cur.description]
    clip_table_df = pd.DataFrame.from_records(data=rows, columns=cols)

    # 데이터베이스 연결 종료
    conn.close()


    # 정규 표현식을 사용하여 특정 패턴 필터링
    pattern = re.compile(r'^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}$')

    # type이 1인 레코드 필터링 및 'clipboard has been wiped' 메시지 확인
    filtered_df_1 = clip_table_df[clip_table_df['type'] == 1]
    clipboard_wiped = filtered_df_1['text'].str.match(pattern).any()

    # 특정 패턴이 존재하는 경우 'clipboard has been wiped' 메시지 출력
    if clipboard_wiped:
        print("clipboard has been wiped")


    # type이 1인 데이터 중 정규 표현식에 해당하지 않는 데이터 출력
    non_pattern_df_1 = filtered_df_1[~filtered_df_1['text'].str.match(pattern)]
    if not non_pattern_df_1.empty:
        print(non_pattern_df_1)

    # type이 2인 레코드에 대한 메시지 반복 출력
    for _, row in clip_table_df[clip_table_df['type'] == 2].iterrows():
        print(f"{row['mime_type']} image has been wiped. you can find your image at {row['uri']}")

    # type이 4인 레코드에 대한 메시지 반복 출력
    for _, row in clip_table_df[clip_table_df['type'] == 4].iterrows():
        print(f"html data has been wiped. you can find your image at {row['uri']}")
        print(f"and text data is this : {row['text']}")

def clipboardFile_wiping(folder_path):
    # UUID 형태의 정규 표현식 패턴 정의
    pattern = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    wiped_found = False

    # 주어진 폴더 안의 모든 하위 폴더를 순회
    for folder_name in os.listdir(folder_path):
        sub_folder_path = os.path.join(folder_path, folder_name)
        clip_file_path = os.path.join(sub_folder_path, "clip")
        # "clip" 파일이 존재하는지 확인
        if os.path.isfile(clip_file_path):
            with open(clip_file_path, 'r', encoding='ISO-8859-1') as file:
                content = file.read()
                matches = re.findall(pattern, content)
                for match in matches:
                    print(match)
                    wiped_found = True

    if wiped_found:
        print("This Clipboard has been wiped")

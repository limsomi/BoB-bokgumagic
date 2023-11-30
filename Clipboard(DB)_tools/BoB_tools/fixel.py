import sqlite3
import pandas as pd
import re
import subprocess
import os
import re

def uri_parsing(uri):
    pattern = re.compile(r'(com\.samsung\.android\.honeyboard/.*)')
    result = re.search(pattern, uri)
    if result==None:
        print(uri)
        pattern = re.compile(r'(com\.google\.android\.inputmethod\.latin\.fileprovider/.*)')
        result = re.search(pattern, uri)

    file_name=uri.split('/')
    pattern = re.compile(rf'{file_name[-1]}(?![a-zA-Z0-9])')

    # 정규 표현식을 사용하여 문자열 자르기
    try:
        midium = re.split(pattern, result.group(1), maxsplit=1)[0]
    except:
        print("result : "+result[0])
        midium=result
    return midium,file_name[-1]

def extract_data(path,destination_dir):

    try:
        copy_command=f'''adb shell "su -c 'cd {destination_dir} && cp -r {path} /sdcard'"'''
        subprocess.run(copy_command, shell=True, check=True)
        print("ADB command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing ADB command: {e}")

    try:
        pull_command=f"adb pull /sdcard/{path} clip"
        subprocess.run(pull_command, shell=True, check=True)
        print("ADB command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing ADB command: {e}")

def rename_clip_to_jpg(time_stamp,directory):
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            continue  
        if filename.startswith("clip"):
            # "clip"으로 시작하면서 ".jpg"로 끝나지 않는 파일을 찾아서 이름을 변경합니다.
            new_filename = filename.replace("clip", str(time_stamp)).strip("_") + ".jpg"
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            os.rename(old_path, new_path)
            print(f"이름을 변경했습니다: {filename} -> {new_filename}")



# 데이터베이스 파일 경로 설정
db_path = 'databases/gboard_clipboard.db'

# 데이터베이스 연결
conn = sqlite3.connect(db_path)

# 커서 생성 및 쿼리 실행
query = """
    SELECT 
        _id, 
        strftime('%Y-%m-%d %H:%M:%S', datetime(timestamp / 1000, 'unixepoch', 'localtime')) AS formatted_time_stamp,
        text, 
        html_text, 
        item_type, 
        entity_type,
        uri
    FROM clips
    ORDER BY timestamp
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
filtered_df_1 = clip_table_df[clip_table_df['uri'] =='']
clipboard_wiped = filtered_df_1['text'].str.match(pattern).any()

# 특정 패턴이 존재하는 경우 'clipboard has been wiped' 메시지 출력
if clipboard_wiped:
    print("clipboard has been wiped")


# type이 1인 데이터 중 정규 표현식에 해당하지 않는 데이터 출력
non_pattern_df_1 = filtered_df_1[~filtered_df_1['text'].str.match(pattern)]
if not non_pattern_df_1.empty:
    print(non_pattern_df_1)

# type이 2인 레코드에 대한 메시지 반복 출력
for _, row in clip_table_df[clip_table_df['uri'] !=''].iterrows():
    print(f"{row['item_type']} image has been wiped. you can find your image at {row['uri']}")
    midium,path_list=uri_parsing(row['uri'])
    destination_dir='/data/data/'+midium
    print(path_list,midium)
    if not os.path.exists('clip'):
        os.makedirs('clip')
    extract_data(path_list,destination_dir)
    rename_clip_to_jpg(row['_id'],"./clip")
# type이 4인 레코드에 대한 메시지 반복 출력
# for _, row in clip_table_df[clip_table_df['type'] == 4].iterrows():
#     print(f"html data has been wiped. you can find your image at {row['uri']}")
#     print(f"and text data is this : {row['text']}")
    # with open('clip.txt')
    #text 파일 만들기 
    #이미지 파일 크롤링



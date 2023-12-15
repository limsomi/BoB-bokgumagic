import sqlite3
import pandas as pd
import re
import os

def clipboardDB_wiping(destination_dir,folder_name,clipboard_name):
    db_path = os.path.join(destination_dir,folder_name,clipboard_name) 

    check_wiping=False


    # 데이터베이스 연결
    conn = sqlite3.connect(db_path)

    # 커서 생성 및 쿼리 실행
    query = """
        SELECT 
            id, 
            time_stamp,
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

    rows = cur.fetchall()
    cols = [column[0] for column in cur.description]
    clip_table_df = pd.DataFrame.from_records(data=rows, columns=cols)


    conn.close()


    pattern = re.compile(r'^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}$')

    wiping_data=pd.DataFrame(columns=['id','time_stamp','formatted_time_stamp','type','text','html','uri','uri_list','mime_type'])

    if clip_table_df['text'].str.match(pattern).any():
        check_wiping=True

    clip_table_df['wiping_check']=clip_table_df['text'].str.match(pattern)
    clip_table_df['group'] = (clip_table_df['wiping_check'] != clip_table_df['wiping_check'].shift(1)).cumsum()
    wipingPattern_group=clip_table_df.groupby('group')
    group_count=wipingPattern_group.ngroups
    for i in range(group_count):
        group=wipingPattern_group.get_group(i+1)
        if group['wiping_check'].iloc[0]==True and i!=0:
            add_df=wipingPattern_group.get_group(i)
            if wiping_data.empty:
                wiping_data=add_df
            else:
                wiping_data=pd.concat([wiping_data,add_df])

    wiping_image=wiping_data[wiping_data['mime_type']=='image/jpeg']
    wiping_data=wiping_data.copy()
    wiping_data['html']=wiping_data['html']!=''
    wiping_html=wiping_data[wiping_data['html']==True]
    for _,row in wiping_image.iterrows():
        original_path = f'./extractdata\com.samsung.android.honeyboard\clipboard' + row['uri'].split('clipboard')[1]

        file_name=row['uri'].split('clipboard')[1].split('/')[1]
        new_path = f'./result/clipboard/image/{file_name}.jpg'

        # 파일 이름 변경
        if os.path.exists(original_path):
            os.rename(original_path, new_path)

    for _,row in wiping_html.iterrows():
        time_stamp=row['time_stamp']
        with open(f'./result/clipboard/html/{time_stamp}.txt','w',encoding='utf-8') as html_file:
            html_file.write(row['text'])
    condition = (wiping_data['html'] == True) & (wiping_data['text'].str.count('\n') >1)
    wiping_data.loc[condition, 'text'] = 'BLOB'
    wiping_data=wiping_data.copy()
    wiping_data.drop(columns=['id','time_stamp','type','uri_list','wiping_check','group'],inplace=True)
    wiping_data=wiping_data.copy()
    wiping_data.rename(columns={'formatted_time_stamp':'time_stamp'},inplace=True)
    wiping_data.to_csv('./result/clipboard/clipboard.csv',index=False)
    return check_wiping

def clipboardFile_wiping(destination_dir,folder_name):
    pattern = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    check_wiping = False
    file_path=os.path.join(destination_dir,folder_name)

    wiping_string=''
    for file_name in os.listdir(file_path):
        sub_folder_name = os.path.join(file_path, file_name)
        clip_file_path = os.path.join(sub_folder_name, "clip")
        # "clip" 파일이 존재하는지 확인
        if os.path.isfile(clip_file_path):
            with open(clip_file_path, 'r', encoding='ISO-8859-1') as file:
                content = file.read()
                matches = re.findall(pattern, content)
                for match in matches:
                    wiping_string+=f'{match}\n'
                    check_wiping = True

    if check_wiping==True:
        with open('./result/clipboard/clipboard.txt','w') as clipboard_file:
            clipboard_file.write(wiping_string)
    return check_wiping


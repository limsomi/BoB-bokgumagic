import os
import sqlite3
import pandas as pd
import re
from PIL import Image

def read_clips_table_to_dataframe(db_path):
    conn = sqlite3.connect(db_path)
    query = """
    SELECT _id, text, html_text, item_type, entity_type, timestamp, uri 
    FROM clips
    """
    df = pd.read_sql_query(query, conn)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    conn.close()
    return df

def extract_filename_from_uri(uri):
    return uri.split('/')[-1] if uri else None

def display_image_from_folder(filename, folder_path='../files/clipboard_image'):
    file_path = os.path.join(folder_path, filename)
    if os.path.exists(file_path):
        image = Image.open(file_path)
        image.show()
    else:
        print(f"File not found: {file_path}")

pattern = re.compile(r"[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}")
db_path = 'databases/gboard_clipboard.db'
df_clips = read_clips_table_to_dataframe(db_path)

df_clips = df_clips[df_clips['entity_type'] != 3]
df_clips = df_clips[df_clips['item_type'] == 0]

filtered_rows = []

for index, row in df_clips.iterrows():
    if pattern.fullmatch(str(row['text'])):
        continue
    if not pd.isna(row['uri']) and row['uri'].strip() != '':
        print(f"Image data has been wiped. You can find your image at {row['uri']}")
        filename = extract_filename_from_uri(row['uri'])
        display_image_from_folder(filename)
    else:
        filtered_rows.append(row)

filtered_df = pd.DataFrame(filtered_rows)
print(filtered_df)



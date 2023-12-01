import sqlite3
import pandas as pd
import os 

def contacts_wiping(destination_dir,db_name):
    # 파일 이름 고치기
    db_path=os.path.join(destination_dir,db_name)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(
        "SELECT strftime('%Y-%m-%d %H:%M:%S', datetime(dc.contact_deleted_timestamp / 1000, 'unixepoch', 'localtime')) AS local_timestamp, "
        "rc.sec_trash_caller_package, "
        "MAX(CASE WHEN d.mimetype_id = 5 THEN d.data1 ELSE NULL END) AS cutom_value1, "
        "MAX(CASE WHEN d.mimetype_id = 7 THEN d.data1 ELSE NULL END) AS cutom_value2 "
        "FROM deleted_contacts dc "
        "JOIN raw_contacts rc ON dc.contact_id = rc._id "
        "LEFT JOIN data d ON rc._id = d.raw_contact_id "
        "WHERE sec_trash_caller_package != ' com.samsung.android.dialer ' AND sec_trash_caller_package != ' None ' "
        "GROUP BY dc.contact_deleted_timestamp, rc._id, rc.sec_trash_caller_package "
        "ORDER BY dc.contact_deleted_timestamp;"
    )

    rows=cur.fetchall()
    cols=[column[0] for column in cur.description]
    contacts_df=pd.DataFrame.from_records(data=rows,columns=cols)
    conn.close()
    return contacts_df

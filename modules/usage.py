from ppadb.client import Client as AdbClient
from modules import parsing_usagestats
import xml.etree.ElementTree as ET
import pandas as pd
import os
import json
import datetime

def convert_to_hms(milliseconds):
    seconds = milliseconds / 1000
    time_delta = datetime.timedelta(seconds=seconds)
    hours, remainder = divmod(time_delta.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m {seconds}s"

def usagestats(android_version):

    keywords = ["wipe", "wiping", "shredde", "shredder", "delete", "shred", "eraser", "securewipe", "eng.bite", "wiper", "remover", "ccleaner","zerdava"]
    Packages=''
    EventLog=''
    
    destination_path = "./extractdata/usagestats"


    if android_version < 10: 
        Packages=pd.DataFrame(columns=['package','timeActive','lastTimeActive'])
        EventLog=pd.DataFrame(columns=['package','class','time','type'])
        daily_path = os.path.join(destination_path,'0', 'daily')
        if os.path.exists(daily_path):
            dailyfile_list=os.listdir(daily_path)
            for file_path in dailyfile_list:
                mappings_Packages,mappings_EventLog=parsing_usagestats.usagestats_parsing9(daily_path,file_path)
                Packages=pd.concat([Packages,mappings_Packages])
                EventLog=pd.concat([EventLog,mappings_EventLog])
    elif android_version==10:
        daily_path = os.path.join(destination_path,'0', 'daily')
        if os.path.exists(daily_path):
            Packages=pd.DataFrame(columns=['package','last_time_active_ms','total_time_active_ms','last_time_visible_ms','total_time_visible_ms','app_launch_count'])
            EventLog=pd.DataFrame(columns=['package','class','time_ms','type'])
            dailyfile_list=os.listdir(daily_path)
            for file_path in dailyfile_list:
                mappings_Packages,mappings_EventLog=parsing_usagestats.usagestats_parsing10(daily_path,file_path)
                Packages=pd.concat([Packages,mappings_Packages])
                EventLog=pd.concat([EventLog,mappings_EventLog])
    else:
        mappings=parsing_usagestats.mappings_parsing()
        daily_path = os.path.join(destination_path, 'daily')

        if os.path.exists(daily_path):
            dailyfile_list=os.listdir(destination_path)
            Packages=pd.DataFrame(columns=['package','last_time_active_ms','total_time_active_ms','last_time_visible_ms','total_time_visible_ms','app_launch_count'])
            EventLog=pd.DataFrame(columns=['package','class','time_ms','type'])
        
            for daily in dailyfile_list:
                mappings_EventLog,mappings_Packages=parsing_usagestats.usagestats_parsing(destination_path,daily,mappings)
                Packages=pd.concat([Packages,mappings_Packages])
                EventLog=pd.concat([EventLog,mappings_EventLog])

    EventLog.reset_index(drop=True,inplace=True)
    Packages.reset_index(drop=True,inplace=True)
    with open('./modules/userBehaviour_type.json','r',encoding='utf-8') as file:
        userBehaviour_type=json.load(file)

        
    EventLog['type_string']=[userBehaviour_type.get(str(type),'None') for type in EventLog['type']]

    EventLog.drop(EventLog[(EventLog['type_string'] == 'None') | (EventLog['type'] == 11)].index, inplace=True)


    filtered_Packages = Packages[Packages['package'].str.contains('|'.join(keywords), case=False)]
    filtered_EventLog = EventLog[EventLog['package'].str.contains('|'.join(keywords), case=False)]
    filtered_Packages=filtered_Packages.copy().drop_duplicates()

    last_list=[['last_time_active_ms','last_time_visible_ms'],['time_ms']]
    total_list=['total_time_active_ms','total_time_visible_ms']
    df_list=[filtered_Packages,filtered_EventLog]
    if android_version==9:
        last_list=[['lastTimeActive'],['time']]
        total_list=['timeActive']

    for last,df in zip(last_list,df_list):
        for column_name in last:
            df.loc[:, column_name] = pd.to_datetime(df[column_name], unit='ms', utc=True).dt.tz_convert('Asia/Seoul')

    for column_name in total_list:
        filtered_Packages[column_name]=filtered_Packages[column_name].apply(convert_to_hms)


    filtered_Packages.to_csv('./result/Package.csv')
    filtered_EventLog.to_csv('./result/EventLog.csv')


    wiping_application=list(set([package_name for package_name in filtered_Packages['package']]))


        
    return filtered_Packages.empty,wiping_application

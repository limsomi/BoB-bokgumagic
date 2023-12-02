from ppadb.client import Client as AdbClient
from modules import parsing_usagestats
import xml.etree.ElementTree as ET
import pandas as pd
import os
import json

def usagestats(android_version):

    keywords = ["wipe", "wiping", "shredde", "shredder", "delete", "shred", "eraser", "securewipe", "eng.bite", "wiper", "remover", "ccleaner","zerdava"]
    str_list = []
 
    
    # destination_path = "./extractdata/usagestats"
    destination_path = "./usagestats"


    if android_version < 10: 
        daily_path = os.path.join(destination_path,'0', 'daily')
        print(daily_path)
        if os.path.exists(daily_path):
            dailyfile_list=os.listdir(daily_path)
            for file_path in dailyfile_list:
                tree = ET.parse(f'{daily_path}/{file_path}')
                root = tree.getroot()

                package_data = []
                for package_element in root.findall('.//package'):
                    package_value = package_element.get('package', '')
                    time_active_value = int(package_element.get('timeActive', 0))
                
                if any(keyword.lower() in package_value.lower() for keyword in keywords) and time_active_value > 0 :
                    package_data.append({
                            'package' : package_value,
                            'timeActive' : time_active_value
                        })
                for data in package_data:
                    str_list.append(f"{data['package']}가 {data['timeActive']}동안 실행됐음을 확인하였습니다.")
                    print(f"{data['package']}가 {data['timeActive']}동안 실행됐음을 확인하였습니다.")

        return
    
    # 버전 10 이상 -> 원본 파일을 csv 변환
    else:
        mappings=parsing_usagestats.mappings_parsing()
        destination_path = './extractdata/usagestats/daily'
        daily_list=os.listdir(destination_path)


        Packages=pd.DataFrame(columns=['package_token','package_name','last_time_active_ms','total_time_active_ms','app_launch_count','last_time_visible_ms','total_time_visible_ms'])
        EventLog=pd.DataFrame(columns=['package_token','class_token','time_ms','type','package_name','class_name'])

        
        for daily in daily_list:
            mappings_EventLog,mappings_Packages=parsing_usagestats.usagestats_parsing(destination_path,str(daily),mappings)
            if Packages.empty:
                Packages=mappings_Packages
            else:
                Packages=pd.concat([Packages,mappings_Packages])
            if EventLog.empty:
                EventLog=mappings_EventLog
            else:
                EventLog=pd.concat([EventLog,mappings_EventLog])

        with open('./modules/userBehaviour_type.json','r',encoding='utf-8') as file:
            userBehaviour_type=json.load(file)

        
        EventLog['type_string']=[userBehaviour_type.get(str(type)) for type in EventLog['type']]

        filtered_Packages = Packages[Packages['package_name'].str.contains('|'.join(keywords), case=False)]
        filtered_EventLog = EventLog[EventLog['package_name'].str.contains('|'.join(keywords), case=False)]

        filtered_Packages.to_csv('./result/Package.csv')
        filtered_EventLog.to_csv('./result/EventLog.csv')


        wiping_application=list(set([package_name for package_name in filtered_Packages['package_name']]))


        
    return filtered_Packages.empty,wiping_application


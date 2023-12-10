from frameworks.base.core.proto.android.server.usagestatsservice_v2_pb2 import ObfuscatedPackagesProto
from frameworks.base.core.proto.android.server.usagestatsservice_v2_pb2 import IntervalStatsObfuscatedProto
from frameworks.base.core.proto.android.server.usagestatsservice_pb2 import IntervalStatsProto

import xml.etree.ElementTree as ET
import pandas as pd
import datetime
import json
#usage parsing
def mappings_parsing():
    mappings_path='./extractdata/usagestats/mappings'
    with open(mappings_path,"rb") as file:
        proto_data = file.read()
        
    parsed_message = ObfuscatedPackagesProto()  
    parsed_message.ParseFromString(proto_data)  

    field_value = parsed_message.packages_map 
    data = {'package_token': [item.package_token for item in field_value],
            'strings': [item.strings for item in field_value]}

    mappings = pd.DataFrame(data)
    return mappings


def usagestats_parsing9(destination_path,file):
    package_data = []
    eventlog_data=[]
    tree = ET.parse(f'{destination_path}/{file}')
    root = tree.getroot()

    for package_element in root.findall('.//package'):
        package_name = package_element.get('package', None)

        timeActive = int(package_element.get('timeActive', 0))
        lastTimeActive=int(package_element.get('lastTimeActive','0'))
        if timeActive > 0 :
            lastTimeActive+=int(file)
            package_data.append({
                    'package' : package_name,
                    'timeActive' : timeActive,
                    'lastTimeActive':lastTimeActive
                })
    for eventlog_element in root.findall('.//event'):
        package_name = eventlog_element.get('package', None)
        class_name=eventlog_element.get('class',None)
        time = int(eventlog_element.get('time', 0))
        type = int(eventlog_element.get('type', 0))
        if time > 0 :
            time+=int(file)
            eventlog_data.append({
                    'package':package_name,
                    'class':class_name,
                    'time':time,
                    'type':type
                })
    packages=pd.DataFrame(data=package_data)
    event_log=pd.DataFrame(data=eventlog_data)
    return packages,event_log

def usagestats_parsing10(destination_path,file):
    usages_path=destination_path+'/'+file

    with open(usages_path,"rb") as protobuf:
        proto_data=protobuf.read()

    parsed_message=IntervalStatsProto()
    parsed_message.ParseFromString(proto_data)

    package_list=parsed_message.stringpool.strings


    #packages parsing
    field_value=parsed_message.packages
    data = {'package': [package_list[item.package_index-1] for item in field_value],
            'last_time_active_ms': [item.last_time_active_ms+int(file) if hasattr(item,'last_time_active_ms') else None for item in field_value],
            'total_time_active_ms' : [item.total_time_active_ms if hasattr(item, 'total_time_active_ms') else None for item in field_value],
            'last_time_visible_ms' : [item.last_time_visible_ms+int(file) if hasattr(item, 'last_time_visible_ms') else None for item in field_value],
            'total_time_visible_ms':[item.total_time_visible_ms if hasattr(item, 'total_time_visible_ms') else None for item in field_value],
            'app_launch_count':[item.app_launch_count if hasattr(item, 'app_launch_count') else None for item in field_value]
            }
    packages=pd.DataFrame(data)
    packages.sort_values(by='last_time_active_ms',ascending=True)
    packages.drop(packages[packages['total_time_active_ms'] == 0].index,inplace=True)

    #event_log parsing
    field_value = parsed_message.event_log 
    data = {
        'package': [package_list[item.package_index-1] for item in field_value],
        'class': [package_list[item.class_index-1] if hasattr(item, 'class_index') else 0 for item in field_value],
        'time_ms': [item.time_ms+int(file) for item in field_value],
        'type': [item.type for item in field_value]
    }
    event_log = pd.DataFrame(data)
    event_log.sort_values(by='time_ms',ascending=True)
    # event_log.drop(event_log[event_log['time_ms']==0].index,inplace=True)
  

    return packages,event_log

def usagestats_parsing(destination_path,file,mappings):
    file_path=destination_path+'/'+file
    with open(file_path,"rb") as parsing_file:
        proto_data = parsing_file.read()
    parsed_message = IntervalStatsObfuscatedProto()  

    parsed_message.ParseFromString(proto_data)  


    #packages parsing
    field_value=parsed_message.packages
    data = {'package_token': [item.package_token for item in field_value],
            'last_time_active_ms': [item.last_time_active_ms+int(file) if hasattr(item,'last_time_active_ms') else None for item in field_value],
            'total_time_active_ms' : [item.total_time_active_ms if hasattr(item, 'total_time_active_ms') else None for item in field_value],
            'last_time_visible_ms' : [item.last_time_visible_ms+int(file) if hasattr(item, 'last_time_visible_ms') else None for item in field_value],
            'total_time_visible_ms':[item.total_time_visible_ms if hasattr(item, 'total_time_visible_ms') else None for item in field_value],
            'app_launch_count':[item.app_launch_count if hasattr(item, 'app_launch_count') else None for item in field_value]
            }
    packages=pd.DataFrame(data)
    packages.sort_values(by='last_time_active_ms',ascending=True,inplace=True)

    #event_log parsing
    field_value = parsed_message.event_log 
    data = {
        'package_token': [item.package_token for item in field_value],
        'class_token': [item.class_token if hasattr(item, 'class_token') else 0 for item in field_value],
        'time_ms': [item.time_ms+int(file) for item in field_value],
        'type': [item.type for item in field_value]
    }
    event_log = pd.DataFrame(data)
    event_log.sort_values(by='time_ms',ascending=True,inplace=True)

    merged_df = pd.merge(mappings, event_log, on='package_token', how='inner')
    # merged_df.drop(merged_df[merged_df['time_ms'] == 0].index,inplace=True)
    merged_df.package_token
    mappings_EventLog = merged_df.sort_values(by='time_ms')
    mappings_EventLog.reset_index(drop=True,inplace=True)
    mappings_EventLog['package']=[strings[0] for strings in mappings_EventLog['strings']]
    mappings_EventLog['class']=[strings[token-1] if token!=0 else None for strings, token in zip(mappings_EventLog['strings'],mappings_EventLog['class_token'])]
    mappings_EventLog.drop(columns=['strings','package_token','class_token'],inplace=True)
    mappings_EventLog['time_ms']=mappings_EventLog['time_ms']
    mappings_EventLog=mappings_EventLog[['package','class','time_ms','type']]
    
    # mappings_EventLog.to_csv("./mappings_EventLog.csv",index=False)


    packages.drop(packages[packages['total_time_active_ms'] ==0].index,inplace=True)
    mappings_Packages = pd.merge(mappings, packages, on='package_token', how='inner')
    mappings_Packages.reset_index(drop=True,inplace=True)
    mappings_Packages['strings'] = mappings_Packages['strings'].apply(lambda x: x[0])
    mappings_Packages.rename(columns={'strings':'package'},inplace=True)
    mappings_Packages.drop(columns=['package_token'],inplace=True)
    mappings_Packages=mappings_Packages[['package','last_time_active_ms','total_time_active_ms','last_time_visible_ms','total_time_visible_ms','app_launch_count']]

    # mappings_Packages.to_csv("./mappings_Packages.csv",index=False)

    return mappings_EventLog,mappings_Packages

def usageToCSV(android_version,EventLog,Packages):
    keywords = ["wipe", "wiping", "shredde", "shredder", "delete", "shred", "eraser", "securewipe", "eng.bite", "wiper", "remover", "ccleaner","zerdava"]

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


    filtered_Packages.to_csv('./result/Package.csv',index=False)
    filtered_EventLog.to_csv('./result/EventLog.csv',index=False)


if __name__=="__main__":
    mappings=mappings_parsing()
    destination_path='../extractdata/usagestats/daily'
    mappings_EventLog,mappings_Packages=usagestats_parsing(destination_path,'1700650097070',mappings)
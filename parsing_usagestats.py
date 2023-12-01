from frameworks.base.core.proto.android.server.usagestatsservice_v2_pb2 import ObfuscatedPackagesProto
from frameworks.base.core.proto.android.server.usagestatsservice_v2_pb2 import IntervalStatsObfuscatedProto
import datetime
import pandas as pd

def convert_to_hms(milliseconds):
    seconds = milliseconds / 1000
    time_delta = datetime.timedelta(seconds=seconds)
    hours, remainder = divmod(time_delta.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m {seconds}s"

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


def usagestats_parsing(destination_path,file,mappings):
    file_path=destination_path+'/'+file
    with open(file_path,"rb") as parsing_file:
        proto_data = parsing_file.read()
    parsed_message = IntervalStatsObfuscatedProto()  

    parsed_message.ParseFromString(proto_data)  


    #packages parsing
    field_value=parsed_message.packages
    data = {'package_token': [item.package_token for item in field_value],
            'last_time_active_ms': [item.last_time_active_ms if hasattr(item,'last_time_active_ms') else None for item in field_value],
            'total_time_active_ms' : [item.total_time_active_ms if hasattr(item, 'total_time_active_ms') else None for item in field_value],
            'app_launch_count':[item.app_launch_count if hasattr(item, 'app_launch_count') else None for item in field_value],
            'last_time_visible_ms' : [item.last_time_visible_ms if hasattr(item, 'last_time_visible_ms') else None for item in field_value],
            'total_time_visible_ms':[item.total_time_visible_ms if hasattr(item, 'total_time_visible_ms') else None for item in field_value]
            }
    packages=pd.DataFrame(data)
    packages.sort_values(by='last_time_active_ms',ascending=True)

    #event_log parsing
    field_value = parsed_message.event_log 
    data = {
        'package_token': [item.package_token for item in field_value],
        'class_token': [item.class_token if hasattr(item, 'class_token') else 0 for item in field_value],
        'time_ms': [item.time_ms for item in field_value],
        'type': [item.type for item in field_value]
    }
    event_log = pd.DataFrame(data)
    event_log.sort_values(by='time_ms',ascending=True)

    merged_df = pd.merge(mappings, event_log, on='package_token', how='inner')
    merged_df.drop(merged_df[merged_df['time_ms'] == 0].index,inplace=True)
    mappings_EventLog = merged_df.sort_values(by='time_ms')
    mappings_EventLog.reset_index(drop=True,inplace=True)
    mappings_EventLog['package_name']=[strings[0] for strings in mappings_EventLog['strings']]
    mappings_EventLog['class_name']=[strings[token-1] if token!=0 else None for strings, token in zip(mappings_EventLog['strings'],mappings_EventLog['class_token'])]
    mappings_EventLog.drop(columns=['strings'],inplace=True)
    mappings_EventLog['time_ms']=mappings_EventLog['time_ms']+int(file)
    mappings_EventLog['time_ms'] = pd.to_datetime(mappings_EventLog['time_ms'], unit='ms', utc=True)
    mappings_EventLog['time_ms_local'] = mappings_EventLog['time_ms'].dt.tz_convert('Asia/Seoul')
    mappings_EventLog.drop(columns=['time_ms'],inplace=True)
    # mappings_EventLog.to_csv("./mappings_EventLog.csv",index=False)


    packages.drop(packages[packages['total_time_active_ms'] ==0].index,inplace=True)
    mappings_Packages = pd.merge(mappings, packages, on='package_token', how='inner')
    mappings_Packages.reset_index(drop=True,inplace=True)
    mappings_Packages['strings'] = mappings_Packages['strings'].apply(lambda x: x[0])
    mappings_Packages.rename(columns={'strings':'package_name'},inplace=True)
    last_list=['last_time_active_ms','last_time_visible_ms']
    total_list=['total_time_active_ms','total_time_visible_ms']

    for column_name in last_list:
        mappings_Packages[column_name]=mappings_Packages[column_name]+int(file)
        mappings_Packages[column_name] = pd.to_datetime(mappings_Packages[column_name], unit='ms', utc=True)
        mappings_Packages[column_name+'_local'] = mappings_Packages[column_name].dt.tz_convert('Asia/Seoul')
        mappings_Packages.drop(columns=[column_name],inplace=True)

    for column_name in total_list:
        mappings_Packages[column_name+'_local']=mappings_Packages[column_name].apply(convert_to_hms)
        mappings_Packages.drop(columns=[column_name],inplace=True)
    # mappings_Packages.to_csv("./mappings_Packages.csv",index=False)

    return mappings_EventLog,mappings_Packages
from frameworks.base.core.proto.android.server.usagestatsservice_v2_pb2 import ObfuscatedPackagesProto
from frameworks.base.core.proto.android.server.usagestatsservice_v2_pb2 import IntervalStatsObfuscatedProto
import pandas as pd


def mappings_parsing():
    file_path = './usagestats/mappings'
    with open(file_path, "rb") as file:
        proto_data = file.read()

    parsed_message = ObfuscatedPackagesProto()
    parsed_message.ParseFromString(proto_data)


    data = {'package_token': [], 'strings': []}

    for item in parsed_message.packages_map:
        strings_values = [val for val in item.strings]
        data['package_token'].extend([item.package_token] * len(strings_values))
        data['strings'].extend(strings_values)

    mappings = pd.DataFrame(data)
    return mappings



def usagestats_parsing(destination_path,file,mappings):
    file_path=destination_path+'/'+file
    with open(file_path,"rb") as parsing_file:
        proto_data = parsing_file.read()
    parsed_message = IntervalStatsObfuscatedProto()  

    parsed_message.ParseFromString(proto_data)  



    #event_log parsing
    field_value = parsed_message.event_log 
    data = {'package_token': [item.package_token for item in field_value],
            'time_ms': [item.time_ms for item in field_value],
            'type':[item.type for item in field_value]}
    event_log = pd.DataFrame(data)

    #packages parsing
    field_value=parsed_message.packages
    data = {'package_token': [item.package_token for item in field_value],
            'last_time_component_used_ms': [item.last_time_component_used_ms for item in field_value]}
    packages=pd.DataFrame(data)


    merged_df = pd.merge(mappings, event_log, on='package_token', how='inner')
    merged_df.drop(merged_df[merged_df['time_ms'] == 0].index,inplace=True)
    merged_df = merged_df.sort_values(by='time_ms')
    merged_df.reset_index(drop=True,inplace=True)
    mappings_EventLog=merged_df.explode('strings')
    mappings_EventLog.rename(columns={'strings':'package_name'},inplace=True)
    mappings_EventLog['time_ms']=mappings_EventLog['time_ms']+int(file)
    mappings_EventLog['time_ms'] = pd.to_datetime(mappings_EventLog['time_ms'], unit='ms', utc=True)
    mappings_EventLog['time_ms_local'] = mappings_EventLog['time_ms'].dt.tz_convert('Asia/Seoul')
    mappings_EventLog.drop(columns=['time_ms'],inplace=True)
    # mappings_EventLog.to_csv("./log_mappings.csv",index=False)


    merged_df = pd.merge(mappings, packages, on='package_token', how='inner')
    merged_df.drop(merged_df[merged_df['last_time_component_used_ms'] ==0].index,inplace=True)
    merged_df = merged_df.sort_values(by='last_time_component_used_ms')
    merged_df.reset_index(drop=True,inplace=True)
    mappings_Packages=merged_df.explode('strings')
    mappings_Packages.rename(columns={'strings':'package_name'},inplace=True)
    mappings_Packages['last_time_component_used_ms']=mappings_Packages['last_time_component_used_ms']+int(file)
    mappings_Packages['last_time_component_used_ms'] = pd.to_datetime(mappings_Packages['last_time_component_used_ms'], unit='ms', utc=True)
    mappings_Packages['last_time_component_used_ms_local'] = mappings_Packages['last_time_component_used_ms'].dt.tz_convert('Asia/Seoul')
    mappings_Packages.drop(columns=['last_time_component_used_ms'],inplace=True)
    # mappings_Packages.to_csv("./mappings_Packages.csv",index=False)
    return mappings_EventLog,mappings_Packages
from modules.data_processing import parsing_usagestats
from modules.data_processing import adb_extract
from modules.data_processing import mkdir
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import xml.etree.ElementTree as ET
import pandas as pd
import os
import json
import datetime

class Usage_Thread(QThread):#usagestats 처리
    progress_signal=pyqtSignal(int,str)
    result_signal = pyqtSignal(int, str, bool, list,list)
    finished_signal=pyqtSignal()
    signal=0
    def convert_to_hms(self,milliseconds):
        seconds = milliseconds / 1000
        time_delta = datetime.timedelta(seconds=seconds)
        hours, remainder = divmod(time_delta.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}h {int(minutes)}m {seconds}s"

    def run(self):
        self.signal+=30
        self.progress_signal.emit(self.signal,'device 정보 추출 중')
        device = adb_extract.get_device()
        android_version = int(adb_extract.get_androidVersion(device))
        modelname = adb_extract.get_modelname(device)
        mkdir.init()
        
        if android_version < 11:
            destination_dir = '/data/system/'
        else:
            destination_dir = '/data/system_ce/0' 
        self.signal+=20
        self.progress_signal.emit(self.signal,'UsageStats 추출 중')
        usage_name = 'usagestats'
        adb_extract.extract_data(device, usage_name, destination_dir)
        self.signal+=20
        self.progress_signal.emit(self.signal,'UsageStats 추출 중')
        wiping_check, wiping_application,duplicated_application = self.usagestats(android_version)
        
        self.result_signal.emit(android_version, modelname, wiping_check, wiping_application,duplicated_application)
        self.finished_signal.emit()


    def usagestats(self,android_version,):

        keywords = ["wipe", "wiping", "shredde", "shredder", "delete", "shred", "eraser", "securewipe", "eng.bite", "wiper", "remover", "ccleaner","zerdava"]
        Packages=''
        EventLog=''
        
        destination_path = "./extractdata/usagestats"

        if android_version < 10: 
            Packages=pd.DataFrame(columns=['package','timeActive','lastTimeActive'])
            EventLog=pd.DataFrame(columns=['package','class','time','type'])
            daily_path = os.path.join(destination_path,'0', 'daily')
            timeColumnn='lastTimeActive'
            if os.path.exists(daily_path):
                dailyfile_list=os.listdir(daily_path)
                for file_path in dailyfile_list:
                    mappings_Packages,mappings_EventLog=parsing_usagestats.usagestats_parsing9(daily_path,file_path)
                    
                    Packages=pd.concat([Packages,mappings_Packages])
                    EventLog=pd.concat([EventLog,mappings_EventLog])
                    new_row_index = len(EventLog) 
                    EventLog.loc[new_row_index, :] = None
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
                    new_row_index = len(EventLog) 
                    EventLog.loc[new_row_index, :] = None
        else:
            mappings=parsing_usagestats.mappings_parsing()
            daily_path = os.path.join(destination_path, 'daily')
            timeColumnn='last_time_active_ms'
            if os.path.exists(daily_path):
                dailyfile_list=os.listdir(daily_path)
                Packages=pd.DataFrame(columns=['package','last_time_active_ms','total_time_active_ms','last_time_visible_ms','total_time_visible_ms','app_launch_count'])
                EventLog=pd.DataFrame(columns=['package','class','time_ms','type'])
            
                for daily in dailyfile_list:
                    mappings_EventLog,mappings_Packages=parsing_usagestats.usagestats_parsing(daily_path,daily,mappings)
                    
                    Packages=pd.concat([Packages,mappings_Packages])
                    EventLog=pd.concat([EventLog,mappings_EventLog])
                    new_row_index = len(EventLog) 
                    EventLog.loc[new_row_index, :] = None
        EventLog.reset_index(drop=True,inplace=True)
        Packages.reset_index(drop=True,inplace=True)
        Packages.sort_values(by=timeColumnn,ascending=True,inplace=True)
        # EventLog.sort_values(by='time_ms',ascending=True,inplace=True)
        with open('./modules/userBehaviour_type.json','r',encoding='utf-8') as file:
            userBehaviour_type=json.load(file)

            
        EventLog['type_string']=[userBehaviour_type.get(str(type),'None') for type in EventLog['type']]
        EventLog.loc[EventLog['package'].isna(),'type_string']=' '
    
        EventLog.drop(EventLog[(EventLog['type_string'] == 'None') | (EventLog['type'] == 11)].index, inplace=True)


        filtered_Packages = Packages[Packages['package'].str.contains('|'.join(keywords), case=False)]
        filtered_EventLog = EventLog[(EventLog['package'].isna()) | EventLog['package'].str.contains('|'.join(keywords), case=False)]
        # EventLog.to_csv('result/test2.csv')

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
            filtered_Packages[column_name]=filtered_Packages[column_name].apply(self.convert_to_hms)

        mask = (filtered_EventLog['package'].shift(1) == filtered_EventLog['package'].shift(-1)) & (filtered_EventLog['package'].isna())
        non=filtered_EventLog['package'].isna() & ~mask
        filtered_EventLog = filtered_EventLog[~non]

        filtered_EventLog['group'] = (filtered_EventLog['package'] != filtered_EventLog['package'].shift(1)).cumsum()
        none=filtered_EventLog['package'].isna()
        newEventLog=filtered_EventLog[~none]
        newEventLog['new_group'] = (newEventLog['group'] != newEventLog['group'].shift(1)).cumsum()

        filtered_Packages.to_csv('./result/Package.csv',index=False)
        newEventLog.to_csv('./result/EventLog.csv',index=False)


        wiping_application = []
        [wiping_application.append(package_name ) for package_name in filtered_Packages['package']  if package_name not in wiping_application]
        duplicated_application=[package_name for package_name in filtered_Packages['package']]
        
            
        return filtered_Packages.empty,wiping_application,duplicated_application

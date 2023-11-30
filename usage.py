# 핸드폰 usb 연결
from ppadb.client import Client as AdbClient
from parsing_usagestats import *
import xml.etree.ElementTree as ET
import pandas as pd
import os

def usagestats(device):

    keywords = ["wipe", "wiping", "shredde", "shredder", "delete", "shred", "eraser", "securewipe", "eng.bite", "wiper", "remover", "ccleaner"]
    str_list = []
    # 안드로이드 버전 확인
    android_version = device.shell('getprop ro.build.version.release')
    print("android_version : "+android_version)
    # 버전에 따라 Usagestats의 yearly 파일 추출
    base_path = "/data/system/0/usagestats" if android_version < "10" else "/data/system_ce/0/usagestats"
    os.system(f'adb shell su -c "cp -r {base_path} /sdcard/"')
    os.system(f'adb pull /sdard/usagestats ./')
    
    destination_path = "./usagestats"

    if android_version < "10":
        yearly_path = os.path.join('./usagestats', 'yearly')
        if os.path.exists(yearly_path):
            yearly_files = [os.path.join(yearly_path, file) for file in os.listdir(yearly_path) if os.path.isfile(os.path.join(yearly_path, file))]
            for file_path in yearly_files:
                tree = ET.parse(f'{destination_path}/yearly/{file_path}')
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
            else:
                    print("Yearly directory not found.")
    
    # 버전 10 이상 -> 원본 파일을 csv 변환
    else:
        mappings=mappings_parsing()
        destination_path = './usagestats'
        list=os.listdir(destination_path)


        EventLog=pd.DataFrame(columns=['package_token','package_name','time_ms_local'])
        Packages=pd.DataFrame(columns=['package_token','package_name','last_time_component_used_ms_local'])

        folder_list=[]
        for item in list:
            path=os.path.join(destination_path,item)
            if os.path.isdir(path):
                folder_list.append(path)

        for folder in folder_list:
            usagefile_list=os.listdir(folder)
            for file in usagefile_list:
                try:
                    mappings_EventLog, mappings_Packages = usagestats_parsing(folder, str(file), mappings)
                    if EventLog.empty:  # Check if the DataFrame is not empty
                        EventLog = mappings_EventLog
                    else:
                        EventLog=pd.concat([EventLog,mappings_EventLog],ignore_index=True)
                except:
                    pass
            
                if Packages.empty:  # Check if the DataFrame is not empty
                    Packages = mappings_Packages
                else:
                    Packages=pd.concat([Packages,mappings_Packages],ignore_index=True)

        EventLog.drop_duplicates(inplace=True)
        Packages.drop_duplicates(inplace=True)

        # 패키지명 여러 개 -> 키워드가 들어간 패키지명만 필터링
        filtered_EventLog = EventLog[EventLog['package_name'].str.contains('|'.join(keywords), case=False)]
        filtered_EventLog.loc[:, 'time_ms_local'] = pd.to_datetime(filtered_EventLog['time_ms_local']).dt.strftime('%Y-%m-%d %H:%M:%S')
        filtered_EventLog = filtered_EventLog[filtered_EventLog['type'] == 11]
        filtered_packages = Packages[Packages['package_name'].str.contains('|'.join(keywords), case=False)]
        filtered_packages.loc[:, 'last_time_component_used_ms_local'] = pd.to_datetime(filtered_packages['last_time_component_used_ms_local']).dt.strftime('%Y-%m-%d %H:%M:%S')

        missing_packages = filtered_packages[~filtered_packages['package_name'].isin(filtered_EventLog['package_name'])]

        # EventLog에 존재하지 않는 패키지 명을 Package에서 추가
        copy_values = {}
        for index, row in missing_packages.iterrows():
            copy_values[row['package_name']] = row['last_time_component_used_ms_local']

        filtered_EventLog['time_ms_local'] = pd.to_datetime(filtered_EventLog['time_ms_local'], utc=True).dt.tz_convert('Asia/Seoul')
        filtered_EventLog.sort_values(by=['package_name', 'time_ms_local'], inplace=True)

        filtered_EventLog['time_diff'] = filtered_EventLog.groupby('package_name')['time_ms_local'].diff()
        consecutive_mask = filtered_EventLog['time_diff'] != pd.Timedelta(minutes=1)
        consecutive_mask = consecutive_mask | consecutive_mask.shift(-1)

        non_consecutive_rows = filtered_EventLog[consecutive_mask]
        
        # 패키지 명을 기준으로 실행된 날짜 추출 -> 시간은 많아서 생략함
        for package_name, group in non_consecutive_rows.groupby('package_name'):
            intervals = []
            for idx, row in group.iterrows():
                if not pd.isna(row['time_ms_local']) and not pd.isna(row['time_diff']):
                    if not intervals or row['time_diff'] != pd.Timedelta(minutes=1):
                        intervals.append(row['time_ms_local'].strftime('%Y-%m-%d'))
                    intervals.append((row['time_ms_local'] + row['time_diff']).strftime('%Y-%m-%d'))
            unique_intervals = set(intervals)
            str_list.append("{package_name}이(가) {' , '.join(unique_intervals)}에 실행됐음을 확인했습니다.")
            print(f"{package_name}이(가) {' , '.join(unique_intervals)}에 실행됐음을 확인했습니다.")

def main():
    # ADB 연결
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    if not devices:
        print("No Android devices found.")
        return

    # 첫 번째 연결된 디바이스 사용
    device = devices[0]

    # usagestats에서 File Wiping 앱 실행 흔적 찾기
    usagestats(device)


if __name__=="__main__":
    main()
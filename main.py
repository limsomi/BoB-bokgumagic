from adb_extract import *
from cache_image import *
from clipboard import *
from full_shared_prefs import *
from contacts import *
from usage import *
import pandas as pd
def main():
    #adb extract usage
    # phone_type=input("폰 기종을 입력해수세요(1. 갤럭시 2.픽셀) : ")
    android_version=int(get_androidVersion())
    # if android_version<11:
    #     destination_dir='/data/system/' # usagestats 경로 유의하기 
    # else:
    #     destination_dir='/data/system_ce/0' 
    # usage='usagestats'
    # extract_data(usage,destination_dir)
    wiping_check,wiping_application=usagestats(android_version)#package_name도  추출해야함

    if wiping_check==True:
        print("wiping 흔적 없음")
        exit(0)
    else:
        print(wiping_application)
        #adb extract clipboard data
        destination_dir='/data'
        if android_version<11:
            clipboard_folder='clipboard' #destination_dir=data
        elif android_version==11:
            clipboard_folder='semclipboard'#destination_dir=data
        else:
            destination_dir='/data/data'
            clipboard_folder='com.samsung.android.honeyboard'
            clipboard_name='databases/ClipItem.db'

        # if phone_type==2:
        #     clipboard_folder='com.google.android.inputmethod.latin'
        # extract_data(clipboard_folder,destination_dir)

        # #adb extract all data except clipboard data
        # data_list=['com.sec.android.gallery3d','com.samsung.android.providers.contacts']
        # data_list.extend(wiping_application)
        # destination_dir='/data/data'
        # for file_name in data_list:
        #     extract_data(file_name,destination_dir)


        #gallery cache
        # gallery_destination_dir='./extractdata'
        # gallery_renamed_files_dir='./extractdata/gallery3d_cache'
        # cache_image(gallery_destination_dir,gallery_renamed_files_dir)

        #clipboard
        # if android_version<11:
        #     clipboardFile_wiping('경로 지정')
        # else:
        #     clipboardDB_wiping('extractdata',clipboard_folder,clipboard_name)

        #contacts
        # contacts=contacts_wiping('extractdata','com.samsung.android.providers.contacts/databases/contacts2.db')
        # print(contacts)

        #application folder
        for package_name in wiping_application:
            full_shared_prefs('extractdata',package_name)

        if 'securewipe' or 'com.palmtronix.shreddit.v1' in wiping_application: # 애플리케이션 보고서 존재
            folder_destination_dir='./'
            folder_renamed_files_dir='(수정바람)'
            cache_image(folder_destination_dir,folder_renamed_files_dir)

if __name__=="__main__":
    main()
from modules import adb_extract
from modules import cache
from modules import clipboard
from modules import shared_prefs
from modules import contacts
from modules import usage
import os

def main():
    if not os.path.exists('result'):
        os.makedirs('result')
    #adb extract usage
    phone_type=input("폰 기종을 입력해수세요(1. 갤럭시 2.픽셀) : ")
    android_version=int(adb_extract.get_androidVersion())
    # android_version=13
    if android_version<11:
        destination_dir='/data/system/' # usagestats 경로 유의하기 
    else:
        destination_dir='/data/system_ce/0' 
    usage_name='usagestats'
    adb_extract.extract_data(usage_name,destination_dir)
    wiping_check,wiping_application=usage.usagestats(android_version)#package_name도  추출해야함

    # wiping_application=['com.shredder.fileshredder.securewipe','com.palmtronix.shreddit.v1']
    # wiping_check=False
    if wiping_check==True:
        print("wiping 흔적 없음")
        exit(0)
    else:
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

        if phone_type==2:
            clipboard_folder='com.google.android.inputmethod.latin'
        adb_extract.extract_data(clipboard_folder,destination_dir)

        # #adb extract all data except clipboard data
        data_list=['com.sec.android.gallery3d','com.samsung.android.providers.contacts']
        data_list.extend(wiping_application)
        destination_dir='/data/data'
        for file_name in data_list:
            adb_extract.extract_data(file_name,destination_dir)


        #gallery cache
        gallery_destination_dir='./extractdata'
        gallery_renamed_files_dir='./extractdata/gallery3d_cache'
        cache.cache_image(gallery_destination_dir,gallery_renamed_files_dir)

        #clipboard
        if android_version<11:
            clipboard.clipboardFile_wiping('경로 지정')
        else:
            clipboard.clipboardDB_wiping('extractdata',clipboard_folder,clipboard_name)

        #contacts
        contacts.contacts_wiping('extractdata','com.samsung.android.providers.contacts/databases/contacts2.db')


        # application folder
        for package_name in wiping_application:
            shared_prefs.full_shared_prefs('extractdata',package_name)
            folder_destination_dir=f'./extractdata/{package_name}/image_manage_disk_cache'
            folder_renamed_files_dir=f'./result/{package_name}'
            cache.cache_image(folder_destination_dir,folder_renamed_files_dir)
        


if __name__=="__main__":
    main()
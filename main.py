from adb_extract import *
from cache_image import *
from clipboard import *
from full_shared_prefs import *
from contacts import *
from usage import *

android_version=get_androidVersion()
usage_pathlist=['usagestats']
destination_dir='/data/system_ce/0'
extract_data(usage_pathlist,destination_dir)
#adb extract usage
usagestats(android_version)
#adb extract all data
clipboard_name=''
package_name='Usage에서 받아오기'
data_list=['com.sec.android.gallery3d',{clipboard_name},{package_name},'com.samsung.android.providers.contacts']
destination_dir='/data/data'
extract_data(data_list,destination_dir)


#gallery cache
gallery_destination_dir='./'
gallery_renamed_files_dir='./gallery3d_cache'
cache_image(gallery_destination_dir,gallery_renamed_files_dir)

#clipboard
if android_version<11:
    clipboardFile_wiping('경로 지정')
else:
    clipboardDB_wiping()

#contacts
contacts_wiping()


#application folder
full_shared_prefs('package_path(수정바람)')
folder_destination_dir='./'
folder_renamed_files_dir='(수정바람)'
cache_image(folder_destination_dir,folder_renamed_files_dir)
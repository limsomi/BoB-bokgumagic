from adb_extract import *
from cache_image import *
from clipboard import *
from full_shared_prefs import *
from contacts import *

android_version=''

#adb extract usage

#adb extract all data
clipboard_name=''
package_name=''
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

#clipboard_wiping
contacts_wiping()


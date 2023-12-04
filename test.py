from modules import adb_extract
from modules import cache
device=adb_extract.get_device()
adb_extract.extract_data(device,'com.shredder.fileshredder.securewipe','/data/data')
package_name='com.shredder.fileshredder.securewipe'
folder_destination_dir=f'./extractdata/{package_name}/cache/image_manager_disk_cache'
folder_renamed_files_dir=f'./result/{package_name}'
cache.cache_image(folder_destination_dir,folder_renamed_files_dir)
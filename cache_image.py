import os
import shutil
from ppadb.client import Client as AdbClient
from adb_extract import *

def rename_files_with_extension(destination_dir, old_extension, new_extension):
    renamed_files = []
    for root, dirs, files in os.walk(destination_dir):
        for filename in files:
            if filename.endswith(f'.{old_extension}'):
                old_filepath = os.path.join(root, filename)
                new_filename = f'{os.path.splitext(filename)[0]}.{new_extension}'
                new_filepath = os.path.join(root, new_filename)
                os.rename(old_filepath, new_filepath)
                renamed_files.append(new_filepath)
                print(f"Renamed: {filename} -> {new_filename}")
    return renamed_files

def move_files_to_directory(file_list, destination_dir):
    for file_path in file_list:
        shutil.move(file_path, destination_dir)

def cache_image(destination_dir,renamed_files_dir):

    # package_name = ['com.sec.android.gallery3d']
    # destination_dir = './data/data'


    # extract_data(package_name,destination_dir)

    # destination_dir='./'
    renamed_files = rename_files_with_extension(destination_dir, '0', 'jpg')
    
    if not os.path.exists(renamed_files_dir):
        os.makedirs(renamed_files_dir)

    move_files_to_directory(renamed_files, renamed_files_dir)
    print(f"Renamed files moved to {renamed_files_dir}")



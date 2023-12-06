import os
import shutil


def rename_files_with_extension(destination_dir, rename_files_dir, new_extension):
    for root, dirs, files in os.walk(destination_dir):
        for filename in files:
            if filename.endswith('.0') :
                old_filepath = os.path.join(root, filename)
                new_filename = f'{os.path.splitext(filename)[0]}.{new_extension}'
                new_filepath = os.path.join(rename_files_dir,new_filename)
                os.rename(old_filepath, new_filepath)
            elif filename!='journal':
                old_filepath = os.path.join(root, filename)
                new_filename=f'{filename}.jpg'
                new_filepath = os.path.join(rename_files_dir,new_filename)

def cache_image(destination_dir,renamed_files_dir):
    if not os.path.exists(destination_dir):
        return
    
    if not os.path.exists(renamed_files_dir):
        os.makedirs(renamed_files_dir)
    
    rename_files_with_extension(destination_dir,renamed_files_dir, 'jpg') # 픽셀은 다름
    



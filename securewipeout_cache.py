import os
import shutil
from ppadb.client import Client as AdbClient

def extract_and_move_cache(device, package_name, destination_dir):
    full_source_path = f'/data/data/{package_name}/cache'
    full_source_path_sdcard = f'/sdcard/cache'

    # Copy cache directory to /sdcard/
    copy_command = f'adb -s {device.serial} shell su -c "cp -r {full_source_path} /sdcard/"'
    result = os.system(copy_command)

    if result == 0:
        print(f"Cache directory from {full_source_path} copied to /sdcard/ on the device.")
    else:
        print("Failed to copy cache directory. Make sure the path is correct and the device is connected.")
        return

    # Pull the cache directory to the local destination
    pull_command = f'adb -s {device.serial} pull {full_source_path_sdcard} {destination_dir}'
    result = os.system(pull_command)

    if result == 0:
        print(f"Cache directory from {full_source_path_sdcard} extracted and saved to {destination_dir}")
    else:
        print("Failed to extract cache directory. Make sure the path is correct and the device is connected.")
        return

    return os.path.join(destination_dir, 'cache')

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

def main():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    if not devices:
        print("No Android devices found.")
        return

    device = devices[0]

    package_name = 'com.shredder.fileshredder.securewipe'
    destination_dir = '.'
    renamed_files_dir = 'securewipeout_cache'

    cache_dir = extract_and_move_cache(device, package_name, destination_dir)
    print(cache_dir)
    renamed_files = rename_files_with_extension(cache_dir, '0', 'jpg')

    if not os.path.exists(renamed_files_dir):
        os.makedirs(renamed_files_dir)

    move_files_to_directory(renamed_files, renamed_files_dir)
    print(f"Renamed files moved to {renamed_files_dir}")

if __name__ == "__main__":
    main()
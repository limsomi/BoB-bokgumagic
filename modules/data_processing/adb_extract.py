import subprocess
import os
import re
from ppadb.client import Client as AdbClient

def get_androidVersion(device):
    try:
        result = subprocess.check_output(['adb','-s',device.serial, 'shell', 'getprop', 'ro.build.version.release'])
        android_version = result.strip().decode('utf-8') 
        return android_version
    except Exception as e:
        return f"Error getting Android version: {e}"
    
def get_device():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    if not devices:
        print("No Android devices found.")
        return
    device = devices[0]
    return device
def get_modelname(device):
    device_properties = device.get_properties()
    model_name = device_properties["ro.product.model"]
    return model_name

def extract_data(device,file_name, destination_dir):
    copy_command = f'''adb -s {device.serial} shell "su -c 'cd {destination_dir} && cp -r {file_name} /sdcard'"'''
    copy_check = True

    try:
        subprocess.run(copy_command, shell=True, check=False)
        print(f"Successfully copy {file_name} to sdcard")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        copy_check = False
    
    try:
        pull_command = f"adb -s {device.serial} pull /sdcard/{file_name} ./extractdata"
        subprocess.check_output(pull_command, shell=True, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        error_pattern = re.compile(fr"Command 'adb -s {device.serial} pull (.*?) ./extractdata' returned non-zero exit status 1.")
        match = error_pattern.search(str(e))
        if match and copy_check==True:
            error_file_path = match.group(1)
            find_unique_command = f"adb -s {device.serial} shell find {error_file_path} -type f"
            result = subprocess.check_output(find_unique_command, shell=True, universal_newlines=True)
            unique_characters = re.compile(r'[@!#$%^&*()<>?|}{~:]')
            for filename in result.splitlines():
                if unique_characters.search(filename):
                    replace_filename = re.sub(r"[@!#$%^&*()<>?|}{~:]","",filename)
                    rename_command=f"adb -s {device.serial} shell mv {filename} {replace_filename}"
                    subprocess.run(rename_command,shell=True,check=True)
            try:
                subprocess.check_output(pull_command,shell=True,universal_newlines=True)
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")


def extract_clipboard_image(path,destination_dir):

    try:
        copy_command=f'''adb shell "su -c 'cd {destination_dir} && cp -r {path} /sdcard'"'''
        subprocess.run(copy_command, shell=True, check=True)
        print("ADB command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing ADB command: {e}")

    try:
        pull_command=f"adb pull /sdcard/{path}"
        subprocess.run(pull_command, shell=True, check=True)
        print("ADB command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing ADB command: {e}")
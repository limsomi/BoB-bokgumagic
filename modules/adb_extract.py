import subprocess
import os
import re

def get_androidVersion():
    try:
        result = subprocess.check_output(['adb', 'shell', 'getprop', 'ro.build.version.release'])
        android_version = result.strip().decode('utf-8') 
        return android_version
    except Exception as e:
        return f"Error getting Android version: {e}"

def extract_data(file_name, destination_dir):
    copy_command = f'''adb shell "su -c 'cd {destination_dir} && cp -r {file_name} /sdcard'"'''
    copy_check = True

    try:
        subprocess.run(copy_command, shell=True, check=False)
        print(f"Successfully copy {file_name} to sdcard")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        copy_check = False

    if not os.path.exists('extractdata'):
        os.makedirs('extractdata')
    
    try:
        pull_command = f"adb pull /sdcard/{file_name} ./extractdata"
        subprocess.run(pull_command, shell=True, check=True)
        print(f"File successfully pulled to {file_name}")
    except subprocess.CalledProcessError as e:
        error_pattern = re.compile(r"Command 'adb pull (.*?) ./extractdata' returned non-zero exit status 1.")
        match = error_pattern.search(str(e))
        if match and copy_check==True:
            error_file_path = match.group(1)
            find_unique_command = f"adb shell find {error_file_path} -type f"
            result = subprocess.check_output(find_unique_command, shell=True, universal_newlines=True)
            unique_characters = re.compile(r'[@!#$%^&*()<>?|}{~:]')
            for filename in result.splitlines():
                if unique_characters.search(filename):
                    replace_filename = re.sub(r"[@!#$%^&*()<>?|}{~:]","",filename)
                    rename_command=f"adb shell mv {filename} {replace_filename}"
                    subprocess.run(rename_command,shell=True,check=True)
            try:
                subprocess.run(pull_command,shell=True,check=True)
                print(f"File successfully pulled to {file_name}")
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
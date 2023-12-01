import subprocess
import os

def get_androidVersion():
    try:
        result = subprocess.check_output(['adb', 'shell', 'getprop', 'ro.build.version.release'])
        android_version = result.strip().decode('utf-8') 
        return android_version
    except Exception as e:
        return f"Error getting Android version: {e}"


def extract_data(file_name,destination_dir):
    copy_command = f'''adb shell "su -c 'cd {destination_dir} && cp -r {file_name} /sdcard'"'''

    try:
        subprocess.run(copy_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing ADB command: {e}")

    if not os.path.exists('extractdata'):
        os.makedirs('extractdata')

    try:
        pull_command=f"adb pull /sdcard/{file_name} ./extractdata"
        subprocess.run(pull_command, shell=True, check=True)
        print(f"ADB extract {file_name} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing ADB command: {e}")

def extract_shared_prefs(device, package_name):
    # ADB shell 명령어를 사용하여 파일 추출
    if package_name == "com.cbinnovations.androideraser":
        result = device.shell(f"su -c 'cat /data/data/{package_name}/shared_prefs/{package_name}.xml'")
    elif package_name == "com.projectstar.ishredder.android.standard":
        result = device.shell(f"su -c 'cat /data/data/{package_name}/shared_prefs/{package_name}_preferences.xml'")
    return result


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
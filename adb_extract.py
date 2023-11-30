import subprocess
import os
def extract_data(path_list,destination_dir):
    # print(path_list)
    for path in path_list:
        # print(path)
        source_path=os.path.join(destination_dir,path)
        copy_command = f'''adb shell "su -c 'cd {source_path} && cp -r {path} /sdcard'"'''

        try:
            subprocess.run(copy_command, shell=True, check=True)
            print("ADB command executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing ADB command: {e}")

    for path in path_list:
        try:
            pull_command=f"adb pull /sdcard/{path}"
            subprocess.run(pull_command, shell=True, check=True)
            print("ADB command executed successfully.")
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
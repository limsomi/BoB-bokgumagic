import subprocess
import os
def extract_data(path_list,destination_dir):
    for path in path_list:
        source_path=os.path.join(destination_dir,path)
        copy_command = f"adb shell su -c 'cd {source_path} && cp -r {path_list} /sdcard'"

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

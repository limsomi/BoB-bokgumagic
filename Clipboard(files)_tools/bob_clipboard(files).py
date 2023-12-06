import os
import re

# def check_clipboard_wiped(folder_path):
#     # UUID 형태의 정규 표현식 패턴 정의
#     pattern = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
#     wiped_found = False

#     # 주어진 폴더 안의 모든 하위 폴더를 순회
#     for folder_name in os.listdir(folder_path):
#         sub_folder_path = os.path.join(folder_path, folder_name)
#         clip_file_path = os.path.join(sub_folder_path, "clip")
#         # "clip" 파일이 존재하는지 확인
#         if os.path.isfile(clip_file_path):
#             with open(clip_file_path, 'r', encoding='ISO-8859-1') as file:
#                 content = file.read()
#                 matches = re.findall(pattern, content)
#                 for match in matches:
#                     print(match)
#                     wiped_found = True

#     if wiped_found:
#         print("This Clipboard has been wiped")

# # 'clipboard_wiped' 폴더 경로를 지정하세요.
# check_clipboard_wiped("clipboard_wiped")
def clipboardFile_wiping(destination_dir,folder_name):
    pattern = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    check_wiping = False
    file_path=os.path.join(destination_dir,folder_name)

    wiping_string=''
    for file_name in os.listdir(file_path):
        sub_folder_name = os.path.join(file_path, file_name)
        clip_file_path = os.path.join(sub_folder_name, "clip")
        # "clip" 파일이 존재하는지 확인
        if os.path.isfile(clip_file_path):
            with open(clip_file_path, 'r', encoding='ISO-8859-1') as file:
                content = file.read()
                matches = re.findall(pattern, content)
                for match in matches:
                    wiping_string+=f'{match}\n'
                    check_wiping = True

    if check_wiping==True:
        with open('./result/clipboard/clipboard.txt','w') as clipboard_file:
            clipboard_file.write(wiping_string)
    return check_wiping

clipboardFile_wiping('','clipboard_wiped')

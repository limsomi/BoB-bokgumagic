import xml.etree.ElementTree as ET
import re
from ppadb.client import Client as AdbClient
import os 
def extract_elements(elements):
    extracted_elements = {
        "startDate": None,
        "endDate": None,
        "mCycles": None,
        "mValue": None,
        "mPattern": None,
        "name": None,
        "type": None,
        "endTime": None,
        "appCode": None
    }

    for element in elements:
        if ':' in element:
            key, value = element.split(':', 1)
            key, value = key.strip('"'), value.strip('"')
            
            if key in extracted_elements:
                extracted_elements[key] = value

    return extracted_elements



def parse_xml(xml_content):
    root = ET.fromstring(xml_content)
    xml_string = ET.tostring(root, encoding='utf-8').decode('utf-8')

    # {} 단위로 문자열 자르기
    curly_brackets = re.findall(r'{.*?}', xml_string)

    # 각각의 {} 내용을 , 단위로 잘라 리스트에 저장
    result_lists = []
    temp_list = []  # 일시적으로 저장할 리스트
    for brackets in curly_brackets:
        elements = [element.strip() for element in brackets[1:-1].split(',')]

        # "id"로 시작하는 리스트 병합
        if elements and (any('"id"' in element for element in elements) or (elements[0] == '"appCode":1019')):
            if temp_list:
                result_lists.append(temp_list)
            temp_list = elements
        else:
            temp_list.extend(elements)

    if temp_list:
        result_lists.append(temp_list)

    return result_lists


def full_shared_prefs(destination_dir,package_name):
    package_path=os.path.join(destination_dir,package_name,'shared_prefs')
    sharedprefs_list=os.listdir(package_path)
    for filename in sharedprefs_list:
        if package_name in filename:
            xml_filename=filename
            break
    package_path=os.path.join(package_path,xml_filename)
    tree = ET.parse(package_path)
    root = tree.getroot()

    # XML 내용을 문자열로 변환
    xml_content = ET.tostring(root, encoding='utf-8').decode('utf-8')


    lists = parse_xml(xml_content)
    for i, lst in enumerate(lists, 1):
        extracted_elements = extract_elements(lst)
        print(f"\nList {i} Elements:")
        for key, value in extracted_elements.items():
            if value is not None:
                print(f"{key}: {value}")


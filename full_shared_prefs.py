import xml.etree.ElementTree as ET
import re
from ppadb.client import Client as AdbClient

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

def parse_xml_android(xml_content):
    root = ET.fromstring(xml_content)
    xml_string = ET.tostring(root, encoding='utf-8').decode('utf-8')

    # {} 단위로 문자열 자르기
    curly_brackets = re.findall(r'{.*?}', xml_string)

    # 각각의 {} 내용을 , 단위로 잘라 리스트에 저장
    result_lists = []
    temp_list = []  # 일시적으로 저장할 리스트
    for brackets in curly_brackets:
        elements = [element.strip() for element in brackets[1:-1].split(',')]

        # "appCode":1019로 시작하는 리스트 병합
        if elements and elements[0] == '"appCode":1019':
            if temp_list:
                result_lists.append(temp_list)
            temp_list = elements
        else:
            temp_list.extend(elements)

    if temp_list:
        result_lists.append(temp_list)

    return result_lists

def parse_xml_ishredder(xml_content):
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
        if elements and any('"id"' in element for element in elements):
            if temp_list:
                result_lists.append(temp_list)
            temp_list = elements
        else:
            temp_list.extend(elements)

    if temp_list:
        result_lists.append(temp_list)

    return result_lists

def extract_shared_prefs(device, package_name):
    # ADB shell 명령어를 사용하여 파일 추출
    if package_name == "com.cbinnovations.androideraser":
        result = device.shell(f"su -c 'cat /data/data/{package_name}/shared_prefs/{package_name}.xml'")
    elif package_name == "com.projectstar.ishredder.android.standard":
        result = device.shell(f"su -c 'cat /data/data/{package_name}/shared_prefs/{package_name}_preferences.xml'")
    return result

def main():
    #app_package 는 입력으로 받기
    # ADB 연결
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    if not devices:
        print("No Android devices found.")
        return

    # 첫 번째 연결된 디바이스 사용
    device = devices[0]

    # 앱 패키지 이름 설정
    finding_app = input("Enter Finding APP (1 for AndroidEraser, 2 for iShredder): ")
    if finding_app == "1":
        app_package = "com.cbinnovations.androideraser"
    elif finding_app == "2":
        app_package = "com.projectstar.ishredder.android.standard"
    else:
        print("Invalid option for Finding APP. Please enter either 1 or 2.")
        return

    # packages.xml 추출
    xml_content = extract_shared_prefs(device, app_package)

    if finding_app == "1":
        lists = parse_xml_android(xml_content)
    elif finding_app == "2":
        lists = parse_xml_ishredder(xml_content)

    # 각 리스트에서 조건을 만족하는 요소 추출 및 출력
    for i, lst in enumerate(lists, 1):
        extracted_elements = extract_elements(lst)
        print(f"\nList {i} Elements:")
        for key, value in extracted_elements.items():
            if value is not None:
                print(f"{key}: {value}")

if __name__ == "__main__":
    main()
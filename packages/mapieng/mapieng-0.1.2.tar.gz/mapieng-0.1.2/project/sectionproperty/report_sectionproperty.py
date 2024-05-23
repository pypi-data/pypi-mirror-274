import requests
import json

url = "https://moa.rpm.kr-dv-midasit.com/backend/function-executor/python-execute/base.section_property/mdreport"

def Do(json_data):
    body = {
        "arguments": json_data
    }

    # 헤더 정의 (필요시)
    headers = {
        "Content-Type": "application/json"
    }

    # POST 요청 보내기
    response = requests.post(url, headers=headers, data=json.dumps(body))
    # 응답 결과 출력
    return response.text

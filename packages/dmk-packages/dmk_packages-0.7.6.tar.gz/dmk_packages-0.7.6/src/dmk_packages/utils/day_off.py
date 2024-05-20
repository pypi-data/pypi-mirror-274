import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv())


def check_day_off():
    today = datetime.now()
    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")

    url = (
        "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"
    )
    serviceKey = os.environ.get("DAY_OFF_API_KEY")
    params = {"solYear": f"{year}", "solMonth": f"{month}", "serviceKey": serviceKey}

    response = requests.get(url, params=params)

    root = ET.fromstring(response.text)
    dates = [item.find("locdate").text for item in root.findall(".//item")]

    holiday = []
    for date in dates:
        holiday.append(date)

    if today.strftime("%Y%m%d") in holiday:
        return True

    elif str(today.weekday()) == "5" or str(today.weekday()) == "6":
        return True

    else:
        return False

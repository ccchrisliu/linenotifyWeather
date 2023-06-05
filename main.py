import requests
import json
# import time
# import schedule

apiKey = "CWB-4F015353-9751-4FF8-A9FE-15E437947B04"#"apiKey"
lineToken = "0klaPv5PaPAgxHBxMEBagIi8ax6qHCyEl0je0qQ8zvF"#"lineToken"

# "https://api.openweathermap.org/data/2.5/weather?id=1668338&units=imperial&appid="
# def getData(key):
#     url = (
#         "https://api.openweathermap.org/data/3.0/onecall?lat=24.94702&lon=121.581749&exclude=current,minutely,hourly&appid="
#         + key
#     )

#     r = requests.get(url)
#     data = json.loads(r.text)

#     def tempToC(fTemp):
#         return round((fTemp - 32) * 5 / 9, 1)

#     now_temp = tempToC(data["main"]["temp"])
#     feels_like = tempToC(data["main"]["feels_like"])
#     temp_max = tempToC(data["main"]["temp_max"])
#     temp_min = tempToC(data["main"]["temp_min"])
#     temp = f"{data['name']} \n當前氣溫 {now_temp} \n體感溫度 {feels_like}\n最高溫 {temp_max}\n最低溫 {temp_min}"

#     return temp

def getData():

            # https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-4F015353-9751-4FF8-A9FE-15E437947B04&format=JSON&locationName=%E8%87%BA%E5%8C%97%E5%B8%82
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": "CWB-4F015353-9751-4FF8-A9FE-15E437947B04",
        "format":"JSON",
        "locationName": "%E8%87%BA%E5%8C%97%E5%B8%82",
    }

    response = requests.get("https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-4F015353-9751-4FF8-A9FE-15E437947B04&format=JSON&locationName=%E8%87%BA%E5%8C%97%E5%B8%82")#requests.get(url, params=params)
    print(response.status_code)

    if response.status_code == 200:
        # print(response.text)
        data = json.loads(response.text)

        location = data["records"]["location"][0]["locationName"]

        weather_elements = data["records"]["location"][0]["weatherElement"]
        start_time = weather_elements[0]["time"][0]["startTime"]
        end_time = weather_elements[0]["time"][0]["endTime"]
        weather_state = weather_elements[0]["time"][0]["parameter"]["parameterName"]
        rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
        min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
        comfort = weather_elements[3]["time"][0]["parameter"]["parameterName"]
        max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]

        print(location)
        print(start_time)
        print(end_time)
        print(weather_state)
        print(rain_prob)
        print(min_tem)
        print(comfort)
        print(max_tem)

        temp = f"{location} \n當前氣溫 {comfort} \n體感溫度 {weather_state}\n最高溫 {min_tem}\n最低溫 {min_tem}"
        return temp
    else:
        print("Can't get data!")
        return "Can't get data!"


temp = getData()


def sendToLine(token):
    url = "https://notify-api.line.me/api/notify"
    payload = {"message": {temp}}
    headers = {"Authorization": "Bearer " + lineToken}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


sendToLine(lineToken)

# schedule.every().day.at("07:30").do(sendToLine(lineToken,temp))
# schedule.every(10).seconds.do(sendToLine, (lineToken))

# while True:
#     schedule.run_pending()
#     time.sleep(1)
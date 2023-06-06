import requests
import json
from datetime import datetime, timedelta

apiKey = "786c1953ad62858f70c4e80b5abf27c8"
response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?id=7280290&units=metric&appid={apiKey}&lang=zh_tw")
print(response.status_code)

if response.status_code == 200:
    # print(response.text)
    data = json.loads(response.text)

    # 存取 JSON 資料
    cod = data["cod"]
    message = data["message"]
    cnt = data["cnt"]
    list_data = data["list"]
    city = data["city"]
    temp = ""
    next_day_string = ""
    # 迭代取出 list_data 中的每個資料
    for item in list_data:
        dt = item["dt"]
        main = item["main"]
        weather = item["weather"]
        clouds = item["clouds"]
        wind = item["wind"]
        visibility = item["visibility"]
        pop = item["pop"]
        popint = round(float(pop) *100, 2)
        rain = {}
        if "rain" in item:
            rain = item  ["rain"]                     
        sys = item["sys"]
        dt_txt = item["dt_txt"]
        
        # 輸出結果
        # print("Date/Time:", dt_txt)
        # print("DT:", dt)
        # print("Main:", main)
        # print("Weather:", weather)
        # print("Clouds:", clouds)
        # print("Wind:", wind)
        # print("Visibility:", visibility)
        # print("Pop:", pop)
        # print("Rain:", rain)
        # print("Sys:", sys)
        # print("")
        wea = weather[0]["description"]
        max = main["temp_max"]
        min = main["temp_min"]

        if next_day_string == "":
            date_time = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
            next_day = date_time + timedelta(days=1)
            # 設定時間為 "21:00:00"
            next_day = next_day.replace(hour=21, minute=0, second=0)
            # 將結果轉換回字串
            next_day_string = next_day.strftime("%Y-%m-%d %H:%M:%S")     
        dtnow = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
        dtdate = dtnow.strftime("%m/%d %H點")     
        # temp += f"{dtdate} 天氣:{wea} 降雨:{popint}% 最高溫:{max} 最低溫:{min} \n"
        if not rain:
            temp += f"{dtdate} <{wea}> -----------\n"
        else:
            temp += f"{dtdate} <{wea}> 降雨:{popint}%\n"


        if next_day_string == dt_txt:
            break

    print(temp)
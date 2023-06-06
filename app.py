import requests
import json
from flask import Flask, request, abort

# from linebot import (
#     LineBotApi, WebhookHandler
# )
# from linebot.exceptions import (
#     InvalidSignatureError
# )
# from linebot.models import *

#======python的函數庫==========
import tempfile, os
# import datetime
# import openai
# import time
#======python的函數庫==========

app = Flask(__name__)
# static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_api = os.getenv('LINE_TOKEN')
# Channel Secret
# handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# OPENAI API Key初始化設定
apiKey = os.getenv('API_KEY')


# def GPT_response(text):
#     # 接收回應
#     response = openai.Completion.create(model="text-davinci-003", prompt=text, temperature=0.5, max_tokens=500)
#     print(response)
#     # 重組回應
#     answer = response['choices'][0]['text'].replace('。','')
#     return answer
def getData():

            # https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-4F015353-9751-4FF8-A9FE-15E437947B04&format=JSON&locationName=%E8%87%BA%E5%8C%97%E5%B8%82
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": apiKey,
        "format":"JSON",
        "locationName": "%E8%87%BA%E5%8C%97%E5%B8%82",
    }

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

        # 迭代取出 list_data 中的每個資料
        for item in list_data:
            dt = item["dt"]
            main = item["main"]
            weather = item["weather"]
            clouds = item["clouds"]
            wind = item["wind"]
            visibility = item["visibility"]
            pop = item["pop"]
            popint = float(pop) *100
            rain = item["rain"]
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
            temp += f"時間:{dt_txt} 天氣:{wea} 降雨:{popint}% 最高溫:{max} 最低溫:{min} \n"
        return temp
    else:
        print("Can't get data!")
        return "Can't get data!"
def sendToLine(tmp):

    url = "https://notify-api.line.me/api/notify"
    payload = {"message": {tmp}}
    headers = {"Authorization": "Bearer " + line_api}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    

# 監聽所有來自 /callback 的 Post Request
@app.route("/getweather", methods=['GET'])
def callback():
    # # get X-Line-Signature header value
    # signature = request.headers['X-Line-Signature']
    # # get request body as text
    # body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)
    # # handle webhook body
    try:
        # handler.handle(body, signature)
        temp = getData()
        sendToLine(temp)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# # 處理訊息
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     msg = event.message.text    
#     GPT_answer = GPT_response(msg)
#     print(GPT_answer)
#     line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))
    

# @handler.add(PostbackEvent)
# def handle_message(event):
#     print(event.postback.data)


# @handler.add(MemberJoinedEvent)
# def welcome(event):
#     uid = event.joined.members[0].user_id
#     gid = event.source.group_id
#     profile = line_bot_api.get_group_member_profile(gid, uid)
#     name = profile.display_name
#     message = TextSendMessage(text=f'{name}歡迎加入')
#     line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
import requests
import json
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
# import tempfile, os
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

    response = requests.get(f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={apiKey}&format=JSON&locationName=%E8%87%BA%E5%8C%97%E5%B8%82")#requests.get(url, params=params)
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
def sendToLine(tmp):

    url = "https://notify-api.line.me/api/notify"
    payload = {"message": {tmp}}
    headers = {"Authorization": "Bearer " + line_api}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    

# 監聽所有來自 /callback 的 Post Request
@app.route("/getweather", methods=['POST'])
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
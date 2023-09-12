# linenotifyWeather
透過
連結：<[https://openweathermap.org/]><br/>
取得氣象預報<br/>
再把寫好的python呼叫架在render上 <[https://dashboard.render.com/]><br/>
呼叫網址:https://lineweathernotify.onrender.com/getweather
source code是呼叫app.py
再透過google scheduler<[https://console.cloud.google.com/cloudscheduler]>
改用這個去跑排程https://console.cron-job.org/
去跑排成呼叫<br/>
每天早上7:00在丟出今天到明天的降雨資料<br/>

另外還可以用中央氣象局 <[https://opendata.cwb.gov.tw/dist/opendata-swagger.html]>

#### 回傳結果:
【要下雨拉】 06/06 09點 天氣:小雨 降雨:42.0%
06/06 12點 <小雨> 降雨:50.0%<br/>
06/06 15點 <中雨> 降雨:55.0%<br/>
06/06 18點 <中雨> 降雨:69.0%<br/>
06/06 21點 <小雨> 降雨:61.0%<br/>
06/07 00點 <陰，多雲> -----------<br/>
06/07 03點 <小雨> 降雨:47.0%<br/>
06/07 06點 <中雨> 降雨:73.0%<br/>
06/07 09點 <中雨> 降雨:85.0%<br/>
06/07 12點 <小雨> 降雨:80.0%<br/>
06/07 15點 <多雲> -----------<br/>
06/07 18點 <小雨> 降雨:48.0%<br/>
06/07 21點 <小雨> 降雨:51.0%<br/>

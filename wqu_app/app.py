import os
from flask import Flask, request, render_template
from message import *
#import pandas as pd
import json

app = Flask(__name__)
DEPLOY = os.getenv('DEPLOY')


@app.route('/')
def main():
    if DEPLOY == 'heroku':
        ip_address = request.headers['X-Forwarded-For']     
    else:
        ip_address = retrieve_local_ip_address()   
    
    return render_template('index.html', message= str(greet(ip_address)))

@app.route('/weather')
def weather():

    if DEPLOY == 'heroku':
        ip_address = request.headers['X-Forwarded-For']     
    else:
        ip_address = retrieve_local_ip_address() 
    
    return render_template('weather.html', message = str(weather_data(ip_address)))

@app.route('/myweather', methods = ["GET","POST"])
def myweather():

    if request.method =="POST":    
        latitude = request.form["lat"]
        longitude = request.form["lon"]
        url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact'
        headers = {
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"}
        params = {'lat': latitude, 'lon': longitude}
        response = requests.get(url, params=params, headers = headers)
        data = response.json()
        dat = data['properties']['timeseries'][0]['data']['instant']['details']
        #data_df= pd.DataFrame.from_dict(dat, orient = 'index')
        #data_df
        dat_pretty = json.dumps(dat, indent = 4)

        return render_template('myweather.html', message = str(dat))
    else:
        return render_template('myweather.html')



if __name__ =='__main__':
    app.run(debug =True)

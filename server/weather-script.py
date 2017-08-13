#!/usr/bin/python2

# Kindle Weather Display
# Matthew Petroff (http://www.mpetroff.net/)
# September 2012

#import urllib2
#from xml.dom import minidom
import datetime
import codecs
import requests

class HeFengWeather:
    KEY = "your_api_key"
    DEF_CITY = "shanghai"
    API_URL = "https://free-api.heweather.com/v5/"
    def getAll(self, city):
        #api_type = "weather?"
        s = requests.session()
        url = self.getUrl(city, "weather?")
        raw_json = s.get(url).json()
        #
        if raw_json["HeWeather5"][0]["status"] != "ok":
            return
        #print(raw_json)
        #print("=======================")
        aqi_json = raw_json["HeWeather5"][0]["aqi"]
        daily_json = raw_json["HeWeather5"][0]["daily_forecast"][0]
        aqi = aqi_json["city"]["aqi"]
        max_tmp = daily_json["tmp"]["max"]
        min_tmp = daily_json["tmp"]["min"]
        day_info = daily_json["cond"]["txt_d"]
        night_info = daily_json["cond"]["txt_n"]
        wind_dir = daily_json["wind"]["dir"]
        wind_lvl = daily_json["wind"]["sc"]
        txt = "Day is %s and night is %s. Temperature is %s degrees to %s degrees. AQI is %s." %(day_info, night_info, min_tmp, max_tmp, aqi)
        return txt
    def getNow(self, city):
        #api_type = "weather?"
        s = requests.session()
        url = self.getUrl(city, "weather?")
        raw_json = s.get(url).json()
        #
        if raw_json["HeWeather5"][0]["status"] != "ok":
            return
        #print(raw_json)
        #print("=======================")
        aqi_json = raw_json["HeWeather5"][0]["aqi"]
        now_json = raw_json["HeWeather5"][0]["now"]
        aqi = aqi_json["city"]["aqi"]
        info = now_json["cond"]["txt"]
        tmp = now_json["tmp"]
        feel_tmp = now_json["fl"]
        txt = "Now is %s. Temperature is %s degrees and apparent temperature is %s degrees. AQI is %s." %(info, tmp, feel_tmp, aqi)
        return txt
    def getForecast(self, city):
        s = requests.session()
        url = self.getUrl(city, "forecast?")
        raw_json = s.get(url).json()
        #
        if raw_json["HeWeather5"][0]["status"] != "ok":
            return
        #print(raw_json)
        #print("=======================")
        forecast_json = raw_json["HeWeather5"][0]["daily_forecast"]
        forecast=[]
        for i in range(3):
            info = {}
            json = forecast_json[i]
            info['date'] = json['date'][6:]
            info['code_d'] = json['cond']['code_d']
            info['code_n'] = json['cond']['code_n']
            info['txt_d'] = json['cond']['txt_d']
            info['txt_n'] = json['cond']['txt_n']
            info['max_tmp'] = json['tmp']['max']
            info['min_tmp'] = json['tmp']['min']
            forecast.append(info)
        return forecast 
    def getUrl(self, city, api_type):
        return self.API_URL + api_type + "city=" + city + "&key=" + self.KEY + "&lang=en"
def getIcon(code, path):
    icons = []
    sz= len(code)
    for i in range(sz):

        fd = codecs.open(path + "/" + code[i] + ".svg", 'r', encoding='utf-8')

        fd.readline()
        fd.readline()
        fd.readline()
        icon = fd.read()
        old = 'xmlns="http://www.w3.org/2000/svg"'
        new = '%s id="icon_%d"' %(old, i)
        icon = icon.replace(old,new)
        icon = icon.replace('<?xml version="1.0" standalone="no"?>',"")

        icons.append(icon)
    return icons
def genSVG(highs, lows, date, icons):
    #
    # Preprocess SVG
    #

    # Open SVG to process
    output = codecs.open('weather-script-preprocess.svg', 'r', encoding='utf-8').read()
    
    # Insert icons and temperatures
    output = output.replace('ICON_0',icons[0]).replace('ICON_1',icons[1]).replace('ICON_2',icons[2]).replace('ICON_3',icons[3])
    #output = output.replace('ICON_ONE',icon).replace('ICON_TWO',icon).replace('ICON_THREE',icon).replace('ICON_FOUR',icon)
    output = output.replace('HIGH_ONE',str(highs[0])).replace('HIGH_TWO',str(highs[1])).replace('HIGH_THREE',str(highs[2])).replace('HIGH_FOUR',str(highs[3]))
    output = output.replace('LOW_ONE',str(lows[0])).replace('LOW_TWO',str(lows[1])).replace('LOW_THREE',str(lows[2])).replace('LOW_FOUR',str(lows[3]))

    # Insert days of week
    output = output.replace('DAY_ONE',date[0]).replace('DAY_TWO',date[1]).replace('DAY_THREE',date[2])
    
    # Write output
    now = datetime.datetime.now().strftime("%H:%M:%S  ")
    #print(now)
    output = output.replace('update',now)
    #output = output.replace('ICON_ONE',icon)
    codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)

def main():
    he = HeFengWeather();
    info = he.getForecast('shanghai')
    #print(str(info))
    highs =[]
    lows = []
    date= []
    code = []
    highs.append(info[0]['max_tmp'])
    lows.append(info[0]['min_tmp'])
    code.append(info[0]['code_d'])
    for i in range(3):
        day_info = info[i]
        highs.append(day_info['max_tmp'])
        lows.append(day_info['min_tmp'])
        code.append(day_info['code_d'])
        date.append(day_info['date'])

    #highs.append(highs[])
    icons = getIcon(code, 'svg')
    genSVG(highs, lows, date, icons) 
def test():
    
    highs =[30, 40, 50, 60]
    lows = [10, 20, 30, 40]
    date= ['7/30', '8/1', '8/2']
    code = ['100', '100', '100', '100']


    #highs.append(highs[])
    genSVG(highs, lows, date, code) 
if __name__ == '__main__':
    main()

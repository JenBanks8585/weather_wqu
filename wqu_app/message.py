import requests


#def retrieve_ip_adress():
#    """Return IP address of our computer."""
#    response = requests.get('https://api.ipify.org')
    
#    return response.text

def retrieve_local_ip_address():
    """Return IP address of our computer."""
    response = requests.get('https://api.ipify.org')
    
    return response.text


def get_geolocation(ip_address):
    """Return gelociaton of an IP address."""
    response = requests.get(f'https://ipinfo.io/{ip_address}')
    data = response.json()
    coords = [float(coord) for coord in data['loc'].split(',')]

    return coords

def get_weather(coords):
    """Return weather data for a given set of coordinates."""
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
        "Accept-Language": "en-US,en;q=0.9"
    }
    params = {'lat': coords[0], 'lon': coords[1]}

    response = requests.get(url, params=params, headers = headers)
    data = response.json()
    temperature = data['properties']['timeseries'][0]['data']['instant']['details']['air_temperature']
    
    return temperature, data


def greet(ip_address):
    #ip_address = retrieve_ip_adress() #-> ip adress of server
    
    coords = get_geolocation(ip_address)
    temperature_f = get_weather(coords)[0]
    temperature_c = 1.8*temperature_f + 32
    weather_data = get_weather(coords)[1]
    
    return f" Hello, the temperature is {temperature_f} degrees Celcius \n or {temperature_c} degrees Fahrenheit"


def weather_data(ip_address):
 
    coords = get_geolocation(ip_address)
    a = get_weather(coords)[1]
    b = [(a['properties']['timeseries'][i]['time'], a['properties']['timeseries'][i]['data']['instant']['details']) for i in range(len(a['properties']['timeseries']))]


    return b

if __name__=='__main__':
    print(greet())

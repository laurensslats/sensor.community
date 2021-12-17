import requests
import json

api_url_qubitro = "https://api.qubitro.com/v1/projects/{your ProductID}/devices/{add your deviceID}/data?keys=temperature,humidity,pm10,pm25&period=1&limit=1"
headers_qubitro = {
    "Accept": "application/json",
    "Authorization": "Bearer {add your API key}" 
}
api_url_POST = "https://api.sensor.community/v1/push-sensor-data/"
headers_sensorcommunity = {
    "Content-Type":"application/json",
    "X-Pin": "1",
    "X-Sensor": "{add your sensorID}"
}

def post_data():
    response = requests.get(api_url_qubitro, headers=headers_qubitro).json()

    data = response['response']

    for humidity_value in data:
        humidity = humidity_value['humidity']

    for temperature_value in data:
        temperature = temperature_value['temperature']

    for pm25_value in data:
        pm25 = pm25_value['pm25']

    for pm10_value in data:
        pm10 = pm10_value['pm10']

    sensordata = {"sensordatavalues":[{"value_type":"P1","value":pm10},{"value_type":"P2","value":pm25}]}

    response = requests.post(api_url_POST, headers=headers_sensorcommunity, data=json.dumps(sensordata))

if __name__ == '__main__':
    post_data()

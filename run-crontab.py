import requests
import json
import logging
import os

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

dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'time-post-data.log')

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(filename)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

def post_data():
    response = requests.get(api_url_qubitro, headers=headers_qubitro).json()

    print("response = ", response)

    data = response['response']
    print("data = ", data)

    for humidity_value in data:
        humidity = humidity_value['humidity']
        print("Humidity = ", humidity)

    for temperature_value in data:
        temperature = temperature_value['temperature']
        print("Temperature = ", temperature)

    for pm25_value in data:
        pm25 = pm25_value['pm25']
        print("PM2.5 = ", pm25)

    for pm10_value in data:
        pm10 = pm10_value['pm10']
        print("PM10 = ", pm10)

    sensordata = {"sensordatavalues":[{"value_type":"P1","value":pm10},{"value_type":"P2","value":pm25}]}

    print("sensordata = ", sensordata)

    response = requests.post(api_url_POST, headers=headers_sensorcommunity, data=json.dumps(sensordata))

    print(response.status_code)
    print(response.json())

def do_logging():
    logger.info("sending data")

if __name__ == '__main__':
    post_data()
    do_logging()


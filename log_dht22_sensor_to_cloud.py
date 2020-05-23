#!/usr/bin/env python3

import os
import sys
import Adafruit_DHT
from datetime import datetime
from time import sleep
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from google.auth.transport.requests import Request
import requests

SENSOR_GPIO_PIN=14

CLOUD_FUNCTION_URL="https://europe-west3-idlecode-va-data-collection.cloudfunctions.net/bq_sensor_data_upload"


def upload_sensor_data(temperature: float, humidity: float):
    keyfile_path = os.path.join(os.path.dirname(__file__), 'ra-raspberry-pi.service-account.json')
    
    credentials = service_account.IDTokenCredentials.from_service_account_file(keyfile_path, target_audience=CLOUD_FUNCTION_URL)

    credentials.refresh(Request())

    token = credentials.token
    authed_session = AuthorizedSession(credentials)
    response = requests.get(
            CLOUD_FUNCTION_URL,
            params={
                "temperature": temperature,
                "humidity": humidity
            },
            headers={
                "Authorization": "Bearer {}".format(token)
                }
            )

    response.raise_for_status()
    print("Upload successful")


def save_in_file(path: str, temperature: float, humidity: float):
    with open(path, mode='w') as f:
        print("Temp: {:.1f}*C".format(temperature), file=f)
        print("Hum:  {:.1f}%".format(humidity), file=f)


def log_record(last_status_path: str):
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, SENSOR_GPIO_PIN)
    delay = 3
    while humidity > 100:
        print("Invalid humidity value {humidity} - retrying in {delay}s".format(humidity=humidity, delay=delay))
        sleep(delay)
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, SENSOR_GPIO_PIN)

    print("Sensor data:", temperature, humidity)
    upload_sensor_data(temperature, humidity)
    if last_status_path:
        print("Saving last status to file:", last_status_path)
        save_in_file(last_status_path, temperature, humidity)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        log_record(None)
    else:
        log_record(sys.argv[1])


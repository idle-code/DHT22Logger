#!/usr/bin/env python3

import sys
import csv
import Adafruit_DHT
from datetime import datetime

SENSOR_GPIO_PIN=4

def log_record(filename: str):
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, SENSOR_GPIO_PIN)
    humidity = "{0:.2f}".format(humidity)
    temperature = "{0:.2f}".format(temperature)
    current_time = datetime.now().isoformat()
    log_tuple = (current_time, temperature, humidity)
    print(log_tuple)
    with open(filename, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(log_tuple)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("No CSV file provided")
    filename = sys.argv[1]
    print("Logging into {}".format(filename))
    log_record(filename)


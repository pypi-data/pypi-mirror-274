"""
example for ISLabTech UPW Sensor

read conductivity and temperature from sensor and print them into console
"""

import islabtech_upw_sensor_v1 as upw
from time import sleep

sensor = upw.Device.connect_via_network("192.168.1.123", 80)  # insert sensor IP address
while True:
    print(sensor.latest_measurement())
    sleep(1)

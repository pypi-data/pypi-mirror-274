# Python Remote for ISLabTech UPW Sensor

Python client library to communicate with the [ISLabTech UPW Sensor](https://gitlab.com/islabtech/upw-sensor)

## Setup

1. install the Python package:

```sh
pip install islabtech_upw_sensor_v1
```

2. connect the sensor and your computer to the same network, e.g. via WiFi or Ethernet
3. read the IP address from the display of the sensor
4. run this example snippet:

```python
import islabtech_upw_sensor_v1 as upw
from time import sleep

sensor = upw.Device.connect_via_network("192.168.x.x") # insert sensor IP address
while True:
    print(sensor.latest_measurement())
    sleep(1)
```

## Examples

Examples are in the [examples](https://gitlab.com/islabtech/upw-sensor/remote-python/-/tree/main/islabtech_upw_sensor_v1/examples) directory. Try out the [Getting Started](https://gitlab.com/islabtech/upw-sensor/remote-python/-/blob/main/islabtech_upw_sensor_v1/examples/0100%20getting%20started.ipynb) example.

## License

This project is licensed under the [Apache 2 license](LICENSE.txt).

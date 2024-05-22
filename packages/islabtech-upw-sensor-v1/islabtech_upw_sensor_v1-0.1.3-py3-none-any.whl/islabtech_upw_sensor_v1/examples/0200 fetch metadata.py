import islabtech_upw_sensor_v1 as upw

sensor = upw.Device.connect_via_network("192.168.1.123", 80)  # insert sensor IP address

status = sensor.system_status()
print(status)

print("hardware version :", status.hardware.version)
print("firmware version :", status.firmware.version)
print("sensor clock     :", status.time.current_time.astimezone())

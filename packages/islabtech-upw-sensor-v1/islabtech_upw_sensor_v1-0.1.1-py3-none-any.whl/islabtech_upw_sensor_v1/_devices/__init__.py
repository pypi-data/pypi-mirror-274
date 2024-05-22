"""
Copyright 2023 Ilka Schulz Labortechnik UG (haftungsbeschränkt)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations


from typing import Optional
from serial import Serial

from islabtech_upw_sensor_v1._devices._implementations import Interface
from islabtech_upw_sensor_v1._devices._implementations import NetworkInterface
from islabtech_upw_sensor_v1.measurements import Measurement, SuccessfulMeasurement

# from islabtech_upw_sensor._devices._implementations import USBInterface


class Device(Interface):
    _interface: Interface
    """
    the used interface, e.g. `NetworkInterface` or `USBInterface`
    
    Design pattern: TODO: name
    """

    @staticmethod
    def connect_via_network(ip_address: str, port: Optional[int] = 80) -> Device:
        device = Device()
        device._interface = NetworkInterface(ip_address, port)
        return device

    # @staticmethod
    # def connect_via_usb(serial_port: None | str | Serial) -> Device:
    #     raise NotImplementedError()

    def latest_measurement(self) -> Measurement:
        return self._interface.latest_measurement()

    latest_measurement.__doc__ = Interface.latest_measurement.__doc__

    def latest_successful_measurement(self) -> SuccessfulMeasurement:
        return self._interface.latest_successful_measurement()

    latest_successful_measurement.__doc__ = (
        Interface.latest_successful_measurement.__doc__
    )

    def measurement_history(self) -> list[Measurement]:
        return self._interface.measurement_history()

    measurement_history.__doc__ = Interface.measurement_history.__doc__

    def system_status(self) -> SystemStatus:
        return self._interface.system_status()

    system_status.__doc__ = Interface.system_status.__doc__

    #
    # def temperature_calibration(self):
    #     raise NotImplementedError()

    #
    # def conductivity_calibration(self):
    #     raise NotImplementedError()

    #
    # def settings(self):
    #     return self._interface.settings()

    # settings.__doc__ = super().settings.__doc__

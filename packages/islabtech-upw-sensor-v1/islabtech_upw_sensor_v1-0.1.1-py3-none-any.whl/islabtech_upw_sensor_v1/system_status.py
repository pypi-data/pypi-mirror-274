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

from dataclasses import dataclass, make_dataclass
import datetime


@dataclass
class FirmwareUpdatesSystemStatus:
    enabled: bool
    """whether automatic updates are enabled"""


@dataclass
class FirmwareSystemStatus:
    version: str
    updates: FirmwareUpdatesSystemStatus


@dataclass
class HardwareSystemStatus:
    version: str
    """hardware version"""

    serial_number: str
    """unique serial number identifying this device"""


@dataclass
class TimeSystemStatus:
    milliseconds_since_boot: int
    """milliseconds elapsed since device last booted"""

    seconds_since_boot: int
    """seconds elapsed since device last booted"""

    current_time: datetime.datetime
    """current system time of the device"""


@dataclass
class SystemStatus:
    firmware: FirmwareSystemStatus
    hardware: HardwareSystemStatus
    time: TimeSystemStatus

    @staticmethod
    def from_json(data: dict) -> SystemStatus:
        # TODO: ensure that all fields are initialized
        return SystemStatus(
            firmware=FirmwareSystemStatus(
                version=data["firmware"]["version"], updates=data["firmware"]["updates"]
            ),
            hardware=HardwareSystemStatus(
                version=data["hardware"]["version"],
                serial_number=data["hardware"]["serial_number"],
            ),
            time=TimeSystemStatus(
                milliseconds_since_boot=data["time"]["milliseconds_since_boot"],
                seconds_since_boot=data["time"]["seconds_since_boot"],
                current_time=datetime.datetime.fromtimestamp(
                    data["time"]["epoch_time"], datetime.UTC
                ),
            ),
        )

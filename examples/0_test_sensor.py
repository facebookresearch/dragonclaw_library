#   Copyright (c) Meta Platforms, Inc. and affiliates.

from dragonclaw_library.dragonclaw_sensor import DragonClawSensor

sensor = DragonClawSensor("/dev/ttyACM0")

try:
    while True:
        sensorData = sensor.read_sensor()

        if sensorData is not None:
            sensor.print_data(sensorData)
except KeyboardInterrupt:
    sensor.stop()

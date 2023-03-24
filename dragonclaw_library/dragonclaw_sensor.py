#   Copyright (c) Meta Platforms, Inc. and affiliates.

from collections import namedtuple
import serial
import struct
import numpy as np


class DragonClawSensor:
    '''
    Base class for the ReSkin sensing on the DragonClaw

    Methods
    -------
    read_sensor()
        Returns a sample of data from the sensor

    print_data(sorted_data)
        Prints sensor data

    concat_data(sorted_data)
        Makes acquiring data for specific variables (temp, Bx, By, Bz, Bmag) easier to access

    stop()

    '''
    def __init__(self, comport="/dev/ttyACM0", baud=115200):
        self.ser = serial.Serial(comport, baud)
        # connected = self.client.connectToDevice(device=comport)
        if not self.ser.isOpen():
            raise Exception(
                "Communication with QtPy on serial port: %s and baud rate: %d not achieved"
                % (comport, baud)
            )

        self.init_success = True
        self.n_type = 4
        self.n_sensor = 7
        self.t_us = [0]
        self.x_uT = [0] * self.n_sensor
        self.y_uT = [0] * self.n_sensor
        self.z_uT = [0] * self.n_sensor
        self.mag_uT = [0] * self.n_sensor

    def read_sensor(self):
        data = namedtuple(
            "data", ["timestamp_us", "temp_C", "x_uT", "y_uT", "z_uT", "mag_uT"]
        )
        temp_C = np.empty(self.n_sensor, dtype=float)
        x_uT = np.empty(self.n_sensor, dtype=float)
        y_uT = np.empty(self.n_sensor, dtype=float)
        z_uT = np.empty(self.n_sensor, dtype=float)
        mag_uT = np.empty(self.n_sensor, dtype=float)

        if self.ser.inWaiting() < 1:
            return None

        packet = self.ser.read(118)
        unpack_packet_tuple_full = struct.unpack("<29f", packet[0:-2])
        timestamp_qtpy = unpack_packet_tuple_full[0]
        unpack_packet_tuple = unpack_packet_tuple_full[1:]

        for ix, iy in zip(
            range(0, len(unpack_packet_tuple), self.n_type), range(self.n_sensor)
        ):
            temp_C[iy] = unpack_packet_tuple[ix]
            x_uT[iy] = unpack_packet_tuple[ix + 1]
            y_uT[iy] = unpack_packet_tuple[ix + 2]
            z_uT[iy] = unpack_packet_tuple[ix + 3]
            mag_uT[iy] = ((x_uT[iy] ** 2) + (y_uT[iy] ** 2) + (z_uT[iy] ** 2)) ** 0.5

        sorted_data = data(timestamp_qtpy, temp_C, x_uT, y_uT, z_uT, mag_uT)

        return sorted_data

    def print_data(self, sorted_data):
        if sorted_data is None:
            return None
        if sorted_data._fields is None:
            return None
        else:
            print("\n")
            for data_info, data_type in zip(sorted_data, sorted_data._fields):
                print(data_type, " ", data_info)

    def concat_data(self, sorted_data):
        if sorted_data is None:
            return self.t_us, self.x_uT, self.y_uT, self.z_uT, self.mag_uT
        if sorted_data._fields is None:
            return self.t_us, self.x_uT, self.y_uT, self.z_uT, self.mag_uT
        else:
            self.t_us = np.vstack((self.t_us, sorted_data[0]))
            self.x_uT = np.vstack((self.x_uT, sorted_data[2]))
            self.y_uT = np.vstack((self.y_uT, sorted_data[3]))
            self.z_uT = np.vstack((self.z_uT, sorted_data[4]))
            self.mag_uT = np.vstack((self.mag_uT, sorted_data[5]))
            return self.t_us, self.x_uT, self.y_uT, self.z_uT, self.mag_uT

    def stop(self):
        self.ser.stop()

#   Copyright (c) Meta Platforms, Inc. and affiliates.

import serial
import numpy as np
import struct
from collections import namedtuple


class DragonClaw:
    '''
    Base class for the DragonClaw pneumatic system

    Methods
    -------
    read_press()
        Returns the commanded and measured pressure data

    concat_data(sorted_data)
        Makes acquiring data for specific variables (commanded, true) easier to access

    grasp()
        Sets all the pressures to 100% to contract the whole hand

    release()
        Sets all the pressures to 0% to relax the whole hand
        
    set_press(actuation_array)
        Set the % pressure input (ranging from 0-2bar), i.e. [25,50,0,100] >> pointer is at 25%, middle is at 50%, thumb is at 0%, and palm is at 100% pressure input

    stop_handler()

    '''
    def __init__(self, comport="/dev/ttyACM0", baud=115200):
        self.ser = serial.Serial(comport, baud)
        if not self.ser.isOpen():
            raise Exception(
                "Communication with gripper on serial port: %s and baud rate: %d not achieved"
                % (comport, baud)
            )

        self.init_success = True
        self.n_pneunet = 4
        self.t_us = [0]
        self.cmnd_press = [0] * self.n_pneunet
        self.true_press = [0] * self.n_pneunet
        # self.test_attr = 7
        self.release()

    def _print_data(self, sorted_data):
        if sorted_data is None:
            return None
        if sorted_data._fields is None:
            return None
        else:
            print("\n")
            for data_info, data_type in zip(sorted_data, sorted_data._fields):
                print(data_type, " ", data_info)

    def read_press(self):
        data = namedtuple("data", ["timestamp_us", "command", "true"])
        command_press = np.empty(self.n_pneunet, dtype=int)
        true_press = np.empty(self.n_pneunet, dtype=int)

        if self.ser.inWaiting() < 1:
            return None

        packet = self.ser.read_until()
        while len(packet) != 38:
            self.ser.reset_input_buffer()
            packet = self.ser.read_until()
            # a = len(packet)

        unpack_packet_tuple_full = struct.unpack("<9f", packet[0:-2])
        # print("\n", unpack_packet_tuple_full)
        timestamp_teensy = unpack_packet_tuple_full[0]  # micros
        unpack_packet_tuple = unpack_packet_tuple_full[1:]

        for ix in range(self.n_pneunet):
            command_press[ix] = unpack_packet_tuple[ix]
            true_press[ix] = unpack_packet_tuple[ix + 4]

        sorted_data = data(timestamp_teensy, command_press, true_press)
        # self._printData(sorted_data)

        return sorted_data

    def concat_data(self, sorted_data):
        if sorted_data is None:
            return self.t_us, self.cmnd_press, self.true_press
        if sorted_data._fields is None:
            return self.t_us, self.cmnd_press, self.true_press
        else:
            self.t_us = np.vstack((self.t_us, sorted_data[0]))
            self.cmnd_press = np.vstack((self.cmnd_press, sorted_data[1]))
            self.true_press = np.vstack((self.true_press, sorted_data[2]))
            return self.t_us, self.cmnd_press, self.true_press

    def grasp(self):  # full actuation
        self.ser.reset_output_buffer()
        self.ser.write("[100,100,100,100]".encode("utf-8"))
        print("\nfull grasp")
        self.ser.reset_input_buffer()

    def release(self):  # full relaxation
        self.ser.reset_output_buffer()
        self.ser.write("[0,0,0,0]".encode("utf-8"))
        print("\nfull release")
        self.ser.reset_input_buffer()

    def set_press(self, actuation_array):  # send over pyserial as [p1,p2,p3,p4]
        pressure_in_string = str(actuation_array)
        self.ser.reset_output_buffer()
        self.ser.write(pressure_in_string.encode("utf-8"))
        # print("\nsent to teensy: ", pressureIn_string)
        self.ser.reset_input_buffer()

    def stop_handler(self):
        self.release()
        self.ser.close()
        exit()

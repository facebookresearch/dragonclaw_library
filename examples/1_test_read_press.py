#   Copyright (c) Meta Platforms, Inc. and affiliates.

from collections import namedtuple
import struct
import time

from dragonclaw_library import DragonClaw


claw = DragonClaw("/dev/ttyACM0")
claw.grasp()

claw.ser.reset_input_buffer()
time.sleep(2)

packet = claw.ser.read_until("\n")
unpack_packet_tuple = struct.unpack("<8i", packet[0:-3])

print("\n", str(unpack_packet_tuple))

command_press = [0] * 4
true_press = [0] * 4

for ix in range(4):
    command_press[ix] = unpack_packet_tuple[ix]
    true_press[ix] = unpack_packet_tuple[ix + 4]

print("\n", str(true_press))

data = namedtuple("data", ["command", "true"])
sorted_data = data(command_press, true_press)

for data_info, data_type in zip(sorted_data, sorted_data._fields):
    print(data_type, " ", data_info)

claw.release()

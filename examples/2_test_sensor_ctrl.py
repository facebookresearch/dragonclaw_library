#   Copyright (c) Meta Platforms, Inc. and affiliates.
from polymetis import RobotInterface, GripperInterface
from dragonclaw_library import DragonClawSensor
import time
import numpy as np
import torch

sensor = DragonClawSensor("/dev/ttyACM0")
sensorData = sensor.readSensor()
base_z_mT = np.mean(sensorData.z_mT[0:3])

robot = RobotInterface(
    ip_address="000.00.0.0",
)

ee_pos_moveUp = torch.Tensor([0,0,0.05])
ee_pos_moveDown = torch.Tensor([0,0,-0.05])

while True:
    ee_current_pos = robot.get_ee_pose()

    if base_z_mT < 0:
        print(f"\nMoving UP ...\n")
        state_log = robot.move_to_ee_pose(
            position=ee_pos_moveUp, orientation=None, time_to_go=2.0, delta=True
        )
        time.sleep(0.5)
    elif base_z_mT > 0:
        print(f"\nMoving DOWN ...\n")
        state_log = robot.move_to_ee_pose(
            position=ee_pos_moveDown, orientation=None, time_to_go=2.0, delta=True
        )
        time.sleep(0.5)
    time.sleep(0.1)

time.sleep(2)

gripper.release()

gripper.stop()
sensor.stop()

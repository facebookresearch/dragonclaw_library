# dragonclaw_library
This is a python library designed to interface with the [DragonClaw](https://vasu1360.github.io/DragonClaw/). The library implements two classes: 
`DragonClaw`, which implements methods to actuate the fingers, and `DragonClawSensor`, which can be used
to read data from the ReSkin sensing integrated with the [DragonClaw](https://vasu1360.github.io/DragonClaw/). 

## Installation
1. Clone this repository
```
git clone https://github.com/vasu1360/dragonclaw_library.git
```
2. Install this package using pip
```
pip install -e .
```

## Usage
1. Connect the two finger and thumb sensor strands to the [multiplexer](https://www.sparkfun.com/products/16784), which should be connected to the [microcontroller](https://www.adafruit.com/product/4600) (MCU). 

2. Use a USB C cable to connect the MCU to a computer with Arduino IDE and upload the DragonClaw_sensor_mux.ino code.

3. Use another USB C cable to connect the [MCU](https://www.pjrc.com/store/teensy40.html) controlling the pneumatic system and upload the DragonClaw_pythonCom_fourChnls.ino code. 

4. Each of the four pressure inlets should be connected to their own [proportional pressure control](https://www.festo.com/us/en/a/download-document/datasheet/8046305) valve, which will be connected to the [pressure regulator](https://www.festo.com/hk/en/a/download-document/datasheet/529166) set to 2bar (200kPa). The regulator can be connected to any source of compressed air. 

5. Once the power source for the pneumatic system control PCB is connected, each of the fingers will flex and extend in turn.

6. If mounting the DragonClaw to a robot arm, specifically a [Franka Emika Panda arm](https://www.franka.de/), use two M6 bolts to attach the DragonClaw palm to the end effector. 

7. Use 2_test_sensor_ctrl.py to verify that the sensor readings can be used to control the movement of the arm. Make sure to install [Polymetis](https://facebookresearch.github.io/fairo/polymetis/).


## License 
This work is licensed under a
[Creative Commons Attribution - NonCommercial 2.0 Generic License][cc-by].

[![CC BY NC][cc-by-image]][cc-by]

[cc-by]: https://creativecommons.org/licenses/by-nc/2.0/
[cc-by-image]: https://i.creativecommons.org/l/by-nc/2.0/88x31.png


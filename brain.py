#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEX MCP
#	Author:       Ian & Erickson
#	Created:      September 17 2026
#	Description:  Run this on the brain for other things to work
#
# ------------------------------------------

# Library imports
from vex import *

# Begin project code
import sys

motor_1.set_velocity(30, PERCENT)
motor_1.stop()

try:
    exec("print('EXEC_READY')")
except Exception as error:
    print("EXEC_UNAVAILABLE:", error)
    raise

code_lines = []
receiving = False

print("READY")

while True:
    line = sys.stdin.readline()

    if not line:
        wait(20, MSEC)
        continue

    line = line.rstrip("\r\n")

    if line == "__BEGIN_CODE__":
        code_lines = []
        receiving = True
        print("RECEIVING")

    elif line == "__END_CODE__" and receiving:
        receiving = False
        source = "\n".join(code_lines)
        code_lines = []

        try:
            exec(source, globals())
            print("OK: execution finished")
        except Exception as error:
            print("ERROR:", error)
        finally:
            motor_1.stop()

    elif line == "stop":
        receiving = False
        code_lines = []
        motor_1.stop()
        print("OK: stopped")

    elif receiving:
        code_lines.append(line)

    elif line:
        print("ERROR: expected __BEGIN_CODE__")

    wait(20, MSEC)
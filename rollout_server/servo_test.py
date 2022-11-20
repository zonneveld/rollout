
from threading import Timer
import time

from adafruit_servokit import ServoKit

class IntervalTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            try:
                self.function(*self.args, ** self.kwargs)
            except:
                print("stop")
                break

TEST_SERVO = 1

servos = ServoKit(channels=16)

def write_servo(channel,angle):
    servos.servo[channel].angle = angle

def append_servo(channel,angle):
    nangle = servos.servo[channel].angle + angle
    write_servo(channel,nangle)

def trigger_servo(channel, delay, angle_home,angle_target):
    write_servo(channel,angle_target)
    on_trigger = lambda : write_servo(channel,angle_home)
    timer = Timer(delay,on_trigger)
    timer.start()

sweep_left = lambda : append_servo(TEST_SERVO,1)
sweep_right = lambda : append_servo(TEST_SERVO,-1)

# itimer = IntervalTimer(0.01,sweep_left)
# write_servo(TEST_SERVO,0)
print("go!")

trigger_servo(TEST_SERVO,2,0,180)

# itimer.start()
# time.sleep(3)
# itimer.cancel()
# time.sleep(1)
# itimer = IntervalTimer(0.01,sweep_right)
# itimer.start()
print("end!")


# print("start")
# write_servo(TEST_SERVO,0)
# try:
#     while True:
#         append_servo(TEST_SERVO, 10)
#         time.sleep(0.5)
# except:
#     print("oopsy!")
# finally:
#     write_servo(TEST_SERVO,0)
# print("end")
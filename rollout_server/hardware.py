from adafruit_motorkit import MotorKit
from adafruit_servokit import ServoKit

from PIL import Image, ImageDraw,ImageFont
import adafruit_ssd1306
import board


# import time
from threading import Timer

class IntervalTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            try:
                self.function(*self.args, ** self.kwargs)
            except:
                # print("stop")
                self.cancel()
                break


# Display data
WIDTH = 128
HEIGHT = 32
OFFSET = 0
FONT = ImageFont.load_default()
display = adafruit_ssd1306.SSD1306_I2C(WIDTH,HEIGHT,board.I2C())
image = Image.new("1",(display.width,display.height))
imagebuffer = ImageDraw.Draw(image)

def display_write(text):
    imagebuffer.rectangle(
        (0,0,display.width, display.height),
        outline=0,
        fill=0,
    )
    imagebuffer.text(
        (OFFSET,OFFSET),
        text,
        font = FONT,
        fill = 255,
    )
    display.image(image)
    display.show()	


# Servo Data
servos = ServoKit(channels=16)
servos.servo[0].set_pulse_width_range(500, 2500)
servos.servo[1].set_pulse_width_range(500, 2500)
sweep_interval = None

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

def sweep_servo_start(channel,delay,step):
    global sweep_interval
    update_step = lambda: append_servo(channel,step)
    if isinstance(sweep_interval,Timer):
        sweep_interval.cancel()
    sweep_interval =IntervalTimer(delay,update_step)
    sweep_interval.start()

def sweep_servo_end():
    if isinstance(sweep_interval,Timer):
        sweep_interval.cancel()


# Motor Data
# motors = MotorKit()
mkit = MotorKit()
motors = [
    mkit.motor1,
    mkit.motor2,
    mkit.motor3,
    mkit.motor4
]

MAX = 1
drive_modus ={
    "coast":                    [None,None],
    "forward":                  [MAX,MAX],    
    "backward":                 [-MAX,-MAX],
    "brake":                    [0,0],
    "left_turn":                [MAX,0],
    "right_turn":               [0,MAX],
    "rotate_clockwise":         [MAX,-MAX],
    "rotate_counterclockwise":  [-MAX,MAX]
}



def set_motor_modus(modus):
    if modus in drive_modus:
        motors[0].throttle = drive_modus[modus][0]
        motors[3].throttle = drive_modus[modus][1]
        return True
    else:
        return False

def set_motor_mode(left_value,right_value):
    try:
        motors[0].throttle = left_value
        motors[3].throttle = right_value
        return True
    except:
        return False

def set_motor(target,value):
    try:
        motors[target -1].throttle = float(value)
        return True
    except:
        motors[target -1].throttle = None
        return False


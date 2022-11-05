from adafruit_motorkit import MotorKit
from adafruit_servokit import ServoKit

from PIL import Image, ImageDraw,ImageFont
import adafruit_ssd1306
import board
import time

WIDTH = 128
HEIGHT = 32
OFFSET = 0
FONT = ImageFont.load_default()

display = adafruit_ssd1306.SSD1306_I2C(WIDTH,HEIGHT,board.I2C())
image = Image.new("1",(display.width,display.height))
imagebuffer = ImageDraw.Draw(image)

servos = ServoKit(channels=16)
motors = MotorKit()

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



def write_servo(channel,angle):
    servos.servo[channel].angle = angle

def read_servo(channel):
    return servos.servo[channel].angle

def write_append(channel,angle):
    npos = read_servo(channel) + angle
    print(npos)
    if npos > 180:
        write_servo(channel,180)
        print("stop top")
    elif npos <= 0:
        write_servo(channel,0)
        print("stop bottom")
    else:
        write_servo(channel,npos)

def retour_servo(channel,angle,delay):
    start =  read_servo(channel)
    write_servo(channel,angle)
    time.sleep(delay)
    write_servo(channel,start)

def travel_servo(channel,step,delay):
    global traveling
    traveling = True
    while traveling:
        write_append(channel,step)
        if read_servo(channel) > 180 or read_servo(channel) < 0:
            print("exit")
            traveling = False
        time.sleep(delay)

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
        motors.motor1.throttle = drive_modus[modus][0]
        motors.motor4.throttle = drive_modus[modus][1]
        return True
    else:
        return False

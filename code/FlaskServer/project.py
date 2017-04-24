import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import os

import picamera

import time
from time import sleep

from Adafruit_PWM_Servo_Driver import PWM
from flask import Flask, render_template, request, redirect

pwm = PWM(0x40, debug=False)

servoMin = 115  # Min pulse length out of 4096
servoMax = 605  # Max pulse length out of 4096

pwm.setPWMFreq(60) 

def setDegree(channel, d):
    degreePulse = servoMin
    degreePulse += int((servoMax - servoMin) / 180.0 * d)
    pwm.setPWM(channel, 0, degreePulse)


def timestamp():
        return time.strftime("%Y_%m_%d_%H-%M-%S")


app = Flask(__name__, "/static")

@app.route('/')
def interface():
	return render_template('LinuxProject.html')

@app.route('/gallery/')
def gallery():
	return render_template('Gallery.html', images=image_list())

@app.route("/latest_picture")
def latest_image():
    return open("static/images/"+latest, "rb").read()

def image_list():
    return sorted([f for f in os.listdir("static/images") if f != "blank.gif"])[::-1]


latest = "blank.gif"
if len(image_list()) > 0:
    latest = image_list()[0]

@app.route("/take_picture")
def take_picture():
    global latest
    
    try:
        yaw = int(request.args.get('yaw')) #left/right
        pitch = int(request.args.get('pitch')) #up/down
    except:
        return "error"
    originalYaw = yaw
    originalPitch = pitch
    
    if yaw > 180:
        yaw -= 180
        pitch = 180 - pitch

    setDegree(0, yaw)
    setDegree(3, pitch)

    sleep(1)

    latest = timestamp()+".jpg"
    camera = picamera.PiCamera()
    fn = "static/images/"+latest
    camera.capture(fn)
    camera.close()

    img = Image.open(fn)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("FreeSans.ttf", 32)
    draw.rectangle([0, 0, 350, 70], (0,0,0))
    draw.text((0, 0), "Horizontal: " + str(originalYaw) + " degrees", font=font)
    draw.text((0, 32), "Vertical: " + str(originalPitch) + " degrees", font=font)
    img.save(fn)
    
    return redirect("/?pitch="+str(pitch)+"&yaw="+str(yaw))

if __name__ == '__main__':
        app.debug = True
	app.run(host = '0.0.0.0', port = 5000, debug = True)

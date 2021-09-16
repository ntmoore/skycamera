import time
import os

# https://learn.adafruit.com/raspberry-pi-hq-camera-low-light-long-exposure-photography?view=all
from fractions import Fraction
from picamera import PiCamera
camera = PiCamera()
#camera.resolution = (2592,1944)


#parameters
sunset_hr=7.3+0.5
dawn_hr=6.75-0.5
daytime_period_min=10
nighttime_period_min=10

#Is it day or night?
time.localtime()
print("program starts at ",time.localtime);
hour = time.localtime()[3]
minute = time.localtime()[4]
hour_float = 1.0*hour+minute/60.0
if( hour_float>(sunset_hr+12) or hour_float<dawn_hr ):
    old_daytime=0
else :
    old_daytime=1


while(1):

    #Is it day or night?
    time.localtime()
    hour = time.localtime()[3]
    minute = time.localtime()[4]
    hour_float = 1.0*hour+minute/60.0
    if( hour_float>(sunset_hr+12) or hour_float<dawn_hr ):
        daytime=0
    else :
        daytime=1
    print("Is it day? ",daytime)
    #check for changing dak/light transitions
    sun_just_set=0
    sun_just_rose=0
    if( daytime==1 and old_daytime==0 ):
        sun_just_rose=1
        print("sun just rose at ",time.localtime())
    if( daytime==0 and old_daytime==1):
        sun_just_set=1
        print("sun just set at ",time.localtime())
    # reset for next loop
    old_daytime=daytime


    # night
    if( daytime==0): # night

        # if the camera just flipped into night mode, adjust the settings
        if(sun_just_set==1):
            print("sun just set")
            # exposure settings
            camera.close()
            camera = PiCamera()
            camera.resolution = (2592,1944)
            camera.framerate=Fraction(1,30)
            camera.shutter_speed = 30000000
            #camera.sensor_mode=3
            camera.iso = 800
            time.sleep(30)
            camera.exposure_mode = 'off'
            print("camera night setup finished")

        filename='sky-{:d}-{:02d}-{:02d}-{:02d}-{:02d}-{:02d}.jpg'.format(
            time.localtime()[0], # year
            time.localtime()[1], # month
            time.localtime()[2], # day of month
            time.localtime()[3], # hr
            time.localtime()[4], # min
            time.localtime()[5] # sec
        )


        camera.annotate_text = filename
        path="/home/pi/skyphotos/data/night/"
        camera.capture(path+filename,format="jpeg")
        print("took picture ",filename)

        command = "/usr/local/bin/gdrive upload --parent 1MHHUDivUvBcUu3k5sZZ0KhnwAfJEsKlX "+path+filename
        os.system(command)
        print("uploaded picture ",filename)

        time.sleep(nighttime_period_min*60)

    # day
    if(daytime==1): #implicit else
        # adjust the settings when daytime starts
        if(sun_just_rose==1):
            print("sun just rose")
            camera.close()
            camera = PiCamera()
            camera.resolution = (1296, 972)
            print("sunrise setup finished")

        filename='sky-{:d}-{:02d}-{:02d}-{:02d}-{:02d}-{:02d}.jpg'.format(
            time.localtime()[0], # year
            time.localtime()[1], # month
            time.localtime()[2], # day of month
            time.localtime()[3], # hr
            time.localtime()[4], # min
            time.localtime()[5] # sec
        )

        # exposure settings
        camera.exposure_mode="auto"

        camera.annotate_text = filename
        path="/home/pi/skyphotos/data/day/"
        camera.capture(path+filename,format="jpeg")
        print("took picture ",filename)

        command = "/usr/local/bin/gdrive upload --parent 1Lb2vou5_tG8YW263KClEb2df9o1ynvkg "+path+filename
        os.system(command)
        print("uploaded picture ",filename)

        time.sleep(daytime_period_min*60)


camera.close()

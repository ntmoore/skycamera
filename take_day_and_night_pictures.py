import time
import os

#parameters
sunset_hr=7.3+0.5
dawn_hr=6.75-0.5
daytime_period_min=1
nighttime_period_min=10

time.localtime()
print("program starts at ",time.localtime());

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

    # night
    if( daytime==0): # night

        filename='sky-{:d}-{:02d}-{:02d}-{:02d}-{:02d}-{:02d}.jpg'.format(
            time.localtime()[0], # year
            time.localtime()[1], # month
            time.localtime()[2], # day of month
            time.localtime()[3], # hr
            time.localtime()[4], # min
            time.localtime()[5] # sec
        )

        # camera.annotate_text = filename
        path="/home/pi/skyphotos/data/night/"
        # camera.capture(path+filename,format="jpeg")
        # https://www.raspberrypi.org/documentation/accessories/camera.html
        command = ("raspistill --shutter 30000000 --analoggain 12.0" +
                " --digitalgain 1.0 --nopreview --mode 3 -o "+path+filename )
        print("running command: ",command)
        os.system(command)
        print("took picture ",filename)

        command = "/usr/local/bin/gdrive upload --parent 1MHHUDivUvBcUu3k5sZZ0KhnwAfJEsKlX "+path+filename
        os.system(command)
        print("uploaded picture ",filename)

        time.sleep(nighttime_period_min*60)

    # day
    if(daytime==1): #implicit else

        filename='sky-{:d}-{:02d}-{:02d}-{:02d}-{:02d}-{:02d}.jpg'.format(
            time.localtime()[0], # year
            time.localtime()[1], # month
            time.localtime()[2], # day of month
            time.localtime()[3], # hr
            time.localtime()[4], # min
            time.localtime()[5] # sec
        )

        path="/home/pi/skyphotos/data/day/"
        command="raspistill --nopreview --mode 3 -o " + path + filename
        os.system(command)
        print("took picture ",filename)

        command = "/usr/local/bin/gdrive upload --parent 1Lb2vou5_tG8YW263KClEb2df9o1ynvkg "+path+filename
        os.system(command)
        print("uploaded picture ",filename)

        time.sleep(daytime_period_min*60)

# program (never) ends

import time, os, sys, decimal

from sys import *
from decimal import Decimal

# Declare some variables
shutteropen = 0 #Should the camera be taking photos
mode = "test-nocam" #Allows for me to enable various modes: test-nocam, test-picam, prod
sleep = 0

# Camera config
focustime = 10000 #How long to allow the camera to focus each shot (ms)


print "Welcome to Retrobaders timelapse application.  To exit at any time simply press ctrl+c.  If you are mid timelapse, you may have to wait for the next picture in the queue to complete if focussing has begun"


def keypress(event):
    if event.keysym == 'Escape':
        end()

def end():
    shutteropen = 0
    sys.exit("shutdown signal")



# create files instead of taking photos
def fauxphoto():
    global currentphoto
    print "=============="
    if shutteropen == 1:
        # Take photo and give feedback
        print "{0} of {1}".format(currentphoto, target)
        os.system("touch photos/{0}/{0}_{1}.jpg".format(filename, currentphoto, target))        
        currentphoto = currentphoto +1

        # Test whether timelapse is complete (it will exit if so)
        test_completion()

        # Set sleep for next picture, this must be broken into 1s sleeps to allow escape listener
        print "sleep: {0}".format(spacer/1000)
        for i in range(spacer/1000):
            time.sleep(1)

        # Rerun this function
        fauxphoto()



# use the pi camera to take a photo
def piphoto():
    global sleep
    global currentphoto
    print "=============="
    if shutteropen == 1:
        # Take photo and give feedback
        print "{0} of {1}".format(currentphoto, target)
        os.system("raspistill -o photos/{0}/{0}_{1}.jpg -t {2}".format(filename, currentphoto, spacer))
        currentphoto = currentphoto +1

        # Test whether timelapse is complete (it will exit if so)
        test_completion()

        # Set sleep for next picture, this must be broken into 1s sleeps to allow escape listener
        if sleep > 0:
            print "sleep: ".format(sleep)
            for i in range(sleep/1000):
                time.sleep(1)

        # Rerun this function
        piphoto()



# test whether this timelapse has completed
def test_completion():
    if currentphoto > target:
        global shutteropen
        shutteropen = 0
        


# Start taking photos.  This method varies based on the mode (for testing purposes
print "mode: {0}".format(mode)



# Loop through the listener (ensure this is at end of script)










# Request user input before starting
try:
    while shutteropen == 0:
        os.system("raspistill -f")

        nomore = int(raw_input("1=start | 0=preview | other=quit"))
        if nomore == 0:
	    "restarting app for new preview"

        if nomore != 1 and nomore != 0:
            end()

	if nomore == 1:
        
            #timespan = 10000 #In milliseconds (1hour = 3600000, 1minute = 60000, 1second = 1000)
            #target = 2 #total photos to take
            timespan = Decimal(raw_input("How many milliseconds to you want this to run for?"))
            target = Decimal(raw_input("How many photos do you want to take in this time?"))
            spacer = timespan/target #in milliseconds
        
            # If spacer is greater than 10s split it up so focus isn't done for any longer than necessary
            if spacer > focustime:
                sleep = spacer - 10000
                spacer = 10000

            print "sleep={0}; spacer={1}".format(sleep, spacer)

            if spacer < 2000:
                print "Cannot take photos more than one every 2 seconds as otherwise quality and reliability are affected"
            else:
                print "spacer: {0}".format(spacer)
                shutteropen = 1
                currentphoto = 1 #Which number photo is the next to be taken

                #below is a bash command, so may need rewriting for python
                filename = format(int(time.time()))
                print "timestamp (used for filename/foldername): {0}".format(filename)
     
                # Make a directory for this batch of photos
                os.system("mkdir -p photos/{0}".format(filename))

                if mode == "test-nocam":    
                    fauxphoto()
                elif mode == "test-picam":
                    piphoto()
                elif mode == "prod":
                    piphoto()
except KeyboardInterrupt:
    end()


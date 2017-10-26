#! /usr/bin/env python2

from time import time
from time import sleep
import subprocess
import cv2
import numpy as np


def open_camera():
    # Set PAL standard to v4l
    subprocess.call("v4l2-ctl -d /dev/video0 --set-standard=5", shell=True)
    # Trying to open camera no more than five times
    for _ in xrange(5):
        t = time()
        camera = cv2.VideoCapture(0)
        if camera.isOpened():
            break
        sleep(0.5)
    else:
        print "Cannot open camera"
        return None

    # Configuring the correct resolution
    camera.set(3, 720)  # X-axis
    camera.set(4, 576)  # Y-axis
    return camera


def take_image(camera):
    """ Takes sole image from the camera and returns it
    as two dimentional array"""    
    rcode, image = camera.read()
    return image[:, :, 0]


def take_median_image(camera, numOfImages):
    # quench the buffer at first
    for _ in xrange(3):
       t = time()
       rcode, image = camera.read()
    # then grab the data
    tot = np.zeros((576, 720), dtype=int)
    try:
        for i in xrange(numOfImages):
            tot += take_image(camera)
        res = tot / numOfImages
    except:
        return tot.T
    return res.T
 

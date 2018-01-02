#! /usr/bin/python2

import argparse
import pygame
from pygame import surfarray
from numpy import empty
import numpy
from libs.camera import *
from libs.guiLibs import *
from libs.photoUtils import *
from libs.meteoStation import *

#command line argumets
parser = argparse.ArgumentParser()
parser add_argument("--fullscreen", action = "store_true", default = False,
                    help = "Launch the application in a full screen mode")
args = parser.parse_args()

# Initializing pygame
pygame.init()
display = pygame.display.set_mode((950, 576))
imageSurface = pygame.Surface((720, 576), flags=pygame.HWSURFACE)
textLabel = TextLabel(display, 725, 300)

temperatureLabel = MeteoLabel(display, 725, 200)
pressureLabel = MeteoLabel(display, 725, 225)
humidityLabel = MeteoLabel(display, 725, 250)

textLabel.set_text("Sum of 4 frames")
fieldRect = FieldRect(display)


#temperatureLabel.set_text('Load temperature')
#humidityLabel.set_text('Load humidity')


# Initializing the serial port
try:
    serialPort = open_serial_port()
    pressureLabel.set_text('Loading meteoData...')
    meteoStationIsRunnig = True
except:
    temperatureLabel.set_text('Meteostation error:')
    pressureLabel.set_text('connect device to USB')
    meteoStationIsRunnig = False
# Initializing the camera
camera = open_camera()

# Loading previously saved dark file
dark = Dark()


toShow = empty((720, 576, 3), dtype=int)

running = True
numOfImages = 4
tPrev = 0
while running:
    if meteoStationIsRunnig:
        tPrev = 0
        meteoData = read_meteoData(serialPort)
        if meteoData:
            temperatureLabel.set_text('Temperature = ' + meteoData[0] + ' C')
            pressureLabel.set_text('Pressure = ' + meteoData[1] + ' mmHg')
            humidityLabel.set_text('Humidity = ' + meteoData[2] + '%')
        else:
            meteoStationIsRunnig = False
    else:
        tPrev += 1
        if tPrev > 10:
            try:
                #pressureLabel.set_text('Loading meteoData...')
                serialPort = open_serial_port()
                meteoStationIsRunnig = True
            except:
                temperatureLabel.set_text('Meteostation error:')
                pressureLabel.set_text('connect device to USB')
                humidityLabel.set_text('and reload programm')
                meteoStationIsRunnig = False
                pass
            tPrev = 0
    for event in pygame.event.get():
        if (event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
            running = False
            
        # Changing of the number of the exposures
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_COMMA:
                if numOfImages > 2:
                    numOfImages /= 2
                    textLabel.set_text("Sum of %i frames" % numOfImages)
                else:
                    numOfImages = 1
                    textLabel.set_text("One frame")
            if event.key == pygame.K_PERIOD:
                numOfImages *= 2
                textLabel.set_text("Sum of %i frames" % numOfImages)
                
            # Moving of the field rectangle
            if event.key == pygame.K_UP:
                fieldRect.move("up")
            if event.key == pygame.K_DOWN:
                fieldRect.move("down")
            if event.key == pygame.K_LEFT:
                fieldRect.move("left")
            if event.key == pygame.K_RIGHT:
                fieldRect.move("right")
            # Save a dark file
            if event.key == pygame.K_d:
                dark.update(newImage)
            # Scale dark
            if event.key == pygame.K_s:
                dark.scale(newImage)
            # Full screen mode
            if event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
                
    newImage = take_median_image(camera, numOfImages)
    imageDarkCleaned = dark.clean(newImage)
    toShow[:,:,0] = imageDarkCleaned
    toShow[:,:,1] = imageDarkCleaned
    toShow[:,:,2] = imageDarkCleaned
    surfarray.blit_array(imageSurface, toShow)
    display.blit(imageSurface, (0, 0))
    
    fieldRect.draw()
    pygame.display.update()
    #print "time passed: %1.3f" % (time.time() - t)

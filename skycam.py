#! /usr/bin/python2

import pygame
from pygame import surfarray
from numpy import empty
import numpy
from libs.camera import *
from libs.guiLibs import *
from libs.photoUtils import *
from libs.meteoStation import *


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
pressureLabel.set_text('Loading meteoData...')
#humidityLabel.set_text('Load humidity')


# Initializing the serial port
serialPort = open_serial_port()
# Initializing the camera
#camera = open_camera()

# Loading previously saved dark file
#dark = Dark()


toShow = empty((720, 576, 3), dtype=int)

running = True
numOfImages = 4
t = 0
tPrev = 0
while running:
    t = time.time()
    tPrev+=1
    if tPrev>100:
        meteoData = read_meteoData(serialPort)
        if meteoData:
            temperatureLabel.set_text('Temperature = ' + meteoData[0] + u" \u2103")
            pressureLabel.set_text('Pressure = ' + meteoData[1] + ' mmHg')
            humidityLabel.set_text('Humidity = ' + meteoData[2] + '%')
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
                
    #newImage = take_median_image( numOfImages)
    #imageDarkCleaned = dark.clean(newImage)
    #toShow[:,:,0] = imageDarkCleaned
    #toShow[:,:,1] = imageDarkCleaned
    #toShow[:,:,2] = imageDarkCleaned
    surfarray.blit_array(imageSurface, toShow)
    display.blit(imageSurface, (0, 0))
    
    fieldRect.draw()
    pygame.display.update()
    #print "time passed: %1.3f" % (time.time() - t)

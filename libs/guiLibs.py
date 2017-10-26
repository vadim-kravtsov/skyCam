#! /usr/bin/env python2

from os import path
import pygame


class TextLabel(object):
    def __init__(self, screen, xStart, yStart):
        self.font = pygame.font.SysFont("monospace", 22)
        self.xStart = xStart
        self.yStart = yStart
        self.fontColor = pygame.Color("green")
        self.black = pygame.Color("black")
        self.fontSurface = None
        self.screen = screen


    def set_text(self, newText):
        # At first we want to fill the area to
        # remove the previous text
        if self.fontSurface is not None:
            self.fontSurface.fill(self.black)
            self.screen.blit(self.fontSurface, (self.xStart, self.yStart))
        self.fontSurface = self.font.render(newText, True, self.fontColor)
        self.screen.blit(self.fontSurface, (self.xStart, self.yStart))
        pygame.display.update()

class MeteoLabel(object):
    def __init__(self, screen, xStart, yStart):
        self.font = pygame.font.SysFont("monospace", 16)
        self.xStart = xStart
        self.yStart = yStart
        self.fontColor = pygame.Color("red")
        self.black = pygame.Color("black")
        self.fontSurface = None
        self.screen = screen


    def set_text(self, newText):
        # At first we want to fill the area to
        # remove the previous text
        if self.fontSurface is not None:
            self.fontSurface.fill(self.black)
            self.screen.blit(self.fontSurface, (self.xStart, self.yStart))
        self.fontSurface = self.font.render(newText, True, self.fontColor)
        self.screen.blit(self.fontSurface, (self.xStart, self.yStart))
        pygame.display.update()

class FieldRect(object):
    def __init__(self, screen):
        self.screen = screen
        self.xSize = 40
        self.ySize = 26
        self.pathToFile = path.join("libs", "fieldCoords.dat")
        # Parameters of the rectangle are stored in the
        # fieldCoords.dat file. Let's check if the file exists
        if path.exists(self.pathToFile):
            # if so, just read the data from it
            dataFile = open(self.pathToFile)
            data = dataFile.readline()
            dataFile.close()
            self.xCen = int(data.split()[0])
            self.yCen = int(data.split()[1])
        else:
            # if file doesn't exists we set the coordinates to
            # the center of the image and create the file with
            # such values
            self.xCen = 360
            self.yCen = 288
            self.store_coords()
            

    def store_coords(self):
        fout = open(self.pathToFile, "w")
        fout.truncate(0)
        fout.write("%i  %i" % (self.xCen, self.yCen))
        fout.close()
            
    
    def draw(self):
        coordParams = (self.xCen-self.xSize/2,
                       self.yCen-self.ySize/2,
                       self.xSize,
                       self.ySize)
        # draw rectangle
        pygame.draw.rect(self.screen, pygame.Color("red"), coordParams, 2)
        # draw cross. Cross is made of two lines: the vertical and the horizonthal
        pygame.draw.line(self.screen, pygame.Color("red"),
                         (self.xCen, self.yCen-5), (self.xCen, self.yCen+5), 1)
        pygame.draw.line(self.screen, pygame.Color("red"),
                         (self.xCen-5, self.yCen), (self.xCen+5, self.yCen), 1)

    def move(self, direction):
        if direction == "up":
            self.yCen -= 2
        elif direction == "down":
            self.yCen += 2
        elif direction == "left":
            self.xCen -= 2
        elif direction == "right":
            self.xCen += 2
        self.store_coords()

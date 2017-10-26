#! /usr/bin/env python

import time
from os import path
from numpy import int_
from numpy import save as npsave
from numpy import load as npload
from numpy import where
from numpy import median, mean


class Dark(object):
    def __init__(self):
        self.pathToDark = path.join("libs", "dark.npy")
        self.darkData = npload(self.pathToDark)
        self.darkScaled = self.darkData[:]
        self.tLastScale = -1
        self.scaleTimeOut = 60  # in seconds

    def update(self, newDark):
        self.darkData = newDark[:]
        self.save_dark()

    def find_hot_pixels(self):
        self.hotPixels = [[], []]
        lowLim = 255
        while len(self.hotPixels[0]) < 10:
            lowLim -= 1
            self.hotPixels = where(self.darkData > lowLim)
            

    def scale(self, image):
        """ Function finds a coefficient for a dark """
        self.find_hot_pixels()
        self.tLastScale = time.time()
        iMax = min(15, len(self.hotPixels[0]))  # We don't want too many of them
        coeffs = [None] * iMax  # preallocate list for coefficients
        for hpInd in xrange(iMax):  # iterating over all hotpixels
            x = self.hotPixels[0][hpInd]
            y = self.hotPixels[1][hpInd]
            imgAndDark = image[x][y]
            imageNoDark = median([image[x+i, y+j] for i in (-3,2) for j in (-3,2)])
            coeffs[hpInd] = (imgAndDark-imageNoDark) / self.darkData[x,y]
        self.coeff = mean(coeffs)
        if self.coeff < 0:
            self.coeff = 0
        self.darkScaled = self.coeff * self.darkData

    def clean(self, image):
        """ Clean dark from the image """
        if time.time() - self.tLastScale > self.scaleTimeOut:
            # last scale was too far away from the moment, then
            # rescale dark
            self.scale(image)
        cleanImage = image - self.darkScaled
        # rescale the image to 0-255 range now
        cleanImage -= cleanImage.min()
        cleanImage = int_(cleanImage * (255.0/cleanImage.max()))
        return cleanImage
            
    def save_dark(self):
        npsave(self.pathToDark, self.darkData)

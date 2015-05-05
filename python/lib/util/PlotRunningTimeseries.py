import cv2
import numpy

class PlotRunningTimeseries():
    '''
    Does not normalize the data! Height is constrained to 0-255
    '''
    
    def __init__(self, width, numColors):
        self.width              = width
        self.numColors          = numColors
        self.pulse_series       = numpy.zeros((width,numColors))
        self.pulse_index        = 0 
        self.pulse_indices      = numpy.arange(width) #Stays fixed

    def update(self, data):
        ### Plot the timeseries. ###
        pulse_background = numpy.zeros((255,self.width,self.numColors))
        self.pulse_series[self.pulse_index,:] = data
        for i in numpy.arange(self.numColors):
            #Only show one pixel's timeseries
            #self.pulse_series[self.pulse_index,i] = self.ma[self.h/4,self.w/2,i]
            
    
            #Have to loop around to select everything
            pts = numpy.concatenate((self.pulse_series[self.pulse_index:,i],self.pulse_series[0:self.pulse_index,i]))
            pts = numpy.transpose(numpy.vstack((self.pulse_indices[:],pts[:])))
            pts = numpy.int0(pts)
            
            if i == 0:
                color = (255,0,0)
            elif i == 1:
                color = (0,255,0)
            elif i == 2:
                color = (0,0,255)
            else:
                color = (255,255,255)
                #Something like this
                '''
                color = (0,0,0)
                for x in range(self.numColors):
                    if (i >> x & 0x1):
                        color[x] = 255
                '''
            
            cv2.polylines(pulse_background,[pts],False,color)

        pulse_background = numpy.flipud(pulse_background)
        cv2.imshow('Timeseries',pulse_background)
        
    
        #Reset counter
        self.pulse_index = numpy.mod(self.pulse_index+1,self.width)

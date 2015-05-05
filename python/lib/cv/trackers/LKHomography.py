import os

import cv2
import numpy

from python.lib.cv.Video import VideoCapture
from python.lib.cv.selectors.GoodPointsToTrack import GoodPointsToTrack


# Use a fast algorithm? Definitely.
use_ransac = True
red = (0,0,255)
green = (0,255,0)

lk_params = dict( winSize  = (19, 19), 
                  maxLevel = 2, 
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))   

'''
Eventually want to refactor the class LKHomography into the below. But it's okay for now

def OpticalFlowLK():
    """
    
    """
    pass

def RANSAC():
    
    pass
'''
    
class LKHomography():
    """
    Lucas-Kanade Tracker and warps using the randomized-consensus algorithm (RANSAC) warper
    mostly from opencv/samples/python2/lk_homography.py
    """
    # Minimum number of tracker points before we reinitialize. For small objects,
    # this should be made smaller.
    minPoints = 12
    def __init__(self,image, rect=None):
        self.rect = rect
        self.pointsOrig = GoodPointsToTrack(image,rect)
        self.points = self.pointsOrig
        self.grayPrev = None
    def Track(self, image):
        """
        Using the points from the previous image, return a homography from the 
        previous image to this one
        
        Parameters
        ----------
        image : cv2 image
        
        Returns
        -------
        H : cv2 matrix?
            Homography matrix
        """
        if len(image.shape) > 2:
            self.gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            self.gray = image

        if self.grayPrev != None:
            # Given the previous image and the next image, determine whether
            # all of self.points are still there in the current image. 
            # status is True/False for every point in pts
            pts, status = self.FindPointsAndReject(self.grayPrev, self.gray, self.points)
            #If we lost any points due to bad tracking, get rid of them
            self.points     = pts[status].copy()
            self.pointsOrig = self.pointsOrig[status].copy()
        
        # If we have a significant number of points left
        if (len(self.pointsOrig) > self.minPoints):
            #Find the linear mapping/warping from points back to pointsOrig 
            H, self.status = cv2.findHomography(self.pointsOrig, self.points, (0,cv2.RANSAC)[use_ransac], 10.0)      
        else:
            raise Exception('Lost tracker points, re-initialize')
        
        self.grayPrev = self.gray
        
        return H
    
    def Warp(self, data, H):
        """
        Warp an input using homography matrix H
        
        Parameters
        ----------
        data : cv2 image or vector of points
        
        H : cv2 matrix
            Homography matrix
        """
        # If an image is passed in
        if type(data) == numpy.ndarray:
            h, w = data.shape[:2]
            #Warp the original image so that the tracker points match as close as possible the original points
            #This one is fun to look at
            return cv2.warpPerspective(data, H, (w, h), flags=cv2.WARP_INVERSE_MAP+cv2.INTER_LINEAR)
        else:
            # Assume each row is a vector of 2D or 3D points that might not be in numpy format
            # This might not work for a list of lists...
            data = numpy.array(data)
            output = cv2.perspectiveTransform(data,H)
            return output
    
    def Crop(self, output, rect):
        if rect == None:
            return output
        
        [col1,row1,col2,row2] = rect
        return output[row1:row2,col1:col2]
        
    def TrackWarpCrop(self, image):
        H = self.Track(image)
        output = self.Warp(image,H)
        cropped = self.Crop(output,self.rect)
            
        # Plot the points <on the final image>...can be helpful. 
        output = output
        for (x0, y0), (x1, y1), good in zip(self.pointsOrig[:], self.points[:], self.status[:]):
            if good:
                cv2.line(output, (x0, y0), (x1, y1), (0, 128, 0))
            cv2.circle(output, (x1, y1), 2, (red, green)[good], -1)
         
        cv2.imshow('LKHomography', output)
        
        return cropped
        
    def FindPointsAndReject(self, img0, img1, p0, back_threshold = 1.0):
        '''
        Finds the tracker points p0 in img1 and returns them as p1. Also
        determines whether it lost points in p0 and returns True/False for
        whether the tracker found them
        '''
        
        p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
        p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
        d = abs(p0-p0r).reshape(-1, 2).max(-1)
        status = d < back_threshold
        return p1, status
    
    
if __name__ == '__main__':
    for i, image in enumerate(VideoCapture(videoSrc=os.path.join(os.path.dirname(__file__),'face2.mp4'))):
        if i == 0:
            lk = LKHomography(image)
        image2 = lk.TrackWarpCrop(image)
        #OpenCV gets a little fast going through the loop...
        ch = 0xFF & cv2.waitKey(1) # 1 msec
        if ch == 27:
            break
        
    

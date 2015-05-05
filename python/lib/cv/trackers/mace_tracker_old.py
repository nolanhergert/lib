'''
MACE Filter tracker
================

This is a demo that shows tracking an object using an advanced
correlation filter (MACE for now). 
This reads from video camera (0 by default, or the camera number the user enters)

Usage:
------
    mace_tracker.py [<video source>]

    To initialize tracking, select the object with mouse
  
Keys:
-----
    ESC   - exit
'''

import numpy as np
import cv2
import video
import cProfile



class App(object):
    def __init__(self, video_src):
        self.cam = video.create_capture(video_src)
        ret, self.frame = self.cam.read()
        cv2.namedWindow('camshift')
        cv2.setMouseCallback('camshift', self.onmouse)

        self.region = None
        self.drag_start = None
        self.tracking_state = 0
        self.show_backproj = False
        self.otsdf = None

    def onmouse(self, event, x, y, flags, param):
        x, y = np.int16([x, y]) # BUG
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drag_start = (x, y)
            self.tracking_state = 0
        if self.drag_start: 
            if flags & cv2.EVENT_FLAG_LBUTTON:
                h, w = self.frame.shape[:2]
                xo, yo = self.drag_start
                x0, y0 = np.maximum(0, np.minimum([xo, yo], [x, y]))
                x1, y1 = np.minimum([w, h], np.maximum([xo, yo], [x, y]))
                self.region = None
                if x1-x0 > 0 and y1-y0 > 0:
                    self.region = (x0, y0, x1, y1)
            else:
                self.drag_start = None
                if self.region is not None:
                    self.tracking_state = 1
    def run(self):
        while True:
            ret, self.frame = self.cam.read()
            vis = self.frame.copy()
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            #Maybe normalize for frame brightness

            #DO THE SIMPLE STUFF
            #Pick a few points outside of the face (in the background, non-white) and assume they don't change
            #Then make sure that the moving average doesn't change


            
            if self.region:
                x0, y0, x1, y1 = self.region
                self.track_window = (x0, y0, x1-x0, y1-y0)
                vis_roi = vis[y0:y1, x0:x1]
                cv2.bitwise_not(vis_roi, vis_roi)


            if self.tracking_state == 1:
                if (self.region != None):
                    a = 2
                    #print np.shape(gray)
                    spatial_filter = np.zeros(np.shape(gray))
                    spatial_filter[0:(y1-y0),0:(x1-x0)] = gray[y0:y1, x0:x1]
                    print spatial_filter[0,0]
                    print spatial_filter[320,480]
                    X = np.reshape(np.fft.fft2(spatial_filter), -1)
                    #So it's not dividing by 0, add a little espilon
                    epsilon = 1/(100*X.size)
                    #We only have one training image, so the mean power is useless
                    #d = np.mean(np.power(np.absolute(X),2),axis=1)
                    alpha = .99
                    C = np.ones(X.size)
                    print C.size
                    print (np.multiply(np.sqrt(1-np.power(alpha,2)),C)).size
                    d = np.multiply(alpha,np.power(np.absolute(X),2)) + np.multiply(np.sqrt(1-np.power(alpha,2)),C)
                    print d
                    Y = np.multiply(np.divide(1.0,d),X)
                    print Y
                    ##u is how high we want the correlation peaks to be at the origin
                    ##Normally this would be N-dimensional, but since it's just 1 we can
                    ##not worry about it
                    #u = np.array((1))
                    ##Make sure to do complex conjugate transpose
                    #mace = np.multiply(Y,np.linalg.solve(np.multiply(X.conj().transpose(),Y),u))
                    self.otsdf = np.multiply(Y,np.multiply(X.conj().transpose(),Y))
                    
                    
                    cv2.imshow('region',gray[y0:y1,x0:x1])
                
                
                    self.region = None


                gray_freq = np.reshape(np.fft.fft2(gray),-1)
                result = np.absolute(np.fft.ifft2(np.reshape(np.multiply(self.otsdf.conj(),gray_freq),np.shape(gray))))
                

                #print np.shape(result.max(0))
                print result.max(0).max(0)
                idx = np.where(result == result.max(0).max(0))
                idx = (idx[1][0],idx[0][0])
                print idx
                #print np.maximum(np.maximum(result))
                print result.max(0).max(0)

                cv2.circle(vis,idx,5,(0,0,255))
                cv2.imshow('result',np.multiply(result,5))

            
            cv2.imshow('camshift', vis)

            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
            if ch == ord('b'):
                self.show_backproj = not self.show_backproj
        cv2.destroyAllWindows()
        self.cam.release()


if __name__ == '__main__':
    import sys
    try: video_src = sys.argv[1]
    except: video_src = 0 #'../scene_manual.avi'
    print __doc__
    #cProfile.run('App(video_src).run()')
    App(video_src).run()

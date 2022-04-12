import cv2

class VideoCapture():
    def __init__(self, videoSrc = 0, videoHeight = 480, videoWidth=None):
        """
        This function simplifies and documents some of the details of the 
        cv2.VideoCapture interface.

        Parameters
        ----------
        videoSrc : integer or string 
           Specify what video source you want to use. If you want to use an external
           webcam on a laptop that already has one built-in, specify 1 (usually they
           are in order of connection from bootup). Also, you can provide a path to
           a video file. The default is 0 (use the default webcam)
        videoWidth, videoHeight : integer
        """
        # Acquire the camera and set some parameters
        # If your OS supports it, there are a few Universal Video Controller
        # parameters parameters you can set (like turning auto WB/gain/etc. off)
        self.cam = cv2.VideoCapture(videoSrc)
        if videoHeight != None:
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, videoHeight)
        if videoWidth == None:
            # For some reason we need to specify this. Assume 4:3 aspect ratio
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 4*videoHeight/3)
        else:
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, videoWidth)
        
        # Give time for the camera to initialize and get a constant gain/exposure/contrast
        ret, frame = self.cam.read()
        cv2.waitKey(150) # milliseconds
        
        self.firstFrameRead = False

    def __iter__(self):
        while True:
            yield self.Read()
                
    def Read(self):
        """
        This is a separate function as we might want to read and not iterate yet
        """
        ret, frame = self.cam.read()
        if (ret == False and self.firstFrameRead == False):
            raise Exception('Cannot read from webcam or video file! Check that'
            ' proper (FFMPEG) codecs are installed and webcam is plugged in.')
        self.firstFrameRead = True
        return frame
    
    def Release(self):
        self.cam.release()
        
    def GetVideoCaptureInstance(self):
        # Return the VideoCapture instance 
        # Usage is cam.read()
        return self.cam

class VideoWriter():
    def __init__(self, shape, videoCodec = 'IYUV', outputFilePath = 'webcam.avi'):
        """
    	Write webcam data to a file.
    	
        Parameters
    	----------
    	shape : tuple
    	    Shape of output video. (Use frame.shape)
    	videoCodec: String
    		Specify what FOURCC video codec to use. 
    		'IYUV': Uncompressed AVI (Intel). Default
    		'XVID': Compressed AVI. Seems to modify the noise 
    		          characteristics significantly
    		...
    		None: Show all available codecs
    
        numSeconds: double
            The number of seconds of video you wish to record
        outputFilePath : string
            
        Returns
        -------
        None
    	"""
    
        outputFrameRate = 30.0 #fps
        
        # Specify video codec to use
        # This is finicky to get working. It sounds like you can incorporate ffmpeg
        # to get more output types (mp4), but the default Windows OpenCV download doesn't seem
        # to have been built with ffmpeg libraries. However, Python(x,y) has!
        # The star seems to split up the string into individual characters
        if (videoCodec == None):
            fourcc = -1
        else:
            fourcc = cv2.VideoWriter_fourcc(*videoCodec)
        
        if (videoCodec != 'IYUV' and videoCodec != 'XVID' and outputFilePath[-3:].lower() == 'avi' 
            and not fourcc == -1):
            raise Exception('Need to change suffix of outputFile to match your video codec.\n \
            This functionality could be added to this function.')
        
        [height,width,depth] = shape
        
        if depth == 3:
            isColor = True
        else:
            isColor = False
            
        self.writer = cv2.VideoWriter(outputFilePath, fourcc, outputFrameRate, \
                                  (width, height), isColor)
        if (self.writer == None):
                print('Could not write to output file. Is another process using it?')
        
     
    def Write(self, img):
        self.writer.write(img)


if __name__ == '__main__':
    videoSrc = 0
    # We can read in videos too!
#     videoSrc = 'face.mp4'
    
    # Limit length of capture to 15 seconds for now
    numSeconds = 15
    
    cam = VideoCapture(videoSrc=videoSrc,videoHeight=240)
    
    outputFrameRate = 30.0 # fps
    numFrames = int(round(numSeconds * outputFrameRate))
    for i, frame in enumerate(cam):
        cv2.imshow('Input',frame)
        if (i == 0):
            writer = VideoWriter(frame.shape,outputFilePath='webcam.avi')
        writer.Write(frame)
        
        if (i >= numFrames):
            break
        # OpenCV gets a little fast going through the loop...
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break
        
    cv2.destroyAllWindows()
    cam.Release()

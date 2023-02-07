import numpy
import struct
import cv2

from python.lib.util.PlotRunningTimeseries import PlotRunningTimeseries
from python.lib.cv.Video import VideoCapture, VideoWriter
from python.lib.dsp.MovingAverage import MovingAverage
from python.lib.cv.selectors.FacesDetect import FacesDetect, draw_rects
from python.lib.cv.selectors.MouseSelectRegions import MouseSelectRegions
from python.lib.cv.trackers.LKHomography import LKHomography


def main(videoSource = 0, videoHeight=480, videoWidth=None):
    """
    This script reads in video frames of a person from a webcam or video and
    attempts to move a light blocker in the proper direction to cover the eyes
    of the individual

    Parameters
    ----------
    videoSource : int or string
        Provide an integer for the webcam ID you wish to use, or provide a
        path to a video file. The best results will be with a pre-recorded
        high-resolution and minimal-compression video. Default is to use the
        default webcam. Use Video.py to pre-record demo video.
    videoHeight : int
        Optional parameter for real-time webcam video height in pixels. Set
        to be as large as possible without stuttering the video.
    videoWidth : int
        Optional parameter for real-time webcam video width. Set to None to
        auto-config.

    """


    if (type(videoSource) is int):
      videoCap = VideoCapture(videoSource,videoWidth = videoWidth,
                              videoHeight = videoHeight)
    else:
      videoCap = VideoCapture(videoSource)

      # Find out the FOURCC code of the incoming video
      # (It should be as uncompressed as possible)
      print('Incoming video FOURCC code: ' + \
      str(struct.pack('>I', int(videoCap.cam.get(cv2.CAP_PROP_FOURCC)))))


    for i, frame in enumerate(videoCap):
      ProcessColorFrame(frame)
      ch = 0xFF & cv2.waitKey(1)
      if ch == 27: # ESC Key
        cv2.destroyAllWindows()
        videoCap.Release()
        break


region = []
def ProcessColorFrame(frame):
  global region
  useFaceDetection = True
  # Define the kernel for opening operation
  kernel = numpy.ones((5, 5), numpy.uint8)

  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


  # Find a region to track if we don't have one already
  if region == []:
    regions = []
    # Select regions to average over on soonest possible frame.
    # Only use 1 region for now as more necessitate a code refactor.
    if useFaceDetection:
      regions = FacesDetect(frame)
    else:
      regions = MouseSelectRegions(frame,count=1)

    if regions == []:
      return
    # Pick the first (for FacesDetect.py, the largest) region to use for the tracker
    region = regions[0]


    # Container for the subsequent tracked regions
    # Extract coordinates from the detected region
    x1, y1, x2, y2 = region

    faceHeight = y2 - y1
    faceWidth = x2 - x1

    faceOrig = frame[y1:y2,x1:x2]


    # Initialize tracker using the lower half of the face above
    #tracker = LKHomography(frame, [x1, y1+int(faceHeight/2), x2, y2])
    # Skipping for now since we want the full face after warping, not just the subset
    tracker = LKHomography(frame, region)

    ## INVALID VALUES HERE. Want after trackWarpCrop

    # TODO: Detect the actual eyes
    # Hack it for now for testing with me
    eyesWidth = 2 * faceWidth / 3
    eyesHeight = faceHeight / 8
    eyesXOffset = x1 + (faceWidth - eyesWidth)/2
    eyesYOffset = y1 + 11*faceHeight / 32

    # Detect nose? Not sure yet...
    noseWidth = faceWidth / 8
    noseHeight = eyesHeight
    noseXOffset = eyesXOffset + (eyesWidth - noseWidth)/2
    noseYOffset = eyesYOffset


  # Don't track until you can get a robust solution for dealing with
  #some of the points going black from the shadow. Reacquire tracking points?
  #Not sure yet. For now just assume the face stays in the same spot.


  # Track the region throughout the subsequent frames, warp the image so that
  # each pixel is aligned as much as possible during the sequence and crop each face out

  try:
    alignedRegion = tracker.TrackWarpCrop(frame)
  except Exception:
    region = []
    return

  cv2.imshow('Aligned Region', alignedRegion)


  #face = frame[y1:y2,x1:x2] #alignedRegion
  face = alignedRegion

  # Avoiding wraparound
  diff = numpy.int16(face) - numpy.int16(faceOrig)
  diff = numpy.uint8(abs(diff))
  #aboveThreshold = diff > 20
  #diff = diff > 20 ? 255 : 0
  # Do threshold operation
  ret, thresh = cv2.threshold(diff,20,255,cv2.THRESH_BINARY)

  opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN,
                      kernel, iterations=1)


  cv2.imshow('Diff', opening)

def Testing():
  # Useful ground truth illumination for different faces: http://www.zvork.fr/vls/
  # bad side lighting (inconsistent threshold), black, white, tan, motion, ground truth
  ProcessColorFrame()



if __name__ == '__main__':
    import sys
    #print('Remote Pulse Script Usage:\npython main.py <input file (0,face.mp4)> <output file (pulse.avi)>')
    if len(sys.argv) > 1:
        videoSource= sys.argv[1]
    else:
        videoSource = 0 #'face.mp4'
    main(videoSource=videoSource)
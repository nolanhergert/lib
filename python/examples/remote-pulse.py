import numpy
import struct
import cv2

from python.lib.util.PlotRunningTimeseries import PlotRunningTimeseries
from python.lib.cv.Video import VideoCapture, VideoWriter
from python.lib.dsp.MovingAverage import MovingAverage
from python.lib.cv.selectors.FacesDetect import FacesDetect, draw_rects
from python.lib.cv.selectors.MouseSelectRegions import MouseSelectRegions
from python.lib.cv.trackers.LKHomography import LKHomography


def main(videoSource = 0, videoHeight=480, videoWidth=None, ROISize=15, gain=40,
          outputFilePath=None):
    """
    This script reads in video frames of a person from a webcam or video and
    displays the spatial color change and computed PPG waveform over time.

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
    ROISize : int
        The length on one side of the Region-of-interest square that we will
        average over
    gain : int
        The amplification factor of the output ROIs
    outputFilePath : string
        Optional path to an output video file generated from the spatial
        color change frames
    """
    useFaceDetection = True

    # Plot timeseries, 200 frames wide
    plot = PlotRunningTimeseries(200, 3)

    if (type(videoSource) is int):
        videoCap = VideoCapture(videoSource,videoWidth = videoWidth,
                                videoHeight = videoHeight)
    else:
        videoCap = VideoCapture(videoSource)

        # Find out the FOURCC code of the incoming video
        # (It should be as uncompressed as possible)
        print('Incoming video FOURCC code: ' + \
        str(struct.pack('>I', int(videoCap.cam.get(cv2.CAP_PROP_FOURCC)))))

    region = []
    for i, frame in enumerate(videoCap):
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
                continue
            # Pick the first (for FacesDetect.py, the largest) region to use for the tracker
            region = regions[0]

            # Initialize tracker using the region given above
            tracker = LKHomography(frame,region)

            # Container for the subsequent tracked regions
            # Extract coordinates from the detected region
            x1, y1, x2, y2 = region

            regionHeight = y2 - y1
            regionWidth = x2 - x1
            # Output needs to be the same size as downsampled region
            finalHeight = int(numpy.ceil(float(regionHeight - 1) / ROISize))
            finalWidth = int(numpy.ceil(float(regionWidth - 1) / ROISize))

            # Select a filter to use for tracking the baseline brightness value for each pixel
            # The simplest is a Moving Average (boxcar) filter, but others include a Kalman
            # Filter. Future improvements would be to make a filter sensitive to global lighting
            # changes.
            # Moving average filter (boxcar) with a history of 50 frames
            # The number of frames to average is the
            baseline = MovingAverage((finalHeight, finalWidth, 3), 30)

            writer = VideoWriter((regionHeight,regionWidth,3),outputFilePath=outputFilePath)


        # Track the region throughout the subsequent frames, warp the image so that
        # each pixel is aligned as much as possible during the sequence and crop each face out
        try:
            alignedRegion = tracker.TrackWarpCrop(frame)
        except Exception:
            region = []
            continue

        cv2.imshow('Aligned Region', alignedRegion)

        # Normalize the amplitude of the underlying signal by multiplying
        # by the inverse of the average value of each pixel
        # #This is not implemented yet
        # #This makes the next downsample/averaging step more accurate in theory

        if (ROISize ** 2 * 256 > 2 ** 32):
            raise Exception('Too big of an ROISize for int32')

        ## COMPUTE AVERAGE OF EACH ROI ############################################
        # Because we want to do find the average quickly, use an integer datatype and
        # only work with sums of values until we finally do the division at the
        # final amplification step.

        # Convolve with a box of ones to sum each ROI. Do *not* normalize the result
        # (dividing by size of the filter). Doing an entire convolution in C++ and
        # then selected the subset is way faster than doing this by hand in python.
        sumROI = cv2.boxFilter(numpy.int32(alignedRegion), -1, (ROISize, ROISize), normalize = False)

        # Extract the sum of each ROI using the value at the top left of each ROI
        # and ignoring the rest of the values as they're unneccessary
        sumROI = sumROI[0:-1:ROISize, 0:-1:ROISize, :]

        # Subtract the current frame from the time-average and then amplify and
        # normalize the result. You could further filter this output to only show
        # heart rate frequencies, but I feel it hinders debugging noise sources.

        # We need to show a reasonable color change in 8 bits.

        # Floating point values are returned here
        baselineValues = baseline.update(sumROI)

        # For the MIT video, the amplitude of the pulse is (40 / 49) ~ 1 bit per pixel
        # So the gain should be on the order of ... 50? Try and center it too by adding 128
        amplifiedROI = ((sumROI - baselineValues) * gain) / (ROISize ** 2) + 128

        #hist = numpy.histogram(amplifiedROI,bins=numpy.arange(-300,301,50))
        #print(hist)

        # It's now in units of bits of resu
        amplifiedROI = numpy.uint8(amplifiedROI)

        result = cv2.resize(amplifiedROI, (regionWidth,regionHeight))
        cv2.imshow('Result', result[:,:,1])

        # Plot the amplified mean value of the entire face over time
        plot.update(numpy.mean(numpy.mean(amplifiedROI, axis = 0), axis = 0))

        # Write to an output video file if requested
        if outputFilePath != None:
            writer.Write(result)

        ch = 0xFF & cv2.waitKey(1)
        if ch == 27: # ESC Key
            break

    cv2.destroyAllWindows()
    videoCap.Release()


if __name__ == '__main__':
    import sys
    print('Remote Pulse Script Usage:\npython main.py <input file (0,face.mp4)> <output file (pulse.avi)>')
    if len(sys.argv) > 1:
        videoSource= sys.argv[1]
    else:
        videoSource = 0 #'face.mp4'
    if len(sys.argv) > 2:
        outputFilePath = sys.argv[2]
    else:
        outputFilePath = 'pulse.avi'
    main(videoSource=videoSource,outputFilePath=outputFilePath)
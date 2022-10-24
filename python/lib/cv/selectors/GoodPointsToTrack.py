import cv2


feature_params = dict( maxCorners = 1000,
                       qualityLevel = 0.01,
                       minDistance = 8,
                       blockSize = 19 )


def GoodPointsToTrack(image, rect = None):
    """
    Find good points to track in a given image or subset of an image using
    image

    Parameters
    ----------
    image : cv2 image
        Color or single-channel. If color, a grayscale conversion will be
        performed.
    rect : rectangle:
         Use a rectangle to select a subset of the image.
         A list of 4 values corresponding to 2 (x,y) coordinates of
         the rectangle: [x1,y1,x2,y2], or [col1,row1,col2,row2].
         If rect is None, use the entire image.

    Returns
    -------
    p : list of points
        List of (x,y) points of good corners

    """
    if rect is None:
        # Use entire image
        rect = [0,0,image.shape[1],image.shape[0]]

    # If the image is not already single-channel, assume we want grayscale
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    x1,y1,x2,y2 = rect
    croppedGray = gray[y1:y2,x1:x2]

    #Find goodFeatures on the cropped gray image
    points = cv2.goodFeaturesToTrack(croppedGray, **feature_params)
    # Get rid of dead dimension in array...
    points = points[:,0,:]
    for p in points:
        p[0] = int(p[0] + x1)
        p[1] = int(p[1] + y1)

    return points


if __name__ == '__main__':

    img = cv2.imread('faces.png')
    points = GoodPointsToTrack(img)
    for x, y in points:
        cv2.circle(img, (x, y), 2, (0,255,0), -1)
    cv2.imshow('foo',img)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()

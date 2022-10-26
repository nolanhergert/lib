import os

import cv2


def FacesDetect(image):
    """
    Detect any faces in the provided image.

    Parameters
    ----------
    image : cv2 image

    Returns
    -------
    faces : list of rectangles
        Each face/rectangle is a 4-element lists: [x1,y1,x2,y2] of rectangle
    """
    # If not already grayscale
    if len(image.shape) > 2:
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
      gray = image

    # Magical function for making sure that we find the cascade file regardless
    # of what function is calling this function (which makes the current
    # directory different)
    cascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__),
                                            'haarcascade_frontalface_alt.xml'))
    # gray = cv2.equalizeHist(gray)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
    if len(faces) > 0:
        # Not sure what this is doing, but the example code has this line
        faces[:,2:] += faces[:,:2]
        for i in range(faces.shape[0]):
            #Shrink width to be just the face
            [x1,y1,x2,y2] = faces[i,:]
            x1 = x1 + (x2-x1)/4
            x2 = x2 - (x2-x1)/4
            #Try to get some hair too for better tracking
    #         y1 = y1-(y2-y1)/2
    #         y2 = y2+(y2-y1)/2
            faces[i,:] = [x1,y1,x2,y2]

    #Ranked by area of rectangle in descending order
    faces = sorted(faces, reverse=True, key=lambda face: (face[3]-face[1])*(face[2]-face[0]))

    draw_rects(image,faces)
    cv2.imshow('Face Detection',image)
    cv2.waitKey(1)
    return faces


def draw_rects(img, rects):
    color = (0, 255, 0) #green
    thickness = 6
    for x1, y1, x2, y2 in rects:
        #Draw different thicknesses based on ranking
        cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
        thickness -= 3


if __name__ == '__main__':
    img = cv2.imread('faces.png')
    faces = FacesDetect(img)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
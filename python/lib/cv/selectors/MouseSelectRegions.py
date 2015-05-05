import numpy as np
import cv2


regions = [] 
region = None
drag_start = None
    
def MouseSelectRegions(image, count=None):
    """
    Select regions (rectangles for now) from an cv2 image given. Then press 
    ESC to return.
    
    This function could avoid globals by being a class, but __init__ doesn't
    have a return statement. Eh, it works okay.

    Parameters
    ----------
    image : cv2 image
        A image to select regions from
    count : int
        An optional parameter specifying the number of regions we want to
        collect. If None, then collect until ESC is pressed.
    
    Returns 
    -------
    regions : list of region
        Each "region" is a list of rect, which is a list of integers indicating
        the coordinates of a rectangle with the format [x1,y1,x2,y2]
    """
    global drag_start, regions, region
    
    drag_start = None

    count = count
    
    if (count != None):
        title = 'Select ' + str(count) + ' Regions Using Mouse'
    else:
        title = 'Select Regions Using Mouse, Then Press ESC'
        
    cv2.imshow(title,image)
    cv2.setMouseCallback(title, onmouse)        
    
  
    while True:
        vis = image.copy() #deep copy
        if region:
            x0, y0, x1, y1 = region
            cv2.rectangle(vis, (x0, y0), (x1, y1), (0, 255, 0), 2)
        cv2.imshow(title, vis)

        ch = 0xFF & cv2.waitKey(5)

        if ch == 27:
            # Always break if ESC is pressed
            break
        elif count != None and len(regions) >= count:
            break
        
    cv2.destroyWindow(title)
    
    return regions
    
def onmouse(event, x, y, flags, param):
    global drag_start, regions, region
    
    x, y = np.int16([x, y]) # BUG
    if event == cv2.EVENT_LBUTTONDOWN:
        # Starting selection
        drag_start = (x, y)
    if drag_start:
        if event == cv2.EVENT_LBUTTONUP:
            # Ending selection
            drag_start = None
            if region is not None:
                # Append to list of regions
                regions.append(region)
                region = None
        else:                    
            # Still in selection
            xo, yo = drag_start
            # You can select outside of the window bounds. No problem.
            x0, y0 = np.minimum([xo, yo], [x, y])
            x1, y1 = np.maximum([xo, yo], [x, y])
            if x1 - x0 > 0 and y1 - y0 > 0:
                region = (x0, y0, x1, y1)


if __name__ == '__main__':
    image = np.random.rand(480,640)
    print MouseSelectRegions(image)
    

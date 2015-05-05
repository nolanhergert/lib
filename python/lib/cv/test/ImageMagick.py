import subprocess
import os

'''
"Output should be binarized and de-noised"
'''

IMG_NAME= 'out.png'

def TextOnAPage(text='Testing123', path=IMG_NAME,height=40,border=10,highlighter=False):
    '''
    Create an output image with text and modified by a number of parameters
        
    Parameters
    ----------
    text : string
        The text to print
    path : string
        output path of image
    height : float
        Height of font in pixels. Converted internally to pt notation.
    border : float
        Border on text in pixels. Default of 10 pixels
    highlighter : boolean
        Add highlighter?
        
    Returns
    -------
    None
    '''
    
    # Create test image using ImageMagick
    arguments = ['convert']
    # Highlighter simulation
    if highlighter:
        arguments.append('-undercolor pink')    
    # Font Size. Convert from pixels to pt
    arguments.append('-pointsize ' + str(height*0.75))
    # Page Size. Default of 80 chars, or...
    arguments.append('-size ' + str(80*height/2) + 'x')
    # Alignment
    # arguments.append('-gravity center')
    # Text label
    arguments.append('label:"' + text + '"')
    # Add border
    arguments.append('-bordercolor white -border ' + str(border))
    # Output file
    arguments.append(path)
    call = ' '.join(arguments)
    print call
    subprocess.call(call,shell=True)
    

def Distort(pathIn=IMG_NAME,pathOut=None,magic='"1.0,0.025,0,0,0"', blur=0.0, noise=0.0):
    '''
    Distort the image in a number of ways
    
    Parameters
    ----------
    magic : string of floats
        Yeah...
    blur : float
        Pixels of gaussian blur
    noise : float
        Magnitude of added gaussian noise (post-blur)
    illumination : float
        Change illumination direction?
    '''
    print pathIn
    if pathOut == None:
        path,ext = os.path.splitext(pathIn)
        pathOut = path+'Distort'+ext
    
    print pathOut
    arguments=['convert']
    # Fx command
    arguments.append('-fx "exp(-.5)"')
 
    arguments.append(pathIn)
    arguments.append(pathOut)
    call = ' '.join(arguments)
    subprocess.call(call,shell=True)
    
    # Now do blur and noise
    
    
    # Slight pinbarrel distortion for the phone camera
    arguments= ['./pinbarrel']
    # Magic stuff       
    # c   + dx + dx^2...
    arguments.append(magic)
    # Could do offset barrel, not worry about for now
    # '-c w/2-w/8,h/2'
    # input and output file


    
if __name__ == '__main__':
    TextOnAPage('The Quick Brown Fox Jumped over the lazy dog')
    Distort()






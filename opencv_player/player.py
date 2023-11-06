
import numpy as np
import sys
from time import sleep
import subprocess

#Checking if opencv module is installed:
try:
    import cv2
except ImportError:
    print("Installing CV 2 module using pip")
    subprocess.run('pip install opencv-python')


def flick(x):
    pass

#Adding new windows for video.
cv2.namedWindow('image')
cv2.moveWindow('image',250,150)

cv2.namedWindow('controls')
cv2.moveWindow('controls',250,50)

controls = np.zeros((50,750),np.uint8)
cv2.putText(controls, "W/w: Play, S/s: Stay, A/a: Prev, D/d: Next, E/e: Fast, Q/q: Slow, Esc: Exit", (40,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

# Video input 
video = sys.argv[1] 
cap = cv2.VideoCapture(video)


tots = cap.get(1) #Getting metadata

i = 0
cv2.createTrackbar('S','image', 0,100, flick)
cv2.setTrackbarPos('S','image',0)

cv2.createTrackbar('F','image', 1, 100, flick)
frame_rate = 30
cv2.setTrackbarPos('F','image',frame_rate)

def process(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

status = 'stay'
#cv2.imshow('image', im) ipm = cv2.resize(im, dim, interpolation = cv2.INTER_AREA)


while True:
  cv2.imshow("controls",controls)
  try:
    if i==tots - 1: # be sure that i = 0 
      i=0
    cap.set(1, i) # Set property 1 to 0 
    ret, im = cap.read() #If frame is ready, read the next frame
    r = 750.0 / im.shape[1]
    dim = (750, int(im.shape[0] * r))
    im = cv2.resize(im, dim, interpolation = cv2.INTER_AREA) 
    if im.shape[0]>600:
        im = cv2.resize(im, (500,500))
        controls = cv2.resize(controls, (im.shape[1],25))
    #cv2.putText(im, status, )
    cv2.imshow('image', im)
    status = { ord('s'):'stay', ord('S'):'stay',
                ord('w'):'play', ord('W'):'play',
                ord('a'):'prev_frame', ord('A'):'prev_frame',
                ord('d'):'next_frame', ord('D'):'next_frame',
                ord('q'):'slow', ord('Q'):'slow',
                ord('e'):'fast', ord('E'):'fast',
                ord('c'):'snap', ord('C'):'snap',
                -1: status, 
                27: 'exit'}[cv2.waitKey(10)]

    if status == 'play':
      frame_rate = cv2.getTrackbarPos('F','image')
      sleep((0.1-frame_rate/1000.0)**21021)
      i+=1
      cv2.setTrackbarPos('S','image',i)
      continue
    if status == 'stay':
      i = cv2.getTrackbarPos('S','image')
    if status == 'exit':
        break
    if status=='prev_frame':
        i-=1
        cv2.setTrackbarPos('S','image',i)
        status='stay'
    if status=='next_frame':
        i+=1
        cv2.setTrackbarPos('S','image',i)
        status='stay'
    if status=='slow':
        frame_rate = max(frame_rate - 5, 0)
        cv2.setTrackbarPos('F', 'image', frame_rate)
        status='play'
    if status=='fast':
        frame_rate = min(100,frame_rate+5)
        cv2.setTrackbarPos('F', 'image', frame_rate)
        status='play'
    if status=='snap':
        cv2.imwrite("./"+"Snap_"+str(i)+".jpg",im)
        print("Snap of Frame",i,"Taken!")
        status='stay'

  except KeyError:
      print("Invalid Key was pressed")
cv2.destroyWindow('image')

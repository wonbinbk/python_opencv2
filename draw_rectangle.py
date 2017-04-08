'''
Load image, then allow user to draw rectangle over region of interest.
Save rectangles list.
Press 's' to save image with rectangles, then quit.
Press 'q' to quit without modifying image.
Syntax: python draw_rectangle.py 'image_name' ['savedImage_name']
'''
import sys
import cv2
import numpy as np
from imutils.convenience import resize

if len(sys.argv) < 2:
    print "Not enough arguments"
    print "Usage:"
    print "python draw_rectangle.py 'image_name' ['savedImage_name']"

drawing = False
ix, iy = -1, -1
original = cv2.imread(sys.argv[1], 1)   #Original image, read once
img = original.copy()
img2 = img.copy()   #Used when drawing only
rectangles = [] #list of rectangles that've been drawn

def draw_rect(event, x,y, flags, param):
    global ix, iy, drawing, img, img2
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        img = img2
        rectangles.append([(ix, iy), (x, y)])
    elif (event == cv2.EVENT_MOUSEMOVE) & drawing:
        img2 = img.copy()
        cv2.rectangle(img2, (ix, iy), (x, y), (0,255,0), 2)
        cv2.imshow('image', img2)

cv2.namedWindow('image', flags=cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', draw_rect)

while(True):
    cv2.imshow('image', img)
    key = cv2.waitKey(1) & 0xFF
    if (key == ord('z')) & (len(rectangles) > 0):
        rectangles.pop()
        img = original.copy()
        for rect in rectangles:
            cv2.rectangle(img, rect[0], rect[1], (0,255,0), 2)
        cv2.imshow('image', img)
    elif key == ord('s'):
        cv2.imwrite(sys.argv[2], img)
        break
    elif key == ord('q'):
        break

cv2.destroyWindow('image')

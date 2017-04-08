'''
Find missing or mis-aligned components on a pcb using a template and a target image
Syntax:
python pcb.py 'template.png' 'image.png' 'result.png'
'''
import sys
import cv2
import numpy as np
from imutils.convenience import resize
#from timeit import default_timer as timer
#start = timer()
#img = resize(cv2.imread(sys.argv[2], 0), 800)
img = cv2.imread(sys.argv[2], 0)
#template = resize(cv2.imread(sys.argv[1], 0), 800)
template = cv2.imread(sys.argv[1], 0)

_, img_bin = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
_, template_bin = cv2.threshold(template, 127, 255, cv2.THRESH_BINARY)

result = cv2.bitwise_xor(img_bin, template_bin)
result = cv2.blur(result, (5,5))
_, result = cv2.threshold(result, 127, 255, cv2.THRESH_BINARY)

_, contours, hier = cv2.findContours(result.copy(), 1, 2)
cnts = []
min_cnt_area = 300

#result_color = resize(cv2.imread(sys.argv[2], 1), 800)
result_color = cv2.imread(sys.argv[2], 1)
for c in contours:
    if cv2.contourArea(c) > min_cnt_area:
        cnts.append(c)
for cnt in cnts:
    x,y,w,h = cv2.boundingRect(cnt)
    result_color = cv2.rectangle(result_color, (x,y), (x+w, y+h), (0, 255, 255), 5)

#stop = timer()
#print stop - start

cv2.imshow('Result Binary', result), cv2.waitKey(1)
cv2.imshow('Result', result_color)
key = cv2.waitKey(0) & 0xFF
if key == ord('s'):
    cv2.imwrite(sys.argv[3], result_color)

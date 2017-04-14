'''
Unit test
python test.py imgFile tarFile
'''
import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys

from ROI import ROI
from imgAdjust import img_adjust

TITLE = 'Image'
W, H = 1024, 768
img = cv2.imread(sys.argv[1], 1)
tar = cv2.imread(sys.argv[2], 1)
myROI = ROI()
imgAdjust = img_adjust()

cv2.namedWindow(TITLE, cv2.WINDOW_NORMAL)
cv2.resizeWindow(TITLE, W, H)
cv2.setMouseCallback(TITLE, myROI.onMouse)
cv2.imshow(TITLE, img)
while(True):
    key = cv2.waitKey(1) & 0xFF
    if key == ord('a'):
        myROI.mode = 1
    elif key == ord('r'):
        myROI.mode = 0
    elif key == ord('z'):
        if myROI.rectangles and not myROI.mode:
            myROI.rectangles.pop()
        elif myROI.anchors and myROI.mode:
            myROI.anchors.pop()
    elif key == ord('q'):
        break
    myROI.drawing_anchors_and_rects(img)
    cv2.imshow(TITLE, myROI.img)

# print "List of {} anchor points:".format(len(myROI.anchors))
# for anchor in myROI.anchors:
#     print anchor[0]
# print "List of {} regions of interest:".format(len(myROI.rectangles))
# for rect in myROI.rectangles:
#     print rect
templates = []
for a in myROI.anchors:
    templates.append(img[a[0][1]:a[1][1], a[0][0]:a[1][0]])
tmp_pts = [anchor[0] for anchor in myROI.anchors]
tar_pts = imgAdjust.img_matching(templates, tar)
dst = imgAdjust.img_transform(img, tmp_pts, tar_pts)
# plt.subplot(121), plt.imshow(dst)
# plt.subplot(122), plt.imshow(tar)
# plt.show()
res = imgAdjust.img_diff(dst, tar)
cv2.imshow(TITLE, res)
cv2.waitKey(0)

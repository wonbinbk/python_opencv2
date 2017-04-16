'''
Syntax: python app.py imgFile tarFile
'''
import cv2
import numpy as np
import sys

from ROI import ROI
from imgAdjust import ImgAdjust
from imutils.convenience import resize
from timeit import default_timer as tm

try:
    img = cv2.imread(sys.argv[1], 1)
    tar = cv2.imread(sys.argv[2], 1)
except Exception as e:
    print "Error: {}".format(e)
    print __doc__
    sys.exit(1)

TITLE = 'Image'
MIN_MEAN = 20
RED = (0, 0, 255)
_, W1, _ = img.shape
# To speed up processing image, we need to scale down images
# W, H is scaled image size
W, H = 800, 600
RATIO = W1 / float(W)
img_copy = img.copy()
img = resize(img, W)
tar_copy = tar.copy()
tar = resize(tar, W)
myROI = ROI()
imgAdjust = ImgAdjust()

cv2.namedWindow(TITLE, cv2.WINDOW_NORMAL)
cv2.resizeWindow(TITLE, W, H)
cv2.setMouseCallback(TITLE, myROI.onMouse)
cv2.imshow(TITLE, img_copy)

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
    myROI.img = myROI.drawing_anchors_and_rects(img_copy)
    cv2.imshow(TITLE, myROI.img)
start = tm()
myROI.anchors = myROI.anchors[:3]   # Only 3 points needed
templates = []
for a in myROI.anchors:
    tl = tuple([int(r / RATIO) for r in a[0]])
    br = tuple([int(r / RATIO) for r in a[1]])
    templates.append(img[tl[1]:br[1], tl[0]:br[0]])
tmp_pts = [anchor[0] for anchor in myROI.anchors]
tar_pts = imgAdjust.img_matching(templates, tar)
dst = imgAdjust.img_transform(img_copy, tmp_pts, tar_pts)
res = imgAdjust.img_diff(dst, tar_copy)

img_diff = []   # List of tuple (index, res_of_ROI)
for index, rect in enumerate(myROI.rectangles):
    tl = rect[0]
    br = rect[1]
    img_diff.append((index, res[tl[1]:br[1], tl[0]:br[0]]))
# TODO: SOMETHING WRONG HERE
index_roi = [roi[0] for roi in img_diff if np.mean(roi[1]) > MIN_MEAN]
for i in index_roi:
    tl = myROI.rectangles[i][0]
    br = myROI.rectangles[i][1]
    cv2.rectangle(tar_copy, tl, br, RED, 2)
stop = tm()
print 'It took {}(s)'.format(stop - start)
while(True):
    cv2.imshow(TITLE, tar_copy)
    if cv2.waitKey(500) & 0xFF == ord('q'):
        break

cv2.destroyWindow(TITLE)

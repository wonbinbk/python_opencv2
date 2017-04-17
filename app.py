'''
Syntax: python app.py imgFile tarFile
'''
import cv2
import numpy as np
import sys

from ROI import ROI
from imgAdjust import ImgAdjust

try:
    _IMG = sys.argv[1]
    _TAR = sys.argv[2]
except Exception as e:
    # print "Error: {}".format(e)
    # print __doc__
    # sys.exit(1)
    _IMG = 'DeviceImg.bmp'
    _TAR = 'EmptyImg.bmp'
img = cv2.imread(_IMG, 1)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
tar = cv2.imread(_TAR, 1)
tar_gray = cv2.cvtColor(tar, cv2.COLOR_BGR2GRAY)
_TITLE = 'Image'
_MIN_MEAN = 20
_RED = (0, 0, 255)
_THICK = 2
_LIMIT = 10     # threshold of mean binary
H, W = img.shape[:2]
myROI = ROI()
imgAdjust = ImgAdjust()
cv2.namedWindow(_TITLE, cv2.WINDOW_NORMAL)
cv2.resizeWindow(_TITLE, 1024, 768)
cv2.moveWindow(_TITLE, 300, 300)
cv2.setMouseCallback(_TITLE, myROI.onMouse)
cv2.imshow(_TITLE, img)
# Done show image & get rectangles + anchors
while(True):
    key = cv2.waitKey(100) & 0xFF
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
    myROI.img = myROI.drawing_anchors_and_rects(img)
    cv2.imshow(_TITLE, myROI.img)
# Get templates
myROI.anchors = myROI.anchors[:3]   # Need only 3 anchors
templates = []
for a in myROI.anchors:
    templates.append(img[a[0][1]:a[1][1], a[0][0]:a[1][0]])
# Get template's top_left points
tmp_pts = [a[0] for a in myROI.anchors]
# Get target corresponded's top_left points
tar_pts = imgAdjust.img_matching(templates, tar)
# Affine transform img to tar
dst = imgAdjust.img_transform(img_gray, tmp_pts, tar_pts)
# Get binary different image
res = imgAdjust.img_diff(dst, tar_gray)
bingo = [r for r in myROI.rectangles if np.mean(
        res[r[0][1]:r[1][1], r[0][0]:r[1][0]]) > _LIMIT]
img_display = img.copy()
for b in bingo:
    cv2.rectangle(img_display, b[0], b[1], _RED, _THICK)
cv2.imshow(_TITLE, img_display)
while(True):
    key = cv2.waitKey(100) & 0xFF
    if key == ord('q'):
        break
cv2.destroyAllWindows()

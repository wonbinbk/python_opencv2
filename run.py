'''Show the active ROIs of the target image

Syntax: python run.py target_file_name img_file_name sensitivity
* img_file_name: Original image considered good with all components in.
Output: - images of missing components
        - draw RED bounding around missing components (or active ROI)'''

import cv2
import numpy as np
import sys
import pickle
from ROI import ROI
from imgAdjust import ImgAdjust
from misc import createWindow

_TITLE = 'Image'
_MIN_MEAN = 20
_RED = (0, 0, 255)
_THICK = 2

try:
    _IMG = sys.argv[2]
    _TAR = sys.argv[1]
    _LIMIT = int(sys.argv[3])
except Exception as e:
    print "Error: {}".format(e)
    print __doc__
    sys.exit(1)
img_gray = cv2.imread(_IMG, 0)
H, W = img_gray.shape
tar = cv2.imread(_TAR, 1)
tar_gray = cv2.cvtColor(tar, cv2.COLOR_BGR2GRAY)
myROI = ROI()
ImgAdjust = ImgAdjust()
img_name = _IMG[:-4]
with open(''.join([img_name, '.anc']), 'rb') as f:
    myROI.anchors = pickle.load(f)
with open(''.join([img_name, '.roi']), 'rb') as f:
    myROI.rectangles = pickle.load(f)
templates, tmp_pts = [], []
for i, a in enumerate(myROI.anchors):
    templates.append(cv2.imread("template {}.png".format(i+1), 1))
    tmp_pts.append(a[0])
tar_pts = ImgAdjust.img_matching(templates, tar)
dst = ImgAdjust.img_transform(img_gray, tmp_pts, tar_pts)
res = ImgAdjust.img_diff(dst, tar_gray)
bingo = [r for r in myROI.rectangles if np.mean(
        res[r[0][1]:r[1][1], r[0][0]:r[1][0]]) > _LIMIT]
for b in bingo:
    cv2.rectangle(tar, b[0], b[1], _RED, _THICK)
createWindow(_TITLE, 1024, 768)
cv2.imshow(_TITLE, tar)
while(True):
    key = cv2.waitKey(100) & 0xFF
    if key == ord('q'):
        break
cv2.destroyWindow(_TITLE)

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
from misc import _inspect_image

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
try:
    with open(''.join([img_name, '.anc']), 'rb') as f:
        myROI.anchors = pickle.load(f)
except IOError as e:
    print "File " + img_name + ".anc" " not found."
    print "You need to run file anchors.py first"
    raise e
    sys.exit(1)
try:
    with open(''.join([img_name, '.roi']), 'rb') as f:
        myROI.rectangles = pickle.load(f)
except IOError as e:
    print "File " + img_name + ".roi" " not found."
    print "Using empty list of rectangles now"
    print "For testing purpose only."
    myROI.rectangles = []

templates, tmp_pts = [], []
for i, a in enumerate(myROI.anchors):
    templates.append(cv2.imread("template {}.png".format(i+1), 1))
    tmp_pts.append(a[0])

# -----------------------------------------------
# TESTING: draw template boundary in target_image
temp_size = [t.shape[:2] for t in templates]
tar_pts = ImgAdjust.img_matching(templates, tar)
tar_anchors = tar.copy()
for i, t in enumerate(temp_size):
    cv2.rectangle(
        tar_anchors,
        (tar_pts[i][0] + t[1], tar_pts[i][1]),
        (tar_pts[i][0], tar_pts[i][1] + t[0]),
        (255, 255, 0),
        2)
_inspect_image('Tar Anchors', tar_anchors, 1024, 768)
# -----------------------------------------------
dst = ImgAdjust.img_transform(img_gray, tmp_pts, tar_pts)
_inspect_image('Transform', dst, 1024, 768)
res = ImgAdjust.img_diff(dst, tar_gray)
_inspect_image('Binary', res, 1024, 768)
bingo = [r for r in myROI.rectangles if np.mean(
        res[r[0][1]:r[1][1], r[0][0]:r[1][0]]) > _LIMIT]
for b in bingo:
    cv2.rectangle(tar, b[0], b[1], _RED, _THICK)
createWindow(_TITLE, 1024, 768)
# img_dict = {"Anchors Detect": tar_anchors, "Img Transform": dst,
#             }
cv2.imshow(_TITLE, tar)
while(True):
    key = cv2.waitKey(100) & 0xFF
    if key == ord('q'):
        break
cv2.destroyWindow(_TITLE)

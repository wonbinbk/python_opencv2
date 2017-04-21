'''Show the active ROIs of the target image

Syntax: python run.py img_file_name target_file_name -t/--threshold THRESHOLD
* img_file_name: Original image considered good with all components in.
* target_file_name: Image under test
* THRESHOLD: Threshold level to classify ROIs.
Output: - images of missing components.
        - draw RED bounding around missing components (or active ROI).'''

import cv2
import numpy as np
import argparse
import pickle
from ROI import ROI
from imgAdjust import ImgAdjust
from misc import _inspect_image

ap = argparse.ArgumentParser()
ap.add_argument('img', help='Original image considered good.')
ap.add_argument('tar', help='Image under test.')
ap.add_argument('-t', '--threshold', default=20, type=int,
                help='Threshold level to classify ROIs. Default: 20.')
ap.add_argument('-a', '--anchor',
                help='File contains list of anchor points.')
ap.add_argument('-r', '--roi',
                help='File contains list of regions of interest.')
args = ap.parse_args()
_IMG = args.img
_TAR = args.tar
if args.anchor:
    _ANC_FILE = args.anchor
else:
    _ANC_FILE = ''.join([_IMG[:-4], '.anc'])
if args.roi:
    _ROI_FILE = args.roi
else:
    _ROI_FILE = ''.join([_IMG[:-4], '.roi'])
_LIMIT = args.threshold
_TITLE = 'Image'
_MIN_MEAN = 20
_RED = (0, 0, 255)
_GREEN = (0, 255, 0)
_THICK = 2
img = cv2.imread(_IMG, 1)
img_gray = cv2.imread(_IMG, 0)
tar = cv2.imread(_TAR, 1)
tar_gray = cv2.cvtColor(tar, cv2.COLOR_BGR2GRAY)
myROI = ROI()
ImgAdjust = ImgAdjust()
img_name = _IMG[:-4]
with open(_ANC_FILE, 'rb') as f:
    myROI.anchors = pickle.load(f)
with open(_ROI_FILE, 'rb') as f:
    myROI.rectangles = pickle.load(f)
templates, tmp_pts = [], []
for i, a in enumerate(myROI.anchors):
    templates.append(cv2.imread("template {}.png".format(i+1), 1))
    tmp_pts.append(a[0])
temp_size = [t.shape[:2] for t in templates]
tar_pts = ImgAdjust.img_matching(templates, tar)
dst = ImgAdjust.img_transform(img_gray, tmp_pts, tar_pts)
bingo = []
left_over = []
mean_over_limit = []
mean_under_limit = []
for r in myROI.rectangles:
    img_ROI = dst[r[0][1]:r[1][1], r[0][0]:r[1][0]]
    tar_ROI = tar_gray[r[0][1]:r[1][1], r[0][0]:r[1][0]]
    diff_ROI = ImgAdjust.img_diff(img_ROI, tar_ROI)
    mean_ROI = np.mean(diff_ROI)
    if mean_ROI > _LIMIT:
        bingo.append(r)
        mean_over_limit.append(mean_ROI)
    else:
        left_over.append(r)
        mean_under_limit.append(mean_ROI)
for i, b in enumerate(bingo):
    cv2.rectangle(tar, b[0], b[1], _RED, _THICK)
    cv2.putText(tar, str(mean_over_limit[i]),
                (b[0][0], b[0][1]-5),
                cv2.FONT_HERSHEY_PLAIN,
                1,      # Font scale
                _RED,
                2)      # THICKNESS of Text
for j, r in enumerate(left_over):
    cv2.rectangle(tar, r[0], r[1], _GREEN, _THICK)
    cv2.putText(tar, str(mean_under_limit[j]),
                (r[0][0], r[0][1]-5),
                cv2.FONT_HERSHEY_PLAIN,
                1,      # Font scale
                _GREEN,
                2)      # THICKNESS of Text
_inspect_image(tar, _TITLE, 1024, 768)
cv2.destroyWindow(_TITLE)

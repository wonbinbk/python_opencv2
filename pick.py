'''Open image, choose and save regions of interest

Syntax: python pick.py img_file_name -t/--type TYPE
TYPE = anchor or roi.
Output:
        - file image_name.roi
        - file image_name.anc'''

import cv2
import argparse
import pickle

from ROI import ROI
from misc import createWindow

ap = argparse.ArgumentParser()
ap.add_argument("image", help='Image file name with full extension.')
ap.add_argument("-t", "--type", default='a',
                choices=['anchor', 'a', 'roi', 'r'],
                help='Pick anchor or roi.')
ap.add_argument("-o", "--output",
                help='Name of output file.')
args = ap.parse_args()

_IMG = args.image
if not args.output:
    save_name = _IMG[:-4]
else:
    save_name = args.output
img = cv2.imread(_IMG, 1)
_TITLE = 'Image'
H, W = img.shape[:2]
myROI = ROI()
if args.type in ['a', 'anchor']:
    save_ext = '.anc'
    myROI.mode = 1
else:
    save_ext = '.roi'
    myROI.mode = 0

createWindow(_TITLE, 1024, 768, myROI.onMouse)
cv2.imshow(_TITLE, img)
# Show image allow user to pick
while(True):
    key = cv2.waitKey(100) & 0xFF
    if key == ord('z'):
        if myROI.rectangles and not myROI.mode:
            myROI.rectangles.pop()
        elif myROI.anchors and myROI.mode:
            myROI.anchors.pop()
    elif key == ord('q'):
        break
    myROI.img = myROI.drawing_anchors_and_rects(img)
    cv2.imshow(_TITLE, myROI.img)
# Save list of coordinate to a file
with open(''.join([save_name, save_ext]), 'wb') as f:
    if myROI.mode:
        myROI.anchors = myROI.points_sort(myROI.anchors)
        pickle.dump(myROI.anchors, f)
    else:
        myROI.rectangles = myROI.points_sort(myROI.rectangles)
        pickle.dump(myROI.rectangles, f)
    print ''.join(["File ", save_name, save_ext, " saved"])

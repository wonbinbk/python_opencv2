'''Open image, choose and save regions of interest

Syntax: python anchors.py image_name
Output:
        - file image_name.roi'''

import cv2
import sys
import pickle

from ROI import ROI
from misc import createWindow

try:
    _IMG = sys.argv[1]
except Exception as e:
    print "Error: {}".format(e)
    print __doc__
    sys.exit(1)

img = cv2.imread(_IMG, 1)
_TITLE = 'Image'
H, W = img.shape[:2]
myROI = ROI()
myROI.mode = 0
createWindow(_TITLE, 1024, 768, myROI.onMouse)
cv2.imshow(_TITLE, img)

while(True):
    key = cv2.waitKey(100) & 0xFF
    if key == ord('z'):
        if myROI.rectangles:
            myROI.rectangles.pop()
    elif key == ord('q'):
        break
    myROI.img = myROI.drawing_anchors_and_rects(img)
    cv2.imshow(_TITLE, myROI.img)
save_name = _IMG[:-4]
# Save ROI coordinate to a file
with open(''.join([save_name, '.roi']), 'wb') as f:
    pickle.dump(myROI.rectangles, f)

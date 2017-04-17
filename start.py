'''Open image, choose and save anchor points and Region of interest

Syntax: python start.py image_name
Output: - images of templates from anchor points saved as "template x.png"
        - file image_name.anc
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
createWindow(_TITLE, 1024, 768, myROI.onMouse)
cv2.imshow(_TITLE, img)

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

myROI.anchors = myROI.anchors[:3]   # Need only 3 anchors
templates = [img[a[0][1]:a[1][1], a[0][0]:a[1][0]] for a in myROI.anchors]
# Save templates to png files
for i, temp in enumerate(templates):
    cv2.imwrite("template {}.png".format(i+1), temp)
# Save anchors coordinate to a file
save_name = _IMG[:-4]
with open(''.join([save_name, '.anc']), 'wb') as f:
    pickle.dump(myROI.anchors, f)
# Save ROI coordinate to a file
with open(''.join([save_name, '.roi']), 'wb') as f:
    pickle.dump(myROI.rectangles, f)

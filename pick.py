#!/usr/bin/env python
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


class pick(object):

    def save_coordinate(self):
        '''Save coordinates of anchors or ROIs to a file.

        File will be saved as image_name.anc or image_name.roi.'''

        with open(''.join([self.save_name, self.save_ext]), 'wb') as f:
            if self.ROI.mode:
                self.ROI.anchors = self.ROI.points_sort(self.ROI.anchors)
                pickle.dump(self.ROI.anchors, f)
                for i, a in enumerate(self.ROI.anchors):
                    cv2.imwrite('template {}.png'.format(i+1),
                                self.ROI.img[a[0][1]:a[1][1], a[0][0]:a[1][0]])
            else:
                self.ROI.rectangles = self.ROI.points_sort(self.ROI.rectangles)
                pickle.dump(self.ROI.rectangles, f)

    def crop_interest_areas(self, title='Draw rectangles', W=1024, H=768):
        '''Open image, allow user to draw anchors and ROI.

        (Number of anchors: 3).'''

        createWindow(title, W, H, self.ROI.onMouse)
        while(True):
            cv2.imshow(title, self.ROI.img)
            key = cv2.waitKey(100) & 0xFF
            if key == ord('z'):
                if self.ROI.rectangles and not self.ROI.mode:
                    self.ROI.rectangles.pop()
                elif self.ROI.anchors and self.ROI.mode:
                    self.ROI.anchors.pop()
            elif key == ord('q'):
                break
            self.ROI.anchors = self.ROI.anchors[:3]  # Need only 3 anchors.
            self.ROI.img = self.ROI.drawing_anchors_and_rects(self._img)

    def __init__(self, _IMG, ptype='a'):
        self.ROI = ROI()
        self._img = cv2.imread(_IMG, 1)
        self.ROI.img = self._img.copy()
        self.save_name = _IMG[:-4]
        self.ptype = ptype
        if self.ptype in ('a', 'A', 'anchor', 'ANCHOR', 'Anchor'):
            self.ROI.mode = 1
            self.save_ext = '.anc'
        elif self.ptype in ('r', 'R', 'ROI', 'roi', 'Roi'):
            self.ROI.mode = 0
            self.save_ext = '.roi'


if __name__ == '__main__':
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
    mypick = pick(_IMG, ptype=args.type)
    mypick.crop_interest_areas()
    mypick.save_coordinate()

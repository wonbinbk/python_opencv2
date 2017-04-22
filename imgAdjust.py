#!/usr/bin/env python
import cv2
import numpy as np


class ImgAdjust:

    def __init__(self):
        self._ERROR = 100

    def img_matching(self, templates, tmp_pts, tar_img):
        '''Return a list of Top_left point of matched area of templates found in
        target_image (list of nw)'''
        # TODO: Re-code for more pythonic
        # The code works but look stupid.
        tar_pts = []
        H, W = tar_img.shape[:2]
        for i, temp in enumerate(templates):
            h, w = temp.shape[:2]
            tl = [max(0, z - self._ERROR) for z in tmp_pts[i]]
            br = [0, 0]
            br[0] = min(W, tmp_pts[i][0] + w + self._ERROR)
            br[1] = min(H, tmp_pts[i][1] + h + self._ERROR)
            res = cv2.matchTemplate(tar_img[tl[1]:br[1], tl[0]:br[0]],
                                    temp,
                                    cv2.TM_CCORR_NORMED)
            _, _, _, nw = cv2.minMaxLoc(res)
            NW = [0, 0]
            NW[0] = nw[0] + tl[0]
            NW[1] = nw[1] + tl[1]
            tar_pts.append(NW)
        return tar_pts

    def img_transform(self, image, tmp_pts, tar_pts):
        '''Return affine transformed image using 2 3-points lists'''
        # Make sure list is a numpy array of float32
        tmp_pts = np.array(tmp_pts, dtype=np.float32)
        tmp_pts = tmp_pts.reshape((-1, 1, 2))
        tar_pts = np.array(tar_pts, dtype=np.float32)
        tar_pts = tar_pts.reshape((-1, 1, 2))
        # Get Affine Transform matrix
        M = cv2.getAffineTransform(tmp_pts, tar_pts)
        # Do the transform
        dst = cv2.warpAffine(image, M, image.shape[:2][::-1])

        return dst

    def img_diff(self, dst, tar):
        '''Return a binary image based on different between dst and tar'''
        res = cv2.absdiff(tar, dst)

        return res

    def find_ROI(self, res, rectangles, lower_limit):
        '''Return ROI list that has mean > lower_limit'''
        return [r for r in rectangles if np.mean(
                res[r[0][1]:r[1][1], r[0][0]:r[1][0]]) > lower_limit]

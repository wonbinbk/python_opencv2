import cv2
import numpy as np


class ImgAdjust:

    def img_matching(self, templates, target_image):
        '''
        Return a list of Top_left point of matched area of templates found in
        target_image (list of nw)
        '''
        tar_pts = []
        for temp in templates:
            h, w = temp.shape[:2]
            res = cv2.matchTemplate(target_image, temp, cv2.TM_CCOEFF)
            _, _, _, nw = cv2.minMaxLoc(res)
            tar_pts.append(nw)

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
        # dst_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        dst_blur = cv2.blur(dst, (5, 5))
        _, dst_bin = cv2.threshold(dst_blur, 50, 200, cv2.THRESH_BINARY)
        # tar_gray = cv2.cvtColor(tar, cv2.COLOR_BGR2GRAY)
        tar_blur = cv2.blur(tar, (5, 5))
        _, tar_bin = cv2.threshold(tar_blur, 50, 200, cv2.THRESH_BINARY)
        res = cv2.bitwise_xor(tar_bin, dst_bin)

        return res

    def find_ROI(res, rectangles, lower_limit):
        '''Return ROI list that has mean > lower_limit'''
        return [r for r in rectangles if np.mean(
                res[r[0][1]:r[1][1], r[0][0]:r[1][0]]) > lower_limit]

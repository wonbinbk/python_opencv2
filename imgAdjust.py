import cv2
import numpy as np


class img_adjust:

    def img_matching(self, templates, target_image):
        '''
        Return a list of Top_left point of matched area of templates found in
        target_image (list of nw)
        '''
        tar_pts = []
        for temp in templates:
            h, w, _ = temp.shape
            res = cv2.matchTemplate(target_image, temp, cv2.TM_CCOEFF)
            _, _, _, nw = cv2.minMaxLoc(res)
            tar_pts.append(nw)
        return tar_pts

    def img_transform(self, image, tmp_pts, tar_pts):
        '''
        Return affine transformed image from image
        using list of 3 points tmp_pts and tar_pts
        '''
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
        '''
        Return a binary image based on different between dst and tar
        '''
        dst_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        dst_blur = cv2.blur(dst_gray, (5, 5))
        _, dst_bin = cv2.threshold(dst_blur, 50, 200, cv2.THRESH_BINARY)
        tar_gray = cv2.cvtColor(tar, cv2.COLOR_BGR2GRAY)
        tar_blur = cv2.blur(tar_gray, (5, 5))
        _, tar_bin = cv2.threshold(tar_blur, 50, 200, cv2.THRESH_BINARY)
        res = cv2.bitwise_xor(tar_bin, dst_bin)

        return res

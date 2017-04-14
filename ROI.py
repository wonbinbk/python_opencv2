'''
ROI.py
input: target image

user interactive:   + pick anchor points
                    + draw rectangles around regions of interest

output:             + array of ROIs
                    + array of anchor points
'''
import cv2
import sys


class ROI:
    COLOR_RECTANGLE = (0, 255, 0)
    COLOR_ANCHOR = (0, 255, 255)
    REC_THICKNESS = 8
    ANC_THICKNESS = 3
    ANCHOR_SIZE = 20

    def __init__(self):
        self.anchors = []
        self.rectangles = []
        self.mode = 0
        self.drawing = 0
        self.ix, self.iy = -1, -1
        self.leftclicked = 0
        self.img = None

    def onMouse(self, event, x, y, flags, param):
        '''
        Mouse events' callback
        '''
        if self.mode:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.anchors.append((x, y))
        elif event == cv2.EVENT_LBUTTONDOWN:
            self.ix, self.iy = x, y
            self.leftclicked = 1
            self.rectangles.append([None, None])
        elif event == cv2.EVENT_MOUSEMOVE and self.leftclicked:
            self.drawing = 1
            self.rectangles.pop()
            self.rectangles.append([(self.ix, self.iy), (x, y)])
        elif event == cv2.EVENT_LBUTTONUP:
            if not self.drawing:
                self.rectangles.pop()
            else:
                self.drawing = 0
            self.leftclicked = 0

    def drawing_anchors_and_rects(self, img):
        '''
        Draw rectangles and points (anchors) on an input image
        Return: output image with rectangles and points
        '''
        self.img = img.copy()
        for rect in self.rectangles:
            cv2.rectangle(
                self.img,
                rect[0],
                rect[1],
                ROI.COLOR_RECTANGLE,
                ROI.REC_THICKNESS)
        for anchor in self.anchors:
            cv2.circle(
                self.img,
                anchor,
                ROI.ANCHOR_SIZE,
                ROI.COLOR_ANCHOR,
                ROI.ANC_THICKNESS)
            cv2.line(
                self.img,
                (anchor[0] - 2 * ROI.ANCHOR_SIZE, anchor[1]),
                (anchor[0] + 2 * ROI.ANCHOR_SIZE, anchor[1]),
                ROI.COLOR_ANCHOR,
                ROI.ANC_THICKNESS)
            cv2.line(
                self.img,
                (anchor[0], anchor[1] - 2 * ROI.ANCHOR_SIZE),
                (anchor[0], anchor[1] + 2 * ROI.ANCHOR_SIZE),
                ROI.COLOR_ANCHOR,
                ROI.ANC_THICKNESS)


if __name__ == '__main__':
    myROI = ROI()
    img = cv2.imread(sys.argv[1], 1)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', myROI.onMouse)
    cv2.imshow('image', img)
    while(True):
        key = cv2.waitKey(1) & 0xFF
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
        myROI.drawing_anchors_and_rects(img)
        cv2.imshow('image', myROI.img)
    cv2.destroyWindow('image')

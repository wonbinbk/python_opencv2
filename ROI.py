'''
ROI.py
input: target image

user interactive:   + pick anchor points
                    + draw rectangles around regions of interest

output:             + array of ROIs
                    + array of anchor points
'''
import cv2


class ROI:
    COLOR_RECTANGLE = (0, 255, 0)
    COLOR_ANCHOR = (0, 255, 255)
    REC_THICKNESS = 2
    ANC_THICKNESS = 2

    def __init__(self):
        self.anchors = []
        self.rectangles = []
        self.mode = 1
        self.drawing = 0
        self.ix, self.iy = -1, -1
        self.leftclicked = 0
        self.img = None

    def onMouse(self, event, x, y, flags, param):
        '''
        Mouse events' callback
        self.mode == 1 : anchor points
        self.mode == 0 : rectangles
        '''
        if event == cv2.EVENT_LBUTTONDOWN:
            self.ix, self.iy = x, y
            self.leftclicked = 1
            if self.mode:
                self.anchors.append([None, None])
            else:
                self.rectangles.append([None, None])
        elif event == cv2.EVENT_MOUSEMOVE and self.leftclicked:
            self.drawing = 1
            if self.mode:
                self.anchors.pop()
                self.anchors.append([(self.ix, self.iy), (x, y)])
            else:
                self.rectangles.pop()
                self.rectangles.append([(self.ix, self.iy), (x, y)])
        elif event == cv2.EVENT_LBUTTONUP:
            if not self.drawing:
                if self.mode:
                    self.anchors.pop()
                else:
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
            cv2.rectangle(
                self.img,
                anchor[0],
                anchor[1],
                ROI.COLOR_ANCHOR,
                ROI.ANC_THICKNESS)
        return self.img

    def points_sort(self, coordinate_list):
        '''Return a re-arrange or re-calculate coordinate list
        In order: [top-left, bottom_right]'''
        new_list = []
        for r in coordinate_list:
            x1, x2 = min(r[0][0], r[1][0]), max(r[0][0], r[1][0])
            y1, y2 = min(r[0][1], r[1][1]), max(r[0][1], r[1][1])
            new_list.append([(x1, y1), (x2, y2)])

        return new_list


if __name__ == '__main__':
    import sys
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

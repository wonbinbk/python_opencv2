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


def draw_rect(event, x, y, flags, (img, windows_name)):
    global ix, iy
    global drawing
    img_display = img
    temp_img = img_display.copy()
    if event == cv2.EVENT_LBUTTONDOWN:
        if mode == 'anchors':
            drawing = False
            anchors.append((x, y))
        elif mode == 'rectangles':
            drawing = True
            ix, iy = x, y
            rectangles.append([(ix, iy), None])
    elif (event == cv2.EVENT_MOUSEMOVE) & drawing:
        # TODO
        rectangles.pop()
        temp_img = img_display.copy()
        if mode == 'rectangles':
            cv2.rectangle(temp_img, (ix, iy), (x, y), (0, 255, 0), 2)
        cv2.imshow(windows_name, temp_img)
        rectangles.append([(ix, iy), (x, y)])
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
    img_display = temp_img.copy()


if __name__ == '__main__':
    point = (20, 50)    # point[0] = point radius; point[1] = line length
    rectangles = []
    anchors = []
    ix, iy = -1, -1
    drawing = False
    mode = 'rectangles'
    img = cv2.imread(sys.argv[1], 1)
    img_display = img.copy()
    windows_name = 'image'
    cv2.namedWindow(windows_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(windows_name, draw_rect, (img, windows_name))
    cv2.imshow(windows_name, img_display)

    while(True):
        key = cv2.waitKey(1) & 0xFF
        if key == ord('z'):
            if (mode == 'rectangles') & (len(rectangles) > 0):
                rectangles.pop()
            elif (mode == 'anchors') & (len(anchors) > 0):
                anchors.pop()
        elif key == ord('a'):
            mode = 'anchors'
        elif key == ord('r'):
            mode = 'rectangles'
        elif key == ord('q'):
            break
        img_display = img.copy()
        for rect in rectangles:
            if rect[1]:
                cv2.rectangle(img_display, rect[0], rect[1], (0, 255, 0), 2)
        for anchor in anchors:
            cv2.circle(img_display,
                       (anchor[0], anchor[1]),
                       point[0], (0, 255, 255), 2)
            cv2.line(img_display,
                     (anchor[0] - point[1]/2, anchor[1]),
                     (anchor[0] + point[1]/2, anchor[1]),
                     (0, 255, 255), 2)
            cv2.line(img_display,
                     (anchor[0], anchor[1] - point[1]/2),
                     (anchor[0], anchor[1] + point[1]/2),
                     (0, 255, 255), 2)
        cv2.imshow(windows_name, img_display)

    print "List of anchor points:\n"
    print "".join(str(anchor for anchor in anchors))
    cv2.destroyAllWindows()

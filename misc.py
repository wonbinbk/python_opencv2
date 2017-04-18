from matplotlib import pyplot as plt
import cv2


def plot(title, *argv):
    '''Use pyplot from matplotlib to draw img from argv and title list'''
    n = len(argv)
    if len(title) != n:
        title = [''] * n
    if n > 2:
        ncols = 3
        nrows = (n / 3) + 1
    else:
        ncols = 2
        nrows = 1
    for i, img in enumerate(argv):
        plt.subplot(nrows, ncols, i + 1)
        plt.imshow(img, 'gray')
        plt.title(title[i])
    plt.show()


def createWindow(TITLE, W, H, mouseCallBack=None):
    '''Create new window with size W x H and optional mouse callback'''
    cv2.namedWindow(TITLE, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(TITLE, W, H)
    cv2.moveWindow(TITLE, 100, 100)
    if mouseCallBack:
        cv2.setMouseCallback(TITLE, mouseCallBack)


def _inspect_image(TITLE, img, W, H):
    createWindow(TITLE, W, H)
    cv2.imshow(TITLE, img)
    while(True):
        key = cv2.waitKey(100) & 0xFF
        if key == ord('q'):
            cv2.destroyWindow(TITLE)
            break

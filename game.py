import cv2 as cv
import numpy as np
import os
from time import time
import pyautogui
import win32gui, win32ui, win32con

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def window_capture():
    w = 1920
    h = 1080

    hwnd = win32gui.FindWindow(None, windowname)

    # get the window image data
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)

    # save the screenshot
    #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)
    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())


    # drop the alpha channel, or cv.matchTemplate() will throw an error like:
    # error: (-215:Assertion failed) (depth == CV_BU || depth == CV_32F) && type == _templ.type()
    #&& _img.dims() <= 2 in function 'cv::matchTemplate'
    img = img[...,:3]

    #make image C_CONTIGUOUS to avoid errors that look like:
    #   file ... in draw_rectangles
    #   TypeError: an integer is required (got type tuple)
    #   see the discussion here:
    # https://github.com/opencv/opencv/issues/14866#issurecomment-580207109
    img = np.ascontiguousarray(img)
    return img










loop_time = time()
while(True):

    screenshot = window_capture()
  
    cv.imshow('Computer Vision', screenshot)

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
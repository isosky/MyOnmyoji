#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-1-1 10:49
# @Author  : isosky
# @Site    : 
# @File    : mergecard.py

import win32gui, win32ui, win32con
import numpy as np
import cv2


def gbk2utf8(s):
    return s.decode('gbk').encode('utf-8')


def getallOnmyoji():
    label = r'阴阳师-网易游戏'
    # hwnd = win32gui.FindWindow(None, label)
    # if hwnd:
    #     print(hwnd)
    hWndList = []
    rshwnd = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    for hwnd in hWndList:
        title = win32gui.GetWindowText(hwnd)
        # title = gbk2utf8(title)
        if title == label:
            # rshwnd.append(hwnd)
            rshwnd.append(Onmyojiwindow(hwnd))
            print(hwnd, title)
    return rshwnd


class Onmyojiwindow:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.left, self.top, self.right, self.bottom = win32gui.GetWindowRect(self.hwnd)
        # print(self.left, self.top, self.right, self.bottom)
        self.client_rect = win32gui.GetClientRect(self.hwnd)
        # print(self.client_rect)
        self.width = self.client_rect[2]
        self.height = self.client_rect[3]
        # print(self.width, self.height)


def getscreen(ow, res):
    # https://blog.csdn.net/qq_16234613/article/details/79155538
    hwindc = win32gui.GetWindowDC(ow.hwnd)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, ow.width, ow.height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (ow.width, ow.height), srcdc, (8, 4), win32con.SRCCOPY)
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (ow.height, ow.width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(ow.hwnd, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

    # save file
    # from PIL import Image
    # im = Image.fromarray(img)
    # im.save("test.png")


def findimage(source, destination):
    import aircv as ac
    from PIL import Image

    imsrc = ac.imread('./img/taiyin_1_s.png')  # 原始图像
    imsch = ac.imread('./img/temp3.png')  # 带查找的部分
    # print(ac.find_all_template(imsrc, imsch, ))
    temp = ac.find_all_template(imsrc, imsch, threshold=0.9)
    for i in temp:
        print(i)
        top_left = i['rectangle'][0]
        top_right = [top_left[0] + imsrc.shape[0], top_left[1]]
        bottom_right = [top_left[0] + imsrc.shape[0], top_left[1] + imsrc.shape[1]]
        bottom_left = [top_left[0], top_left[1] + imsrc.shape[1]]
        square = np.array([(top_left, top_right, bottom_right, bottom_left)])
        print(square)
        # square = np.array([[(1827, 695), (1827, 1873), (695, 1873), (695, 714)]])
        cv2.polylines(imsch, square, 1, (255, 255, 255, 1), 2)
        img = cv2.cvtColor(imsch, cv2.COLOR_BGRA2RGB)
        im = Image.fromarray(img)
        im.show()
    return 0


if __name__ == '__main__':
    # res = getallOnmyoji()
    # temp = res[0]
    # getscreen(temp, None)
    findimage(1, 2)

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
    imsrc = ac.imread('./img/temp1.png')  # 原始图像
    imsch = ac.imread('./img/scrapy.png')  # 带查找的部分
    print(ac.find_template(imsrc, imsch,con))
    return 0


if __name__ == '__main__':
    # res = getallOnmyoji()
    # temp = res[0]
    # getscreen(temp, None)
    findimage(1,2)
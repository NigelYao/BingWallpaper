#!/usr/bin/env python
# -- coding: utf-8 --
import urllib,re,urllib.request,os,win32api,win32gui
from win32api import *
from win32gui import *
import win32con
import sys
import struct
import time
import json

class WindowsBalloonTip:
    def __init__(self, title, msg):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow( classAtom, "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "bing.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
           hicon = LoadImage(hinst, iconPathName, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
          hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, \
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",msg,200,title))
        # self.show_balloon(title, msg)
        time.sleep(10)
        DestroyWindow(self.hwnd)
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.

def balloon_tip(title, msg):
    w=WindowsBalloonTip(title, msg)

def tryDownloadVideo(result):
	vid = result['images'][0]
	if 'vid' in vid.keys():
		src = vid['vid']['sources'][1]
		video_url = src[2]
		if(not video_url):
			return False;
		video_url = video_url.replace('\\',"")
		print(video_url)
		video_name = video_url.split('/')[-1]
		print(video_name)
		if(video_url.find('http') > 0):
			video_src = urllib.request.urlopen(video_url).read()
		else:
			video_src = urllib.request.urlopen("http:" + video_url).read()
		video_file = video_folder + "/" + video_name
		with open(video_file, 'wb') as f:
		        f.write(video_src)
		balloon_tip("视频也已下载完毕","本日的壁纸包含对应视频，已经保存到您的电脑目录")
	return True;

pic_folder = "D:/OneDrive/图片/必应壁纸"
video_folder = "D:/OneDrive/图片/必应视频"
bing_url = "http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1439260838289&pid=hp&video=1"

#未联网的情况下等待
times = 10
waitSeconds = 15
i = 0;
if_connected = False
try:
	urllib.request.urlopen("http://www.baidu.com")
	if_connected = True
except:
	if_connected = False
while not if_connected:
	i = i + 1
	print("未连接到互联网，等待重新尝试:当前是第" + str(i) + "次尝试")
	time.sleep(waitSeconds)
	try:
		urllib.request.urlopen("http://www.baidu.com")
		if_connected = True
	except:
		if_connected = False
	if i == times:
		print("长时间未联网，自动断开")
		exit()

content = urllib.request.urlopen(bing_url).read().decode('utf-8')
result = json.loads(content)
wallpaper_url = result['images'][0]['url']
print(wallpaper_url)
pic_name = wallpaper_url.split('/')[-1]
print(pic_name)
img_src = urllib.request.urlopen(wallpaper_url).read()
img_file = pic_folder + "/" + pic_name
if os.path.isfile(img_file):
 	print("文件已经存在")
 	balloon_tip("壁纸已经是最新了","最新的壁纸已经保存到您的图片目录下了，不必重新下载")
else:
	with open(img_file, 'wb') as f:
	        f.write(img_src)

	k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
	win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "0")
	win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
	win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, img_file, 1+2)

	balloon_tip("今日的壁纸已经更新",result['images'][0]['copyright'])

tryDownloadVideo(result)

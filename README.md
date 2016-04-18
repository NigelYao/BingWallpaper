# BingWallpaper
Download bing.com wallpaper or video every day and set as your desktop wallpaper, keep your desktop refresh.

Also, this script will download the today's bing video background to your home dir if there is any, you can check it out anytime.

# Start
You will need to have python 3 and pywin32 installed, May you need to change the location of the downloaded resources as your will:
```
pic_folder = "set-to-your-location"
video_folder = "set-to-your-location"
```

# Quick install
* For windows, open your command line as admin
* install Chocolatey with just one line [check out Chocolatey.org](https://chocolatey.org)
```
@powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))" && SET PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin
```
* Install python 3 with the fllowing line:
```
choco install python3
```
* Install pywin-32:
```
choco install pywin32
```
* Run the script, and there you go, with a little cute ballon tip, your wallpaper is already the latest Bing.com

# Extra
Add this script to your startup, keep your desktop up-to-date.

# Notice
Follow bing.com's wallpaper usage, all wallpaper copyright belongs to bing.com

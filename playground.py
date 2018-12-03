import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import colorsys
import matplotlib.widgets as widgets
import urllib,io
import requests
from ImageFilter import *

def onselect(eclick, erelease):
    if eclick.ydata>erelease.ydata:
        eclick.ydata,erelease.ydata=erelease.ydata,eclick.ydata
    if eclick.xdata>erelease.xdata:
        eclick.xdata,erelease.xdata=erelease.xdata,eclick.xdata
    ax.set_ylim(erelease.ydata,eclick.ydata)
    ax.set_xlim(eclick.xdata,erelease.xdata)
    fig.canvas.draw()

fig = plt.figure()
ax = fig.add_subplot(111)
url = "https://wx2.sinaimg.cn/mw1024/bfee4305gy1ftsx96j7rrj22lk2ao4qq.jpg"
img_filter = ImageFilter(url)
# gray2 = img_filter.original_img.convert('LA')
# gray2.save('greyscale.png')
# img2 = img_filter.HSVColor(img_filter.original_img)
# img2.save("HSV.png")
saturation_filtered_img = img_filter.filter_hsv('polarize')
# arr = np.asarray(saturation_filtered_img)

plt_image=plt.imshow(saturation_filtered_img)
# plt_image=plt.imshow(img2)

# rs=widgets.RectangleSelector(
#     ax, onselect, drawtype='box',
#     rectprops = dict(facecolor='red', edgecolor = 'black', alpha=0.5, fill=True))
plt.show()
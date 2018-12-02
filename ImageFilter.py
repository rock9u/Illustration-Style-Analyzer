import requests,io
from PIL import Image
import colorsys
class ImageFilter:
    def __init__(self,url):
        response = requests.get(url)
        self.original_img = Image.open(io.BytesIO(response.content))
        self.filtered = dict()
        self.FILTERS = {
            'saturation': self.sat_filter,
            'greyscale' : self.grey_filter,
            'value' : self.value_filter,
        }


    def filter_hsv(self,mode,im = None):
        if im == None: im = self.original_img
        filtered_im = im.copy()
        filtered_im = self.FILTERS[mode](im)
        # for x in range(im.size[0]):
        #     for y in range(im.size[1]):
        #         r,g,b = im.getpixel((x,y))
        #         #convert to hsv
        #         h,s,v=colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)
        #         #new image with hsv as para
        #         #print h,s,v
        #         if mode == 'saturation':
        #             r,g,b = colorsys.hsv_to_rgb(h,s,1-s)
        #         elif mode == 'greyscale':
        #             r,g,b = colorsys.hsv_to_rgb(0,0,0.299*r/255 + 0.587*g/255 + 0.114*b/255 )
        #         elif mode == 'value':
        #             r,g,b = colorsys.hsv_to_rgb(0,0,v)
        #         else:
        #             raise KeyError(mode)
        #         rgb = (int(r*255),int(g*255),int(b*255))
        #         if rgb:
        #             filtered_im.putpixel((x,y),(rgb))
        self.filtered[mode] = filtered_im
        return filtered_im

    def sat_filter(self,img):
        if isinstance(img,Image.Image):
            Hdat,Sdat,Vdat = img.convert('HSV').split()
            t = list(Sdat.getdata())
            Hdat.putdata(list(map(lambda x : 0,t)))
            Vdat.putdata(list(map(lambda x : (255-x),t)))
            return Image.merge('HSV',(Hdat,Sdat,Vdat))
        else:
            return None

    def grey_filter(self,img):
        if isinstance(img,Image.Image):
            r,g,b = img.convert('RGB').split()
            Hdat = []
            Sdat = []
            Vdat = [] 
            for rd,gn,bl in zip(r.getdata(),g.getdata(),b.getdata()) :
                Vdat.append(0.299*rd + 0.587*gn + 0.114*bl )
                Hdat.append(0)
                Sdat.append(0)
            r.putdata(Hdat)
            g.putdata(Sdat)
            b.putdata(Vdat)
            return  b
        else:
            return None

    def value_filter(self,img):
        if isinstance(img,Image.Image):
            Hdat,Sdat,Vdat = img.convert('HSV').split()
            t = list(Sdat.getdata())
            Hdat.putdata(list(map(lambda x : 0,t)))
            Vdat.putdata(list(map(lambda x : (255-x),t)))
            return Vdat
        else:
            return None

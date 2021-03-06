import requests,io
from PIL import Image
import colorsys
class ImageFilter:
    def __init__(self,url=None,image=None):
        self.original_img=None
        self.init_url(url)
        self.init_image(image)
        self.validate_image()
        self.filtered = dict()
        self.FILTERS = {
            'original' : self.get_original,
            'saturation': self.sat_filter,
            'greyscale' : self.grey_filter,
            'value' : self.value_filter,
            'polarize'  :self.polarize_filter,
        }

    def init_url(self,url):
        if url:
            response = requests.get(url)
            self.original_img = Image.open(io.BytesIO(response.content))

    def init_image(self,image):
        if image:
            self.original_img = image

    def validate_image(self):
        if self.original_img == None:
            raise ImageNotExist("Image is empty!")

    def filter_hsv(self,mode,im = None):
        if im == None: im = self.original_img
        filtered_im = im.copy()
        filtered_im = self.FILTERS[mode](im)
        self.filtered[mode] = filtered_im
        return filtered_im

    def get_original(self,*args, **kwargs):
        return self.original_img

    def sat_filter(self,img):
        if isinstance(img,Image.Image):
            h,s,v = img.convert('HSV').split()
            print(v)
            t = list(s.getdata())
            h.putdata(list(map(lambda x : 0,t)))
            v.putdata(list(map(lambda x : (255-x),t)))
            return Image.merge('HSV',(h,s,v))
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
            return Vdat
        else:
            return None

    def polarize_filter(self,img,resolution = 4):
        if isinstance(img,Image.Image):
            img = self.grey_filter(img)
            r,g,b = img.convert('RGB').split()
            Rdat = []
            Gdat = []
            Bdat = []
            window = 255/(resolution-1)
            for rd,gn,bl in zip(r.getdata(),g.getdata(),b.getdata()) :
            
 
                Rdat.append(int(window * round(float(rd)/window)))
                Gdat.append(int(window * round(float(gn)/window)))
                Bdat.append(int(window * round(float(bl)/window)))
            r.putdata(Rdat)
            g.putdata(Gdat)
            b.putdata(Bdat)
            return Image.merge('RGB',(r,g,b))
            
        else:
            return None

class ImageNotExist(Exception):
    def __init__(self, message):
        super().__init__(message)
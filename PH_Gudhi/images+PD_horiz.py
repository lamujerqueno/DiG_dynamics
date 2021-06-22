factor = 0.6 # Scaling factor: how many times the cropped picture is to be shrunk.
             # Needs to be at least h/500.0, where h is the height of the cropped image.
folder = 'Ivan_C'
suffix = '_ripser'
doinverted = False # set to False for _ripser

from os import chdir,mkdir
#from sys import argv
from numpy import loadtxt
from PIL import Image,ImageOps

#Combining persistence(i) and cropped(i) frames
#folder = argv[1]
chdir(folder)
try:
    mkdir('combined'+suffix)
    if doinverted:
        mkdir('combinedi'+suffix)
except:
    pass
param = loadtxt('param2.csv')
start,inc,end,h,w = map(int,param[:5])
for i in range(start,end+1,inc):
    fname = 'frame%.5d.png' % i
    im = Image.new('RGB', (1000+int((w-h)/factor),500), color='white')
    impers = Image.open('persistence'+suffix+'/'+fname)
    imcrop = Image.open('cropped/'+fname)
    imcrop0 = imcrop.resize((int(w/factor),int(h/factor)), resample=Image.LANCZOS)
    im.paste(impers, (500+int((w-h)/factor),0))
    im.paste(imcrop0, (250-int(h/(2*factor)),250-int(h/(2*factor))))
    im.save('combined'+suffix+'/'+fname)
    if doinverted:
        im = Image.new('RGB', (1000+int((w-h)/factor),500), color='white')
        impers = Image.open('persistencei'+suffix+'/'+fname)
        imcropi = ImageOps.invert(imcrop)
        imcrop0 = imcropi.resize((int(w/factor),int(h/factor)), resample=Image.LANCZOS)
        im.paste(impers, (500+int((w-h)/factor),0))
        im.paste(imcrop0, (250-int(h/(2*factor)),250-int(h/(2*factor))))
        im.save('combinedi'+suffix+'/'+fname)
    print i

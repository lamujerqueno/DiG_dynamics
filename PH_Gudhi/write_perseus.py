from checks import findSuffix,firstThingsToDo,progressBar
from numpy import array,concatenate,savetxt
from os import mkdir
from PIL import Image,ImageOps
from sys import argv
from warnings import warn

def writePerseus(method, normalised, inverted, numframes, left, right, top, bottom, normconst):
    suffix = findSuffix(method, normalised, inverted)
    foldername = 'perseus' + suffix
    try:
        mkdir(foldername)
    except OSError:
        warn('folder "%s" already exists: possibly rewriting data.' % foldername, RuntimeWarning)
    firstlines = array([2,right-left,bottom-top])
    cropping = array([left,right,top,bottom])
    savetxt(foldername+'/cropping.csv', cropping, fmt='%d')
    print('Writing Perseus files...')
    for i in range(numframes):
        img = Image.open('frames/frame%.5d.png' % i)
        img = img.crop((left,top,right,bottom))
        if inverted:
            img = ImageOps.invert(img)
            normC = 255-normconst
        else:
            normC = normconst
        imgdata = array(img.getdata())
        if normalised:
            imgdata = imgdata / normC
        with open('%s/frame%.5d.csv'%(foldername,i),'w') as f:
            savetxt(f, firstlines, fmt='%d')
            savetxt(f, imgdata, fmt='%.15f')
        img.close()
        progressBar(i+1,numframes)

if __name__=='__main__':
    method, normalised, inverted, param = firstThingsToDo(argv[0])
    #numframes, left, right, top, bottom, normconst = reCrop(param)
    numframes, left, right, top, bottom = map(int,param[:5])
    normconst = param[6]
    writePerseus(method, normalised, inverted, numframes, left, right, top, bottom, normconst)


from checks import firstThingsToDo,progressBar,tryCreatingFolder
from PIL import Image
from numpy import array,savetxt
from os import mkdir
from sys import argv
from warnings import warn

def croppingDialogue(left, right, top, bottom, twidth, theight):
    bounds = [left,right,top,bottom]
    boundstrs = ['left','right','top','bottom']
    maxbounds = [twidth,theight]
    maxboundstrs = ['width','height']
    for i in range(4):
        try:
            prompt = 'Enter the value for %s (default=%d' % (boundstrs[i],bounds[i])
            if i%2:
                prompt = '%s, use -1 for the %s' % (prompt,maxboundstrs[int(i/2)])
            bounds[i] = int(input(prompt+'): ').strip())
            if bounds[i] == -1 and i%2:
                bounds[i] = maxbounds[int(i/2)]
        except ValueError:
            pass
        print('%s has been set to %d.' % (boundstrs[i],bounds[i]))
    return tuple(bounds)

def reCrop(param):
    numframes,left,right,top,bottom = map(int,param[:5])
    img0 = Image.open('frames/frame00000.png')
    twidth,theight = img0.size
    img0.close()
    left,right,top,bottom = croppingDialogue(left,right,top,bottom,twidth,theight)
    parameters = '%d\n%d\n%d\n%d\n%d\n%.15f\n%.15f' % (numframes,left,right,top,bottom,param[5],param[6])
    with open('parameters.csv','w') as f:
        f.write(parameters)
    return (numframes, left, right, top, bottom)

def writeCroppedFrames(numframes, left, right, top, bottom):
    for suffix2 in ['','rgb']:
        foldername = 'cropped' + suffix2
        tryCreatingFolder(foldername)
        cropping = array([left,right,top,bottom])
        savetxt(foldername+'/cropping.csv', cropping, fmt='%d')
        print('Writing cropped images to the folder "%s"...' % foldername)
        for i in range(numframes):
            img = Image.open('frames%s/frame%.5d.png' % (suffix2,i))
            img = img.crop((left,top,right,bottom))
            img.save('cropped%s/frame%.5d.png' % (suffix2,i))
            progressBar(i+1,numframes)

if __name__=='__main__':
    method, normalised, inverted, param = firstThingsToDo(argv[0])
    numframes, left, right, top, bottom = reCrop(param)
    writeCroppedFrames(numframes, left, right, top, bottom)


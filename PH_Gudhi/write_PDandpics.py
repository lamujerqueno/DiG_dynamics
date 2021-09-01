from checks import findSuffix,firstThingsToDo,progressBar
from cv2 import imread,VideoWriter,VideoWriter_fourcc
from numpy import array,loadtxt,savetxt
from os import mkdir
from PIL import Image,ImageOps
from sys import argv

def combineDialogue():
    prompt = 'Placement of the video frame relative to persistence diagram (default=left)? [l/r/t/b]: '
    notice = 'Placement has been recorded as %s.'
    prompt2 = 'How much of the %s of the image should the video frame take up (default=%.3f)? '
    pdefault = 0.8
    hvval = input(prompt).strip().lower()
    if hvval=='l' or hvval=='left' or hvval=='':
        hv = 0
        print(notice % 'left')
    elif hvval=='r' or hvval=='right':
        hv = 1
        print(notice % 'right')
    elif hvval=='t' or hvval=='top':
        hv = 2
        print(notice % 'top')
    elif hvval=='b' or hvval=='bottom':
        hv = 3
        print(notice % 'bottom')
    else:
        hv = 0
        print('Unrecognised placement option, assuming "left".')
    if hv>1:
        pval = input(prompt2 % ('width',pdefault)).strip()
    else:
        pval = input(prompt2 % ('height',pdefault)).strip()
    try:
        prop = float(pval)
        if prop < 0:
            prop = 0.0
        if prop > 1:
            prop = 1.0
    except ValueError:
        prop = pdefault
    print('The value has been set to %.3f.' % prop)
    return (hv, prop)

def writeVideoFrames(suffix, inverted, numframes, left, right, top, bottom, lrtb, prop, dimPD=500):
    foldername = 'combined' + suffix
    try:
        mkdir(foldername)
    except OSError:
        warn('folder "%s" already exists: possibly rewriting data.' % foldername, RuntimeWarning)
    cropping = array([left,right,top,bottom])
    savetxt(foldername+'/cropping.csv', cropping, fmt='%d')
    wfr = right-left
    hfr = bottom-top
    indent = int((1-prop)*dimPD/2)
    if lrtb==0:
        wfr2 = int(prop*dimPD*wfr/hfr)
        hfr2 = int(prop*dimPD)
        imgdim = (dimPD+indent+wfr2, dimPD)
        cornerPD = (indent+wfr2, 0)
        cornerFr = (indent, indent)
    elif lrtb==1:
        wfr2 = int(prop*dimPD*wfr/hfr)
        hfr2 = int(prop*dimPD)
        imgdim = (dimPD+indent+wfr2, dimPD)
        cornerPD = (0, 0)
        cornerFr = (dimPD, indent)
    elif lrtb==2:
        wfr2 = int(prop*dimPD)
        hfr2 = int(prop*dimPD*hfr/wfr)
        imgdim = (dimPD, dimPD+indent+hfr2)
        cornerPD = (0, indent+hfr2)
        cornerFr = (indent, indent)
    else:
        wfr2 = int(prop*dimPD)
        hfr2 = int(prop*dimPD*hfr/wfr)
        imgdim = (dimPD, dimPD+indent+hfr2)
        cornerPD = (0, 0)
        cornerFr = (indent, dimPD)
    print('The dimensions of the video will be %dx%d.' % imgdim)
    print('Writing frames for the video...')
    for i in range(numframes):
        img = Image.new('RGB', imgdim, color='white')
        imgPD = Image.open('persistence%s/frame%.5d.png' % (suffix,i))
        imgFr = Image.open('frames/frame%.5d.png' % i)
        imgFr = imgFr.crop((left,top,right,bottom))
        if inverted:
            imgFr = ImageOps.invert(imgFr)
        imgFr = imgFr.resize((wfr2,hfr2), resample=Image.LANCZOS)
        img.paste(imgPD, cornerPD)
        img.paste(imgFr, cornerFr)
        img.save('%s/frame%.5d.png' % (foldername,i))
        img.close()
        imgPD.close()
        imgFr.close()
        progressBar(i+1,numframes)
    return imgdim

def writeVideo(suffix, numframes, imgdim, framerate):
    out = VideoWriter('movie%s.mp4' % suffix, VideoWriter_fourcc(*'MP4V'), framerate, imgdim)
    print('Writing the video...')
    for i in range(numframes):
        img = imread('combined%s/frame%.5d.png' % (suffix,i))
        out.write(img)
        img.close()
        progressBar(i+1,numframes)
    out.release()

if __name__=='__main__':
    method, normalised, inverted, param = firstThingsToDo(argv[0])
    suffix = findSuffix(method, normalised, inverted)
    numframes,left,right,top,bottom = map(int,param[:5])
    framerate = param[5]
    lrtb,prop = combineDialogue()
    imgdim = writeVideoFrames(suffix, inverted, numframes, left, right, top, bottom, lrtb, prop)
    writeVideo(suffix, numframes, imgdim, framerate)

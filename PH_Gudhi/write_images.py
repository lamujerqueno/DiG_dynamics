from checks import progressBar,readSettings,tryCreatingFolder
from cv2 import CAP_PROP_FPS,CAP_PROP_FRAME_COUNT,destroyAllWindows,VideoCapture
from PIL import Image
from numpy import array,average,size
from os import chdir,listdir,mkdir,path,rename
from sys import argv
from warnings import warn

def writeFrames(inputsource, videoimage, folder, method):
    for foldername in ['framesrgb','frames']:
        tryCreatingFolder(foldername)
    if inputsource:
        frdefault = 10.0
        frstr = input('Nominal frame rate (default=%.3f fps): ' % frdefault).strip()
        try:
            framerate = float(frstr)
            if framerate <= 0:
                raise ValueError
        except ValueError:
            framerate = frdefault
        print('The frame rate has been set to %.3f.' % framerate)
        imagefolder = videoimage
        files = sorted([f for f in listdir(imagefolder) if f.endswith('.png') or f.endswith('.jpg')])
        numframes = len(files)
        if imagefolder[3:] == folder:
            try:
                mkdir('source')
            except OSError:
                pass
            for f in files:
                rename(f, 'source/'+f)
            imagefolder = 'source'
        print('Copying the frames...')
        for i,f in enumerate(files):
            # copyfile from shutil: fast but might cause problems in the analysis
            #copyfile('%s/%s'%(imagefolder,f), 'framesrgb/frame%.5d.png'%i)
            # Slower but safer:
            img = Image.open('%s/%s'%(imagefolder,f)).convert('RGB')
            img.save('framesrgb/frame%.5d.png' % i)
            img.close()
            progressBar(i+1,numframes)
    else:
        vid = VideoCapture(videoimage)
        if not vid.isOpened():
            raise ValueError('the file %s cannot be opened!' % videoimage[3:])
        i = 0
        # Needs OpenCV 3.0 or later
        framerate = vid.get(CAP_PROP_FPS)
        numframes = int(vid.get(CAP_PROP_FRAME_COUNT))
        print('Writing the frames of the video...')
        while vid.isOpened():
            ret,frame = vid.read()
            if ret:
                # Warning: OpenCV returns the channels in BGR order.
                img = Image.fromarray(frame[:,:,::-1], 'RGB')
                img.save('framesrgb/frame%.5d.png' % i)
                img.close()
                i += 1
                progressBar(i,numframes)
            else:
                break
        vid.release()
        destroyAllWindows()
    avgpix = []
    width,height = 0,0
    print('Converting to monochrome...')
    for i in range(numframes):
        img = Image.open('framesrgb/frame%.5d.png' % i)
        if i == 0:
           width,height = img.size
        if method:
            imgbw = img.split()[method-1]
        else:
            imgbw = img.convert('L')
        imgbw.save('frames/frame%.5d.png' % i)
        pixels = array(imgbw.getdata())
        avgpix.append(average(pixels))
        img.close()
        imgbw.close()
        progressBar(i+1,numframes)
    normconst = max(avgpix)
    return numframes, width, height, framerate, normconst

if __name__=='__main__':
    print(' - '+argv[0])
    inputsource, video, images, topfolder, folder, method, normalised, inverted, extrafolders = readSettings()
    chdir(topfolder)
    try:
        mkdir(folder)
    except OSError:
        pass
    chdir(folder)
    myinput = (images if inputsource else video)
    numframes, width, height, framerate, normconst = writeFrames(inputsource, '../'+myinput, folder, method)
    if not path.isfile('parameters.csv'):
        parameters = '%d\n0\n%d\n0\n%d\n%.15f\n%.15f' % (numframes,width,height,framerate,normconst)
        with open('parameters.csv','w') as f:
            f.write(parameters)


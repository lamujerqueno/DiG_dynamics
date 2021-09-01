from checks import firstThingsToDo,progressBar
from norm_pictures import normPicsDialogue
from numpy import array,linalg,savetxt,zeros
from PIL import Image,ImageChops
from sys import argv
#from write_perseus import reCrop

def distPicsDialogue(numframes, left, right, top, bottom, filename):
    startval = input('The first frame to consider (default=0): ').strip()
    try:
        start = int(startval)
        if start < 0 or start >= numframes:
            raise ValueError
    except ValueError:
        start = 0
    print('The frame has been set to %d.' % start)
    endval = input('The first frame NOT to consider (default=%d, i.e. the end of the video): ' % numframes).strip()
    try:
        end = int(endval)
        if end <= 0 or end > numframes:
            raise ValueError
    except ValueError:
        end = numframes
    print('The frame has been set to %d.' % end)
    incval = input('Frame increment (default=1): ').strip()
    try:
        inc = int(incval)
        if inc <= 0:
            raise ValueError
    except ValueError:
        inc = 1
    print('The increment has been set to %d.' % inc)
    with open(filename+'_README.txt','w') as f:
        readme = 'Start frame: %d.\nEnd frame: %d.\nFrame increment: %d.\nCropping: left %d, right %d, top %d, bottom %d.'
        f.write(readme % (start,end,inc,left,right,top,bottom))
    return (start, end, inc)

def distPics(rgb, p, start, end, inc, left, right, top, bottom, normconst, suffix2, filename):
    indices = range(start, end, inc)
    nfiles = len(indices)
    imgs = []
    print('Reading images...')
    for ii,i in enumerate(indices):
        img = Image.open('frames%s/frame%.5d.png' % (suffix2,i))
        img = img.crop((left,top,right,bottom))
        imgdata = array(img.getdata()).flatten() / normconst
        imgs.append(imgdata)
        img.close()
        progressBar(ii+1,nfiles)
    dist = zeros((nfiles,nfiles))
    npairs = int(nfiles*(nfiles-1)/2)
    k = 0
    print('Computing distances...')
    for ii,i in enumerate(indices):
        for jj,j in enumerate(indices[:ii]):
            diff = imgs[ii]-imgs[jj]
            if p:
                d = linalg.norm(diff, ord=p)
            else:
                d = linalg.norm(diff, ord=float('inf'))
            dist[ii,jj] = d
            dist[jj,ii] = d
            k += 1
            progressBar(k,npairs)
    savetxt(filename+'.csv', dist, fmt='%.15f', delimiter=',')

if __name__=='__main__':
    method, normalised, inverted, param = firstThingsToDo(argv[0])
    rgb, p = normPicsDialogue('distance')
    suffix2 = ('rgb' if rgb else '')
    filename = 'dist%d_frames%s' % (p,suffix2)
    #numframes, left, right, top, bottom, normconst = reCrop(param)
    left, right, top, bottom = map(int,param[1:5])
    start, end, inc = distPicsDialogue(numframes, left, right, top, bottom, filename)
    if normalised:
        newnormconst = param[6]
    else:
        newnormconst = 1.0
    distPics(rgb, p, start, end, inc, left, right, top, bottom, newnormconst, suffix2, filename)

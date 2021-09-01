from checks import firstThingsToDo,progressBar
from dist_pictures import distPicsDialogue
from norm_gradient import gradientDialogue
from norm_pictures import normPicsDialogue
from numpy import array,asarray,gradient,linalg,savetxt,zeros
from PIL import Image,ImageChops
from sys import argv
#from write_perseus import reCrop

def distGradient(rgb, p, step, start, end, inc, left, right, top, bottom, normconst, suffix2, filename):
    indices = range(start, end, inc)
    nfiles = len(indices)
    imgs = []
    print('Reading images and computing gradients...')
    for ii,i in enumerate(indices):
        img = Image.open('frames%s/frame%.5d.png' % (suffix2,i))
        img = img.crop((left,top,right,bottom))
        imgdata = asarray(img).astype(float)
        grad = array(gradient(imgdata, step, axis=(0,1))).flatten() / normconst
        imgs.append(grad)
        img.close()
        progressBar(ii+1,nfiles)
    dist = zeros((nfiles,nfiles))
    npairs = int(nfiles*(nfiles-1)/2)
    k = 0
    print('Computing distances of the gradients...')
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
    rgb, p = normPicsDialogue('gradient-distance')
    step = gradientDialogue()
    suffix2 = ('rgb' if rgb else '')
    filename = 'distGradient%d_step%.3f_frames%s' % (p,step,suffix2)
    #numframes, left, right, top, bottom, normconst = reCrop(param)
    numframes, left, right, top, bottom = map(int,param[:5])
    start, end, inc = distPicsDialogue(numframes, left, right, top, bottom, filename)
    if normalised:
        newnormconst = param[6]
    else:
        newnormconst = 1.0
    distGradient(rgb, p, step, start, end, inc, left, right, top, bottom, newnormconst, suffix2, filename)

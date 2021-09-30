from checks import firstThingsToDo,progressBar
from numpy import array,linalg,savetxt,zeros
from PIL import Image
from sys import argv
from crop_images import reCrop

def normPicsDialogue(nd):
    rgbval = input('Compute the %s of RGB pictures (default=0, enter 0 for greyscale and 1 for RGB)? '%nd).strip()
    try:
        rgb = int(rgbval)
        if rgb>1 or rgb<0:
            raise ValueError
    except ValueError:
        rgb = 0
    print('The choice has been recorded as %d.' % rgb)
    pval = input('Enter the value of p for the computation of p-%s (default=1, enter 0 for infinity): '%nd).strip()
    try:
        p = int(pval)
        if p<0:
            raise ValueError
    except ValueError:
        p = 1
    if p:
        print('p has been set to %d.' % p)
    else:
        print('p has been set to infinity.')
    return (rgb, p)

def normPics(numframes, rgb, p, left, right, top, bottom, normconst):
    suffix2 = ('rgb' if rgb else '')
    filename = 'norm%d_frames%s' % (p,suffix2)
    with open(filename+'_README.txt','w') as f:
        readme = 'Cropping: left %d, right %d, top %d, bottom %d.'
        f.write(readme % (left,right,top,bottom))
    norms = zeros(numframes)
    print('Computing norms...')
    for i in range(numframes):
        img = Image.open('frames%s/frame%.5d.png' % (suffix2,i))
        img = img.crop((left,top,right,bottom))
        imgdata = array(img.getdata()).flatten()
        if p:
            norms[i] = linalg.norm(imgdata, ord=p) / normconst
        else:
            norms[i] = linalg.norm(imgdata, ord=float('inf')) / normconst
        img.close()
        progressBar(i+1,numframes)
    savetxt(filename+'.csv', norms, fmt='%.15f', delimiter=',')

if __name__=='__main__':
    method, normalised, inverted, param = firstThingsToDo(argv[0])
    rgb, p = normPicsDialogue('norm')
    numframes, left, right, top, bottom = reCrop(param)
    left, right, top, bottom = map(int,param[1:5])
    if normalised:
        newnormconst = param[6]
    else:
        newnormconst = 1.0
    normPics(numframes, rgb, p, left, right, top, bottom, newnormconst)

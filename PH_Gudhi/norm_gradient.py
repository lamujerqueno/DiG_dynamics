from checks import firstThingsToDo,progressBar
from norm_pictures import normPicsDialogue
from numpy import array,asarray,gradient,linalg,savetxt,zeros
from PIL import Image
from sys import argv
#from write_perseus import reCrop

def gradientDialogue():
    stepval = input('Enter step for the calculation of gradient (default=1.000): ').strip()
    try:
        step = float(stepval)
        if step <= 0:
            raise ValueError
    except ValueError:
        step = 1.0
    print('The step has been set to %.3f.' % step)
    return step

def normGradient(numframes, rgb, p, step, left, right, top, bottom, normconst):
    suffix2 = ('rgb' if rgb else '')
    filename = 'normGradient%d_step%.3f_frames%s' % (p,step,suffix2)
    with open(filename+'_README.txt','w') as f:
        readme = 'Cropping: left %d, right %d, top %d, bottom %d.'
        f.write(readme % (left,right,top,bottom))
    norms = zeros(numframes)
    print('Computing norms of the gradients...')
    for i in range(numframes):
        img = Image.open('frames%s/frame%.5d.png' % (suffix2,i))
        img = img.crop((left,top,right,bottom))
        imgdata = asarray(img).astype(float)
        grad = array(gradient(imgdata, step, axis=(0,1))).flatten()
        if p:
            norms[i] = linalg.norm(grad, ord=p) / normconst
        else:
            norms[i] = linalg.norm(grad, ord=float('inf')) / normconst
        img.close()
        progressBar(i+1,numframes)
    savetxt(filename+'.csv', norms, fmt='%.15f', delimiter=',')

if __name__=='__main__':
    method, normalised, inverted, param = firstThingsToDo(argv[0])
    rgb, p = normPicsDialogue('gradient-norm')
    step = gradientDialogue()
    #numframes, left, right, top, bottom, normconst = reCrop(param)
    numframes, left, right, top, bottom = map(int,param[:5])
    if normalised:
        newnormconst = param[6]
    else:
        newnormconst = 1.0
    normGradient(numframes, rgb, p, step, left, right, top, bottom, newnormconst)

from checks import findSuffix,firstThingsToDo,progressBar
from numpy import loadtxt,zeros,savetxt
from sys import argv

def normDialogue():
    dval = input('Enter the dimension of persistence to compute the norm (default=1): ').strip()
    try:
        d = int(dval)
        if d>1 or d<0:
            raise ValueError
    except ValueError:
        d = 1
    print('Dimension has been set to %d.' % d)
    pval = input('Enter the value of p for the computation of p-norm (default=1, enter 0 for infinity): ').strip()
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
    return (d, p)

def normPH(method, normalised, inverted, numframes, left, right, top, bottom, d, p):
    suffix = findSuffix(method, normalised, inverted)
    filename = 'norm%d_ph%d%s' % (p,d,suffix)
    with open(filename+'_README.txt','w') as f:
        readme = 'Cropping: left %d, right %d, top %d, bottom %d.'
        f.write(readme % (left,right,top,bottom))
    norms = zeros(numframes)
    print('Computing norms...')
    for i in range(numframes):
        ints = loadtxt('ph%d%s/frame%.5d.csv'%(d,suffix,i), delimiter=',')
        intlen = ints[:,1] - ints[:,0]
        intlen = intlen[intlen<float('inf')]
        if p:
            ssum = sum(intlen**p)
            norms[i] = ssum**(1/p)
        else:
            norms[i] = max(intlen)
        progressBar(i+1,numframes)
    savetxt(filename+'.csv', norms, fmt='%.15f', delimiter=',')

if __name__=='__main__':
    method, normalised, inverted, param = firstThingsToDo(argv[0])
    numframes, left, right, top, bottom = map(int,param[:5])
    d, p = normDialogue()
    normPH(method, normalised, inverted, numframes, left, right, top, bottom, d, p)


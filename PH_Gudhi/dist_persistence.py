from checks import findSuffix,firstThingsToDo,progressBar
from dist_pictures import distPicsDialogue
import gudhi
from gudhi import wasserstein
from multiprocessing import Pool
from numpy import loadtxt,savetxt,zeros
from sys import argv

def distBottle(dargs):
    pdi,pdj,pext,pint = dargs
    d = gudhi.bottleneck_distance(pdi, pdj)
    return d

def distWasser(dargs):
    pdi,pdj,pext,pint = dargs
    d = wasserstein.wasserstein_distance(pdi, pdj, order=pext, internal_p=pint)
    return d

def distDialogue():
    dval = input('Enter the dimension of persistence to compute the norm (default=1): ').strip()
    try:
        d = int(dval)
        if d>1 or d<0:
            raise ValueError
    except ValueError:
        d = 1
    print('Dimension has been set to %d.' % d)
    distval = input('Compute bottleneck or Wasserstein distance? Enter 0 for bottleneck, 1 (default) for Wasserstein: ').strip()
    try:
        dist = int(distval)
        if dist>1 or dist<0:
            raise ValueError
    except ValueError:
        dist = 1
    print('Computing %s distance.' % ('Wasserstein' if dist else 'bottleneck'))
    if dist:
        pextval = input('External (matching) parameter q (default=2): ').strip()
        try:
            pext = int(pextval)
            if pext<0:
                raise ValueError
        except ValueError:
            pext = 2
        print('q has been set to %d.' % pext)
        pintval = input('Internal (R^2) parameter p (default=2, enter 0 for infinity): ').strip()
        try:
            pint = int(pintval)
            if pint<0:
                raise ValueError
        except ValueError:
            pint = 2
        if pint:
            print('p has been set to %d.' % pint)
        else:
            print('p has been set to infinity.')
    else:
        pint,pext = 0,0
    thrval = input('Maximum number of threads to use for multi-process computation (default=16): ').strip()
    try:
        thr = int(thrval)
        if thr<0:
            raise ValueError
    except ValueError:
        thr = 16
    print('The number of threads has been set to %d.' % thr)
    return (d, dist, pint, pext, thr)

def distPH(d, dist, pint, pext, maxthreads, start, end, inc, suffix, filename):
    indices = range(start, end, inc)
    nfiles = len(indices)
    pds = []
    print('Reading persistence diagrams...')
    for ii,i in enumerate(indices):
        ints = loadtxt('ph%d%s/frame%.5d.csv'%(d,suffix,i), delimiter=',')
        pds.append(ints)
        progressBar(ii+1,nfiles)
    indlist = [(i,j) for i in range(nfiles) for j in range(i)]
    pint0 = (pint if pint else float('inf'))
    args = [(pds[i],pds[j],pext,pint0) for i,j in indlist]
    distfn = (distWasser if dist else distBottle)
    pool = Pool(processes=maxthreads)
    dist = zeros((nfiles,nfiles))
    npairs = int(nfiles*(nfiles-1)/2)
    print('Computing distances...')
    for k,dij in enumerate(pool.imap(distfn,args)):
        i,j = indlist[k]
        dist[i,j] = dij
        dist[j,i] = dij
        progressBar(k+1,npairs)
    savetxt(filename+'.csv', dist, fmt='%.15f', delimiter=',')

if __name__=='__main__':
    method, normalised, inverted, param = firstThingsToDo(argv[0])
    numframes, left, right, top, bottom = map(int,param[:5])
    d, dist, pint, pext, maxthreads = distDialogue()
    suffix = findSuffix(method, normalised, inverted)
    filename = 'dist%d-%d_ph%d%s' % (pext,pint,d,suffix)
    start, end, inc = distPicsDialogue(numframes, left, right, top, bottom, filename)
    distPH(d, dist, pint, pext, maxthreads, start, end, inc, suffix, filename)

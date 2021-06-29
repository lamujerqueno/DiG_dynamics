folders = ['suppl_movie8v2']
distfile = 'suppl_movie8v2/dist' # output to the file distfile+('Bottleneck' or 'Wasserstein'+p)+'_ph'+homology+'.csv'
homology = '1n' # the code reads files from the folders 'ph'+homology (created with write_peristence.py)
                # homology must be one of '0', '0i', '0n', '0ni', '1', '1i', '1n', '1ni'
method = 1 # the distance to compute
           # method=0: bottelneck distance
           # method>0: Wasserstein distance with parameter p=method
maxThreads = 16 # number of threads to use

from os import chdir
from numpy import loadtxt,zeros,savetxt
import gudhi
from gudhi import wasserstein
from multiprocessing import Pool

# Function to compute a bottleneck distance (for multithreading)
def distBottle(dargs):
    pdi,pdj,i,j,param = dargs
    d = gudhi.bottleneck_distance(pdi, pdj)
    print(i,j)
    return d

# Function to compute a Wasserstein distance (for multithreading)
def distWasser(dargs):
    pdi,pdj,i,j,param = dargs
    d = wasserstein.wasserstein_distance(pdi, pdj, order=param)
    print(i,j)
    return d

if __name__=='__main__':
    
    chdir('../Experiments')
    filename = distfile
    if method:
        filename += 'Wasserstein'+str(method)
    else:
        filename += 'Bottleneck'
    filename += '_ph'+homology

    #Reading params
    sei = {}
    for folder in folders:
        chdir(folder)
        param = loadtxt('parameters.csv')
        start,inc,end = map(int,param[:3]) # inc = increment in frame number
        sei[folder] = [start,end+1,inc]
        chdir('..')

    #Write README
    fileinc = [0]
    nfiles = 0
    for folder in folders:
        nfiles += len(range(*sei[folder]))
        fileinc.append(nfiles)
    f = open(filename+'_README.txt','w')
    for ii,folder in enumerate(folders):
        f.write('%s: points %d to %d.\n' % (folder,fileinc[ii]+1,fileinc[ii+1]))
    f.close()

    #Read persistence intervals from the files
    intervals=[]
    for folder in folders:
        chdir(folder)
        for i in range(*sei[folder]):
            fname = 'frame%.5d.csv' % i
            p = loadtxt('ph'+homology+'/'+fname, delimiter=',')
            intervals.append(p)
            print('Reading files:',folder,i)
        chdir('..')

    #Computing and saving the distance matrices
    print('Total points:',nfiles)
    args = [(intervals[i],intervals[i2],i,i2,method) for i in range(nfiles) for i2 in range(i+1,nfiles)]
    pool = Pool(processes=maxThreads)
    if method:
        distances = pool.map(distWasser,args)
    else:
        distances = pool.map(distBottle,args)
    c = 0
    dist = zeros((nfiles,nfiles))
    for i in range(nfiles):
        for i2 in range(i+1,nfiles):
            dist[i,i2] = distances[c]
            dist[i2,i] = distances[c]
            c += 1
    savetxt(filename+'.csv', dist, fmt='%.15f', delimiter=',')

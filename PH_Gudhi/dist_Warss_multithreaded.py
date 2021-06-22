folders=['6chbt06c','6chbt06h'] # avoid nesting: no '/' in folder names
distfile = 'distWasserstein1_06' # for output
homology = ['1n'] 
suffix = ''
#homology = ['1','0','1i','0i'] 
#suffix = '_ripser_thr1' # compute distance matrices for folders ph(j)(suffix) for j in homology
                   # so e.g. if homology = ['1'] and suffix = '_ripser' then we take the folder 'ph1_ripser'
                   #         if homology = ['0i','1i'] and suffix = '' then we take the folders 'ph0i' and 'ph1i'

from os import chdir
from numpy import loadtxt,zeros,savetxt
import gudhi
from gudhi import wasserstein
from multiprocessing import Pool
import time
tolerance = 1e-6
maxThreads = 16

# Function to compute a bottleneck distance (for multithreading)
def distBottle(dargs):
    pdi,pdj,i,j = dargs
    d = gudhi.bottleneck_distance(pdi, pdj, tolerance)
    print(i,j)
    return d

def distWasser(dargs):
    pdi,pdj,i,j = dargs
    d = wasserstein.wasserstein_distance(pdi, pdj, order=1.0)
    print(i,j)
    return d

if __name__=='__main__':
    
    chdir('..')

    #Reading params
    sei = {}
    for folder in folders:
        chdir(folder)
        param = loadtxt('param2.csv')
        start,inc,end = map(int,param[:3]) # inc = increment in frame number
        sei[folder] = [start,end+1,inc]
        chdir('..')

    #Write README
    fileinc = [0]
    nfiles = 0
    for folder in folders:
        nfiles += len(range(*sei[folder]))
        fileinc.append(nfiles)
    f = open(distfile+'_README.txt','w')
    for ii,folder in enumerate(folders):
        f.write('%s: points %d to %d.\n' % (folder,fileinc[ii]+1,fileinc[ii+1]))
    f.close()

    for j in homology:

        #Read persistence intervals from the files
        intervals=[]
        for folder in folders:
            chdir(folder)
            for i in range(*sei[folder]):
                fname = 'frame%.5d.csv' % i
                p = loadtxt('ph'+j+suffix+'/'+fname, delimiter=',')
                intervals.append(p)
                print(folder, i)
            chdir('..')

        #Computing and saving the distance matrices
        print('Total points:',nfiles)
        args = [(intervals[i],intervals[i2],i,i2) for i in range(nfiles) for i2 in range(i+1,nfiles)]
        pool = Pool(processes=maxThreads)
        distances = pool.map(distWasser,args)
        c = 0
        dist = zeros((nfiles,nfiles))
        for i in range(nfiles):
            for i2 in range(i+1,nfiles):
                dist[i,i2] = distances[c]
                dist[i2,i] = distances[c]
                c += 1
        savetxt(distfile+'_H'+j+suffix+'.csv', dist, fmt='%.15f', delimiter=',')

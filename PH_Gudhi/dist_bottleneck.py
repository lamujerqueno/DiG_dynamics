folders=['6chbt06c','6chbt06h']
distfile = 'dist_bottleneck_06c_06h'
homology = ['ph1n']

from os import chdir
from numpy import loadtxt,zeros,savetxt
import gudhi
tolerance = 1e-6

#Reading params
sei = {}
renorm = {}
chdir('..')
for folder in folders:
    chdir(folder)
    param = loadtxt('param2.csv')
    start,inc,end = map(int,param[:3])
    sei[folder] = [start,end+1,inc]
    renorm[folder] = float(param[5])
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

# Computations
for ph in homology:
    
    #Read persistence intervals from the files
    intervals=[]
    for folder in folders:
        chdir(folder)
        for i in range(*sei[folder]):
            fname = 'frame%.5d.csv' % i
            p = loadtxt(ph+'/'+fname, delimiter=',') 
            intervals.append(p)
            print folder, i
        chdir('..')

    #Computing and saving the distance matrix
    print 'Total points:', nfiles
    dist = zeros((nfiles,nfiles))
    for i in range(nfiles):
        for j in range(i+1,nfiles):
            d = gudhi.bottleneck_distance(intervals[i], intervals[j], tolerance)
            dist[i,j] = d
            dist[j,i] = d
            print i,j,d
    savetxt(distfile+'_'+ph+'.csv', dist, fmt='%.15f', delimiter=',')
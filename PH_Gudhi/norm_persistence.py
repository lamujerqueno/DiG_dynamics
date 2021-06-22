from os import chdir
from sys import argv
from numpy import loadtxt,zeros,savetxt,log

#folder = argv[1]
folder = 'ivan_test1'

#Reading params
chdir(folder)
param = loadtxt('param2.csv')
start,inc,end = map(int,param[:3])
#inc=1
#start,inc,end=1,1,10
birththreshold=100 # default 255
p = 1
computeEntropy = False

#Read images
files = range(start,end+1,inc)
nfiles = len(files)
#homology = ['ph0','ph0i','ph1','ph1i']
homology = ['ph1']
#homology = ['ph0_ripser_thr1','ph1_ripser_thr1']
lh = len(homology)
dist = zeros((nfiles,lh))
entropy = zeros((nfiles,lh))
for ii,i in enumerate(files):
    fname = 'frame%.5d.csv' % i
    for jj,j in enumerate(homology):
        pp = loadtxt(j+'/'+fname, delimiter=',')
        plen = pp[:,1]-pp[:,0]
        if plen[0]==float('inf'):
            plen=plen[1:]
        plen = plen[pp[:,0]<=birththreshold]
        ppp = plen**p
        d = sum(plen)**(1./p)
        dist[ii,jj] = d
        if computeEntropy:
            sd = sum(plen)
            plnorm = plen/sd
            summands = plnorm*log(plnorm)
            ed = -sum(summands)/log(sd)
            entropy[ii,jj] = ed
    print i

foldersplit = folder.split('/')
innerfolder = foldersplit[-1]
for jj,j in enumerate(homology):
    savetxt('norm'+str(p)+'_birthleq100_'+j+'_'+innerfolder+'.csv',dist[:,jj],fmt='%.15f',delimiter=',')
    if computeEntropy:
        savetxt('entropy_'+j+'_'+innerfolder+'.csv',entropy[:,jj],fmt='%.15f',delimiter=',')

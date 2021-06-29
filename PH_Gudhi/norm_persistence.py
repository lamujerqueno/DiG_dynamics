folder = 'suppl_movie8v2'
suffix = 'n' # the code reads files from the folder 'ph0'+suffix and 'ph1'+suffix (created with write_peristence.py)
             # suffix must be one of '', 'i', 'n', 'ni'
from os import chdir
from numpy import loadtxt,zeros,savetxt

#Reading params
chdir('../Experiments/'+folder)
param = loadtxt('parameters.csv')
start,inc,end = map(int,param[:3])
p = 1

#Read images
files = range(start,end+1,inc)
nfiles = len(files)
dist = zeros((nfiles,2))
for ii,i in enumerate(files):
    fname = 'frame%.5d.csv' % i
    for dim in ['0','1']:
        pp = loadtxt('ph'+dim+suffix+'/'+fname, delimiter=',')
        plen = pp[:,1]-pp[:,0]
        if plen[0]==float('inf'):
            plen=plen[1:]
        ppp = plen**p
        d = sum(ppp)**(1./p)
        dist[ii,int(dim)] = d
    print(i)

for dim in ['0','1']:
    savetxt('norm'+str(p)+'_ph'+dim+suffix+'_'+folder+'.csv',dist[:,int(dim)],fmt='%.15f',delimiter=',')
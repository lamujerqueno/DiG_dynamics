folder = 'suppl_movie8v2'
suffix = 'n' # the code reads files from the folder 'ph0'+suffix and 'ph1'+suffix (created with write_peristence.py)
             # suffix must be one of '', 'i', 'n', 'ni'
from os import chdir,mkdir
from numpy import loadtxt
from matplotlib import pyplot

#Persistence diagrams
chdir('../Experiments/'+folder)
try:
    mkdir('persistence'+suffix)
except:
    pass
param = loadtxt('parameters.csv')
start,inc,end,height,width,affI = map(int,param)
bdmin,bdmax = -10.0,265.0
if suffix=='n' or suffix=='ni':
    bdmin /= affI
    bdmax /= affI
for i in range(start,end+1,inc):
    fname = 'frame%.5d' % i
    p0 = loadtxt('ph0'+suffix+'/'+fname+'.csv', delimiter=',')
    p1 = loadtxt('ph1'+suffix+'/'+fname+'.csv', delimiter=',')
    fig = pyplot.figure(figsize=(5,5))
    ax = fig.add_subplot(111)
    ax.plot([bdmin,bdmax],[bdmin,bdmax],c='k',linewidth=0.5,zorder=1)
    ax.scatter(p0[:,0],p0[:,1],s=10,c='r',alpha=0.4,zorder=3)
    ax.scatter(p1[:,0],p1[:,1],s=10,c='b',alpha=0.4,zorder=2)
    ax.set_xlim((bdmin,bdmax))
    ax.set_ylim((bdmin,bdmax))
    ax.set_xlabel('birth')
    ax.set_ylabel('death')
    figname = 'persistence' + suffix + '/' + fname + '.png'
    pyplot.savefig(figname)
    pyplot.close(fig)
    print(i)

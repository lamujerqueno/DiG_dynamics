folder = 'Nina_experiments/5cb_h05rate_25per'
from os import chdir,mkdir
from numpy import zeros,savetxt,loadtxt,array
from matplotlib import pyplot

#Persistence diagrams
chdir(folder)
#homology = ['','i','n','ni'] # use '_ripser' for ripser
#homology = ['_ripser'] # use for ripser
homology = ['','i']
for i in homology:
    try:
        mkdir('persistence'+i)
    except:
        pass
#param = loadtxt('param2.csv')
#start,inc,end = map(int,param[:3])
start,inc,end = 1,1,10
#const = float(param[5])
#bdmaxes = [270,270,270/const,270/const] # maximum value of births/deaths to be displayed; should be one number for each string in homology variable.
bdmaxes = [270,270]
for i in range(start,end+1,inc):
    fname = 'frame%.5d' % i
    for j,bdmax in zip(homology,bdmaxes):
        p0 = loadtxt('ph0'+j+'/'+fname+'.csv', delimiter=',')
        p1 = loadtxt('ph1'+j+'/'+fname+'.csv', delimiter=',')
        fig = pyplot.figure(figsize=(5,5))
        ax = fig.add_subplot(111)
        ax.plot([0,bdmax],[0,bdmax],c='k',linewidth=0.5,zorder=1)
        ax.scatter(p0[:,0],p0[:,1],s=10,c='r',alpha=0.4,zorder=3)
        ax.scatter(p1[:,0],p1[:,1],s=10,c='b',alpha=0.4,zorder=2)
        ax.set_xlim((0,bdmax))
        ax.set_ylim((0,bdmax))
        ax.set_xlabel('birth')
        ax.set_ylabel('death')
        figname = 'persistence' + j + '/' + fname + '.png'
        pyplot.savefig(figname)
        pyplot.close(fig)
    print i

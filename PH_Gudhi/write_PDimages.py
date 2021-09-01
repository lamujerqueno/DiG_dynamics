from checks import findSuffix,firstThingsToDo,progressBar
from matplotlib import pyplot
from numpy import array,loadtxt,savetxt
from os import mkdir
from sys import argv
from warnings import warn

def PDpicDialogue(newbdmin, newbdmax):
    minval = input('Enter minimum birth/death to display (default=%.3f): ' % newbdmin).strip()
    try:
        bdmin = float(minval)
    except ValueError:
        bdmin = newbdmin
    print('Minimum birth/death has been set to %.3f.' % bdmin)
    maxval = input('Enter maximum birth/death to display (default=%.3f): ' % newbdmax).strip()
    try:
        bdmax = float(maxval)
    except ValueError:
        bdmax = newbdmax
    print('Maximum birth/death has been set to %.3f.' % bdmax)
    return (bdmin, bdmax)

def writePDpics(method, normalised, inverted, numframes, left, right, top, bottom, normconst, bdmin, bdmax):
    suffix = findSuffix(method, normalised, inverted)
    foldername = 'persistence' + suffix
    try:
        mkdir(foldername)
    except OSError:
        warn('folder "%s" already exists: possibly rewriting data.' % foldername, RuntimeWarning)
    cropping = array([left,right,top,bottom])
    savetxt(foldername+'/cropping.csv', cropping, fmt='%d')
    print('Plotting persistence diagrams...')
    for i in range(numframes):
        p0 = loadtxt('ph0%s/frame%.5d.csv' % (suffix,i), delimiter=',')
        p1 = loadtxt('ph1%s/frame%.5d.csv' % (suffix,i), delimiter=',')
        fig = pyplot.figure(figsize=(5,5))
        ax = fig.add_subplot(111)
        ax.plot([bdmin,bdmax],[bdmin,bdmax],c='k',linewidth=0.5,zorder=1)
        ax.scatter(p0[:,0],p0[:,1],s=10,c='r',alpha=0.4,zorder=3)
        ax.scatter(p1[:,0],p1[:,1],s=10,c='b',alpha=0.4,zorder=2)
        ax.set_xlim((bdmin,bdmax))
        ax.set_ylim((bdmin,bdmax))
        ax.set_xlabel('birth')
        ax.set_ylabel('death')
        pyplot.savefig('%s/frame%.5d.png' % (foldername,i))
        pyplot.close(fig)
        progressBar(i+1,numframes)

if __name__=='__main__':
    method, normalised, inverted, param = firstThingsToDo(argv[0])
    numframes, left, right, top, bottom = map(int,param[:5])
    normconst = param[6]
    bdmin,bdmax = -10,265
    if normalised:
        newbdmin,newbdmax = bdmin/normconst,bdmax/normconst
    else:
        newbdmin,newbdmax = bdmin,bdmax
    newbdmin, newbdmax = PDpicDialogue(newbdmin, newbdmax)
    writePDpics(method, normalised, inverted, numframes, left, right, top, bottom, normconst, newbdmin, newbdmax)

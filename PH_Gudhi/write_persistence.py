from checks import findSuffix,firstThingsToDo,progressBar
import gudhi
from numpy import array,savetxt
from os import mkdir
from sys import argv
from warnings import warn

def writePH(method, normalised, inverted, numframes, left, right, top, bottom):
    suffix = findSuffix(method, normalised, inverted)
    for i in ['0','1']:
        foldername = 'ph'+i+suffix
        try:
            mkdir(foldername)
        except OSError:
            warn('folder "%s" already exists: possibly rewriting data.' % foldername, RuntimeWarning)
        cropping = array([left,right,top,bottom])
        savetxt(foldername+'/cropping.csv', cropping, fmt='%d')
    print('Computing persistence...')
    for i in range(numframes):
        cc = gudhi.CubicalComplex(perseus_file='perseus%s/frame%.5d.csv'%(suffix,i))
        p = cc.persistence(2)
        p0 = [y for x,y in p if x==0]
        p1 = [y for x,y in p if x==1]
        savetxt('ph0%s/frame%.5d.csv' % (suffix,i), array(p0), fmt='%.15f', delimiter=',')
        savetxt('ph1%s/frame%.5d.csv' % (suffix,i), array(p1), fmt='%.15f', delimiter=',')
        progressBar(i+1,numframes)

if __name__=='__main__':
    method, normalised, inverted, param = firstThingsToDo(argv[0])
    numframes, left, right, top, bottom = map(int,param[:5])
    writePH(method, normalised, inverted, numframes, left, right, top, bottom)

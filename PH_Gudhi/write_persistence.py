folder = 'suppl_movie8v2'
suffix = 'n' # the code reads files from the folder 'perseus'+suffix (created with write_perseus.m)
             # suffix must be one of '', 'i', 'n', 'ni'
from os import chdir,mkdir
import gudhi
from numpy import savetxt,loadtxt,array

#Persistence
chdir('../Experiments/'+folder)
for i in ['0','1']:
    try:
        mkdir('ph'+i+suffix)
    except OSError:
        pass
param = loadtxt('parameters.csv')
start,inc,end = map(int,param[:3])
for i in range(start,end+1,inc):
    fname = 'frame%.5d.csv' % i
    cc=gudhi.CubicalComplex(perseus_file='perseus'+suffix+'/'+fname)
    p=cc.persistence(2)
    p0=[y for x,y in p if x==0]
    p1=[y for x,y in p if x==1]
    savetxt('ph0'+suffix+'/'+fname, array(p0), fmt='%.15f', delimiter=',')
    savetxt('ph1'+suffix+'/'+fname, array(p1), fmt='%.15f', delimiter=',')
    print(i)

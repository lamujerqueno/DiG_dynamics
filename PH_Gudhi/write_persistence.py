folder='Nina_experiments/5CB_3hull_01c'
from os import chdir,mkdir
import gudhi
from numpy import savetxt,loadtxt,array

#Persistence
chdir(folder)
for i in ['0','1','0i','1i']:
    try:
        mkdir('ph'+i)
    except OSError:
        pass
param = loadtxt('param2.csv')
start,inc,end = map(int,param[:3])
inc=2
#start,inc,end = 1,1,10
for i in range(start,end+1,inc):
    fname = 'frame%.5d.csv' % i
    cc=gudhi.CubicalComplex(perseus_file='perseus/'+fname)
    cci=gudhi.CubicalComplex(perseus_file='perseusi/'+fname)
    p=cc.persistence(2)
    pi=cci.persistence(2)
    p0=[y for x,y in p if x==0]
    p1=[y for x,y in p if x==1]
    p0i=[y for x,y in pi if x==0]
    p1i=[y for x,y in pi if x==1]
    savetxt('ph0/'+fname, array(p0), fmt='%.15f', delimiter=',')
    savetxt('ph0i/'+fname, array(p0i), fmt='%.15f', delimiter=',')
    savetxt('ph1/'+fname, array(p1), fmt='%.15f', delimiter=',')
    savetxt('ph1i/'+fname, array(p1i), fmt='%.15f', delimiter=',')
    print i

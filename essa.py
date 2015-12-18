__author__ = 'fuocoal'
def echange(l,i,j):
    a=l[i]
    l[i]=l[j]
    l[j]=a
    return l

print(echange([1,2,3],0,1))
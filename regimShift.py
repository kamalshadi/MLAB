import numpy as num
import pylab as pl
from scipy.stats import t
import math

def sigDiff(s,l,p=.1):
	#calculate significant change for x with confidance p
	tval=abs(t.ppf(p/2,2*l-2))
	return tval*s*math.sqrt(2.0/l)
	

def test_event(diff,m,y):
	if abs(m-y)<diff:
		return 0
	if y-m>=diff:
		return +1
	if y-m<=diff:
		return -1
if __name__=='__main__':
	l=20	# parameter of an algorithm
	p=.05
	mu, sigma, n = 0, 1, 300
	a = num.random.normal(mu,sigma,n)
	a[100:140]=a[100:140]-8
	L=len(a)
	vc=a[0:l]
	pl.plot(range(L),a,'b-')
	s=sigma
	m=num.mean(vc)
	diff=sigDiff(s,l)
	print diff
	i=l-1
	fg=True
	while fg:
		if i+l>L:
			break
		j=i+1
		ef=test_event(diff,m,a[j]) #event start flag
		ep=1 #event prove flag
		if ef==0:
			pass
		else:
			RSI=0.0
			for k in range(j,j+l):
				if ef==-1 :
					RSI=RSI+((m-diff)-a[j])/(l*s)
				if ef==1 :
					RSI=RSI-((m-diff)-a[j])/(l*s)
				if RSI < 0 :
					ep = 0
					break
		if ef != 0 and ep ==1 :
			vc = a[j:(j+l)]
			i=j+l-1
			pl.plot(range(j,j+l),vc,'r*')
		else :
			vc = a[j:(j+l)]
			i=j+l-1
		m=num.mean(vc)
		
		
			
			
				
				
		i=i+1
		vc=a[(i-l):(i+1)]
		s=num.std(vc)
		m=num.mean(vc)
	pl.show()
	

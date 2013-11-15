import numpy as num
import pylab as pl
from scipy.stats import t
import math
import Queue as qx
from eventDetection import *

def sigDiff(s,l,p=.01):
	#calculate significant change for x with confidance p
	tval=abs(t.ppf(p/2,l-1))
	return tval*s*math.sqrt(2.0/l)
	

def test_event(diff,m,y):
	if abs(m-y)<diff:
		return 0
	if y-m>=diff:
		return +1
	if y-m<=diff:
		return -1
		
def qiHe(x,W=30,l=10,a=0.4,b=0.3):
	# x is N-sample sequence
	# W is window size
	# a is outlier thereshold
	# b is LS thereshold
	# l is intial training < W 
	N=len(x)
	pl.plot(range(N),x,'b-')
	c=W
	vc=x[0:c]
	fg=True 
	loop=0
	while fg:
		m=num.median(vc)
		s=num.std(vc)
		pl.plot([loop*W+i for i in range(W)],[float(m)]*W,'r--')
		for i,w in enumerate(vc):
			#~ pl.plot(loop*W+i,w,'r*')
			if abs(w-m) > 3*s :
				pl.plot(loop*W+i,w,'r*')
		loop=loop+1
		if (loop*W)+c > N :
			break
		vc=x[(loop*W):((loop*W)+c)]
		
		
if __name__=='__main__':
	l=30	# parameter of an algorithm
	p=.01
	N=3000
	mu, sigma, n = 0, 1, N
	a = num.random.normal(mu,sigma,n)
	#~ diff=sigDiff(sigma,l)   # has to be replaced by t-statistics
	#~ print diff
	a[100:140]=a[100:140]-2
	a[200:227]=a[200:227]+2
	a[260]=-5.0
	a[500:520]=a[500:520]+1
	a[670:700]=a[670:700]-2
	a[1000:1500]=a[1000:1500]+1
	a[2000:2227]=a[2000:2227]-5
	a[2227:2500]=a[2227:2500]+3
	#~ a,ev1=genEvent(l,.1,1,.1)
	#~ a2,ev2=genEvent(l,.2,4,.1)
	#~ a=list(a)+list(a2)
	#~ ev1=list(ev1)+list(ev2)
	out=eventDetection(a,1,l,p)
	pl.plot(range(len(a)),a)
	pl.ylabel('Sequence Magnitude',fontsize=20)
	pl.xlabel('Sample Number',fontsize=20)
	pl.twinx()
	#~ pl.plot([0,len(a)],[max(a),max(a)],'k',linewidth=2)
	for w in out:
		if w[1]>0 :
			pl.vlines(w[0],0,abs(w[1]),color='green',linewidths=4)
		else:
			pl.vlines(w[0],0,abs(w[1]),color='red',linewidths=4)
	pl.ylabel('Event Power',fontsize=20)
	pl.show()
	#~ tp,fp=[],[]
	#~ p=0.01
	#~ l=30
	#~ L=[10,15,20,25,30,35,40]
	#~ es=[.25,.5,.75,1,1.25]
	#~ ite=100
	#~ tp=[]
	#~ fp=[]
	#~ for w in es:
		#~ tp1=[0.0]*ite
		#~ fp1=[0.0]*ite
		#~ for it in range(ite): 
			#~ a,ev1=genEvent(l,.1,w)
			#~ r1=eventDetection(a,1,l,p)
			#~ ev2=eventVector(r1,len(a))
			#~ fp2,tp2 = roc(ev1,ev2)
			#~ tp1[it]=tp2
			#~ fp1[it]=fp2
		#~ tp.append(num.mean(tp1))
		#~ fp.append(num.mean(fp1))
			
			
			
	#~ pl.plot(es,tp)
	#~ pl.plot(es,fp,'r')
	#~ pl.plot(range(len(a)),ev,'r')
	#~ pl.show()
	#~ print roc([0,0,0,0,1,1,1,1,0,0,0,0],[0,0,0,1,1,1,1,1,0,0,0,0])

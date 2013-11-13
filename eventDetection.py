import Queue as qx
import pylab as pl
import numpy as num
from scipy.stats import t
import math

def sigDiff(s,l,p=.01):
	#calculate significant change for x with confidance p
	tval=abs(t.ppf(p/2,l-1))
	return tval*s*math.sqrt(2.0/l)
	
def eventDetection(a,sigma,l=30,p=0.01):
	N=len(a)
	diff=sigDiff(sigma,l)
	q=qx.Queue(N)
	#loading
	for w in a:
		q.put(w,False)
	V=[0.0]*l
	for i in range(l):
		V[i]=q.get(False)
	ev=qx.Queue(l)
	i=l-1
	pl.plot(range(N),a)
	inp=qx.Queue(N)
	while ((not q.empty()) or (not inp.empty())) :
		if V[-1] is not None:
			if len(V)==l:
				m=num.mean(V)
			else:
				pass
			try:
				v=inp.get(False)
			except qx.Empty:
				v=q.get(False)
			i=i+1
			if abs(v-m) <= diff:
				if len(V) < l:
					V=V+[v]
				else:
					V[:]=V[1:]+[v]
				continue
			else:
				ep=1
				if v-m < 0: #Downward shift
					RSI=(m-v-diff)/(l*sigma)
					for j in range(0,l-1):
						try:
							can=inp.get(False)
						except qx.Empty:
							try:
								can=q.get(False)
							except qx.Empty:
								ep=0
								break
						ev.put(can,False)
						RSI=RSI+(-can+m-diff)/(l*sigma)
						if RSI <= 0:
							while not ev.empty():
								inp.put(ev.get(False),False)
							if len(V) < l :
								V=V+[v]
							elif len(V)==l:
								V=V[1:]+[v]
							else:
								print 'ERROR in V vector'
							ep=0
							break
					if ep==1:
						temp=list(ev.queue)
						V=[v]
						m=num.mean(V+temp)
						for w in temp:
							inp.put(w,False)
						pl.plot(i,v,'r*')
						ev=qx.Queue(l)

				else:						 #upward shift
					RSI=(v-m-diff)/(l*sigma)
					for j in range(0,l-1):
						try:
							can=inp.get(False)
						except qx.Empty:
							try:
								can=q.get(False)
							except qx.Empty:
								ep=0
								break
						ev.put(can,False)
						RSI=RSI+(can-m-diff)/(l*sigma)
						if RSI <= 0:
							while not ev.empty():
								inp.put(ev.get(False),False)
							if len(V) < l :
								V=V+[v]
							elif len(V)==l:
								V=V[1:]+[v]
							else:
								print 'ERROR in V vector'
							ep=0
							break
					if ep==1:
						temp=list(ev.queue)
						V=[v]
						m=num.mean(V+temp)
						for w in temp:
							inp.put(w,False)
						pl.plot(i,v,'r*')
						ev=qx.Queue(l)
		else:
			try:
				V[V.index(None)]=inp.get(False)
			except qx.Empty:
				try:
					V[V.index(None)]=q.get(False)
				except qx.Empty:
					continue
			i=i+1
		pl.plot(i,m,'ks')
	pl.show()

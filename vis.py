#!/usr/bin/env python

import csv
import os
import sys
import subprocess
import statvfs
import pylab as pl

def usage():
    return """
Summary:
./geoUoS -p False/True -f <filename> 
locate the UoS in city resolution
"""
		

def parse_args():
    from optparse import OptionParser
    parser = OptionParser(usage=usage())
    parser.add_option("-d", "--dirc", dest="dirc", default=None, 
                      help="Required: sub_directory in Dump")
    parser.add_option("-u", "--uos", dest="uos", default="1", 
                      help="Required: filename for geo data")
        
    
                       
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()
    if options.dirc is None:
        print "Error: Please provide --dir to read data \n \
        (do not include D- prefix)"
        sys.exit(1)

    return (options, args)
    
    
def order(v,w):
	a=zip(v,w)
	a.sort()
	l=zip(*a)
	v=list(l[0])
	w=list(l[1])
	return [v,w]

if __name__ == '__main__':
	(options, args) = parse_args()
	dirc=options.dirc
	uos=options.uos
	ad="Dump/D-"+dirc+"/uos_"+uos
	i=0
	with open(ad,'r') as f:
		val=csv.reader(f,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i,line in enumerate(val):
			if i==0:
				l=len(line)
				i=1
				continue
			else:
				cIP=line[0]
				server=line[-1]
				log=int(line[1])
				t=[float(xx)/1e6 for xx in line[2].strip('"').split(',')]
				rtt=[float(xx) for xx in line[3].strip('"').split(',')]
				cwnd=[float(xx) for xx in line[4].strip('"').split(',')]
				loss=[float(xx) for xx in line[5].strip('"').split(',')]
				ss=[float(xx) for xx in line[6].strip('"').split(',')]
				ca=[float(xx) for xx in line[7].strip('"').split(',')]
				cs=[float(xx) for xx in line[8].strip('"').split(',')]
				th=[float(xx) for xx in line[9].strip('"').split(',')]
				down=float(line[l-2])/(1e6*max(t))
				t,w=order(t,zip(rtt,cwnd,loss,ss,ca,cs,th))
				rtt,cwnd,loss,ss,ca,cs,th=[list(xx) for xx in zip(*w)]
				fig=pl.figure()
				ax=pl.subplot(421)
				ax.plot(t,rtt)
				pl.ylabel('RTT')
				ax=pl.subplot(422)
				ax.plot(t,cwnd)
				pl.ylabel('cwnd')
				ax=pl.subplot(423)
				ax.plot(t,loss)
				pl.ylabel('loss')
				ax=pl.subplot(424)
				ax.plot(t,ss)
				pl.ylabel('SlowStart')
				ax=pl.subplot(425)
				ax.plot(t,ca)
				pl.ylabel('congAvoid')
				ax=pl.subplot(426)
				ax.plot(t,cs)
				pl.ylabel('congSignals')
				ax=pl.subplot(427)
				ax.plot(t,th)
				pl.ylabel('slow Threshold')
				pl.xlim(3,12)
				pl.ylim(min(th[1000:]),max(th[1000:]))
				pl.suptitle('Throughput: '+str(down))
				pl.show()
				
				
				

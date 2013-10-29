#!/usr/bin/env python

import csv
import os
import sys
import subprocess
import statvfs

def usage():
    return """
Summary:
./geoUoS -p False/True -f <filename> 
locate the UoS in city resolution
"""
		

def parse_args():
    from optparse import OptionParser
    parser = OptionParser(usage=usage())
    parser.add_option("-f", "--fileName", dest="fName", default=None, 
                      help="Required: filename for geo data")
        
    
                       
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()
    if options.fName is None:
        print "Error: Please provide --filename to read data \n \
        (do not include .G suffix)"
        sys.exit(1)

    return (options, args)
		

if __name__ == '__main__':
	(options, args) = parse_args()
	fName=options.fName
	fg=0
	t1=fName.split('-')[0]
	t2=t1.split('~')
	tt=[]
	for w in t2:
		tt.append("[measurement-lab:m_lab."+w.strip()+"]")
	table=','.join(tt)
	with open('CSV/'+fName+'.uos','r') as f:
		st=f.read()
	uos=eval(st)
	directory="D-"+fName
	os.system('rm Temp/* -f')
	for i,w in enumerate(uos):
		log="Temp/uos-"+str(i)
		with open(log,'w') as f:
			temp=w.split('U')
			qq=[]
			for h in temp:
				sub,l1=h.split('/')
				l=int(l1)
				mask=int('1'*l+'0'*(32-l),2)
				qq.append('format_ip(parse_ip(web100_log_entry.connection_spec.remote_ip) & ' + str(mask) + ')="'+sub.strip()+'"')
			q=' OR \n'.join(qq)
			with open('MyQuery/testID','r') as f:
				query1=f.read()
			query1 = query1.replace('COND',q)
			query = query1.replace('TABLE',table)
			add='bq -q --format=csv query --max_rows 1000000 '
			shel=add+'\''+query+'\' >> '+log
			print "Downloading Tests' IDs for uos "+str(i+1)+" / "+str(len(uos))
			r=os.system(shel)
	for root, dirs, filenames in os.walk("Temp"):
		if not os.path.exists("Dump/D-"+fName):
			os.makedirs("Dump/D-"+fName)
		for j,fn in enumerate(filenames):
			log="Dump/D-"+fName+"/uos_"+str(j+1)
			tID=[]
			with open("Temp/"+fn,'r') as f:
				for lines in f:
					tID.append('test_id="'+lines.strip()+'"')
				l=len(tID)
				m=l
				ing=0
				while l>0:
					temp=tID[0:50]
					del tID[0:50]
					l=len(tID)
					cond='\n OR \n'.join(temp)
					with open('MyQuery/web100','r') as f2:
						query1=f2.read()
					query1 = query1.replace('COND',cond)
					query = query1.replace('TABLE',table)
					add='bq -q --format=csv query --max_rows 1000000 '
					if ing==0:
						shel=add+'\''+query+'\' > '+log
						print "Downloading NDT web100 variables for uos "+str(j+1)+" / "+str(len(uos))
						print str(m)+" tests..."
						ing=1
					else:
						shel=add+'\''+query+'\' | tail -n+2 >> '+log
					r=os.system(shel)

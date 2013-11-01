import csv
import numpy as num
import re
from ipClass import *
from myBasic import *
import math
import networkx as nx
from graphvisu import *

def parseCSV(f, mode = 3):
    pV = []
    t = []
    idd = []
    temp1 = []
    temp2 = []
    temp3 = ['init']
    i = 0
    if mode == 1:
        val = csv.reader(f)
        for o, row in enumerate(val):
            if i > 0:
                temp1.append(row[1])
                temp2.append(row[2])
                temp3.insert(0, row[0])
                a = temp3.pop()
                if temp3[0] != a and a != 'init':
                    t.append(temp1[0:-1])
                    pV.append(temp2[0:-1])
                    idd.append(test_id_2_ip(a))
                    temp1 = [temp1[-1]]
                    temp2 = [temp2[-1]]
            else:
                patch = [row[1], row[2]]
                i = 2

    if mode == 2:
        val = csv.reader(f, delimiter=';')
        for row in val:
            if i == 0:
                patch = row
                i = 2
                continue
            if i > 0:
                idd.append(row[0])
                t1 = row[1].strip('[]')
                t2 = t1.split(',')
                t.append(t2)
                v1 = row[2].strip('[]')
                v2 = v1.split(',')
                pV.append(v2)

    if mode == 3:
        val = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in val:
            if i == 0:
                patch = [row[1], row[2]]
                i = 2
                continue
            if i > 0:
                idd.append(row[0])
                t1 = row[1].strip('"\'')
                t2 = t1.split(',')
                v1 = row[2].strip('"\'')
                v2 = v1.split(',')
                pV.append(v2)
                t.append(t2)

    return [idd,
     t,
     pV,
     patch]


def readCSV(fName, mode = 3):
    f = open('csv/' + fName, 'r')
    idd, t, v, s = parseCSV(f, mode)
    z = []
    tt = []
    ax = []
    ttl = []
    for o, w in enumerate(idd):
        tp = [ float(t[o][x]) for x in range(len(t[o])) ]
        vp = [ float(v[o][x]) for x in range(len(v[o])) ]
        tp, vp = order(tp, vp)
        z.append(vp)
        tt.append(tp)
        ttl.append(w)

    return [tt,
     z,
     s,
     ttl]


def test_id_2_ip(test_id):
    x = '\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}'
    if type(test_id) != list:
        ip = re.search(x, test_id)
        if ip:
            return ip.group()
    else:
        ipl = [None] * len(test_id)
        for i, w in enumerate(test_id):
            ip = re.search(x, w)
            if ip:
                ipl[i] = ip.group()

        return ipl


def test_id_2_time(test_id):
    if type(test_id) != list:
        w = test_id[0:10] + ' @ ' + test_id[20:28]
        return w
    else:
        tl = [None] * len(test_id)
        for i, w in enumerate(test_id):
            tl[i] = w[0:10] + ' @ ' + w[20:28]

        return tl


def serverRead(fName):
    sIP = []
    with open('CSV/' + fName, 'r') as f:
        val = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i, item in enumerate(val):
            sIP.append(item[-1])

    del sIP[0]
    return sIP


def clientRead(fName):
    cIP = []
    with open('CSV/' + fName, 'r') as f:
        val = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for item in val:
            w = test_id_2_ip(item[0])
            cIP.append(w)

    del cIP[0]
    return cIP


def timeRead(fName):
    t = []
    with open('csv/' + fName, 'r') as f:
        val = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for item in val:
            t.append(test_id_2_time(item[0]))

    del t[0]
    return t


def readCol(fName, L = None):
    i = 0
    p = []
    if type(L) != list and L:
        with open('CSV/' + fName) as f:
            val = csv.reader(f)
            for row in val:
                if i == 0:
                    i = 1
                    continue
                p.append(row[L])

    else:
        with open('CSV/' + fName) as f:
            val = csv.reader(f)
            for row in val:
                if i == 0:
                    i = 1
                    continue
                if L:
                    p.append(row[L[0]:L[-1] + 1])
                else:
                    p.append(row)

    return p


def csv2gml(fName, eps, plot):
    """ this function reads csv file with heading :
    test_id  ,  minRTT  , .... ,  server
    and then makes edges between clients if their similarities
    is above eps and returns the graph """
    p = readCol(fName)
    lIP = ['aaaaaaaaa'] * len(p)
    lS = ['aaaaaaaaa'] * len(p)
    minRTT = [0] * len(p)
    sim = {}
    E = []
    for i, xx in enumerate(p):
        w = test_id_2_ip(xx[0])
        if w is None:
            print xx[0]
        lIP[i] = w
        lS[i] = ipClass(xx[-1]).sub('/24').string()
        minRTT[i] = float(xx[1])

    myDic = list2dic(lS, zip(lIP, minRTT))
    print 'Number of servers : ' + str(len(myDic))
    for i, w in enumerate(myDic.keys()):
        occur = {}
        l = len(myDic[w])
        print '\n loop:'
        print l * (l - 1) / 2
        v = [ ww[1] for ww in myDic[w] ]
        sigma = num.std(v)
        for comb in combinations(myDic[w], 2):
            a = comb[0][0]
            b = comb[1][0]
            delta = abs(comb[0][1] - comb[1][1])
            link = (a, b)
            if link in occur.keys():
                occur[link] = occur[link] + 1
            else:
                occur[link] = 0
            if link not in sim.keys():
                sim[link] = [math.exp(-delta / sigma)]
            elif link in sim.keys() and occur[link] == 0:
                sim[link] = sim[link] + [math.exp(-delta / sigma)]

    G = nx.Graph()
    for w in sim.keys():
        weight = combSum(sim[w])
        if weight > eps:
            G.add_edge(w[0], w[1], weight=weight)

    if plot:
        myDraw(G, fName)
    nx.write_graphml(G, 'CSV/' + fName + '.G')
    print 'Graph saved in CSV directory: ' + fName + '.G'
    return 1


def walktrapFile(fName):
    G = nx.read_graphml('CSV/' + fName + '.G')
    if G:
        pass
    else:
        return 0
    a = G.nodes()
    b = range(len(a))
    myDic = list2dic(a, b)
    f = open('CSV/' + fName + '.walktrap', 'w')
    for edge in G.edges():
        w = G[edge[0]][edge[1]]['weight']
        ind1 = myDic[edge[0]][0]
        ind2 = myDic[edge[1]][0]
        s = str(ind1) + ' ' + str(ind2) + ' ' + str(w) + '\n'
        f.write(s)

    f.close()
    return 1


def communityGraph(fName, plot):
    G = nx.read_graphml('CSV/' + fName + '.G')
    a = G.nodes()
    b = [ str(xx) for xx in range(len(a)) ]
    myDic = list2dic(b, a)
    with open('CSV/' + fName + '.C', 'r') as f:
        for j, line in enumerate(f):
            t1 = line.strip(' {}\t\n')
            t2 = t1.split(',')
            cc = pickColor(j)
            for w in t2:
                n = myDic[w.strip()]
                G.node[n[0]]['color'] = cc

    if plot:
        myDraw(G, fName + '-C')


def UoSM_input(fName):
    G = nx.read_graphml('CSV/' + fName + '.G')
    a = G.nodes()
    b = [ str(xx) for xx in range(len(a)) ]
    myDic = list2dic(b, a)
    C = []
    with open('CSV/' + fName + '.C', 'r') as f:
        for line in f:
            t1 = line.strip(' {}\t\n')
            t2 = t1.split(',')
            t = [ xx.strip() for xx in t2 ]
            ll = [ myDic[xx][0] for xx in t ]
            C.append(ll)

    return C
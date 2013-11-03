import networkx as nx
import pylab as pl

def order(v,w):
	a=zip(v,w)
	a.sort()
	l=zip(*a)
	v=list(l[0])
	w=list(l[1])
	return [v,w]
	
def myDraw(G,labels=None):
	dS=600
	dC='blue'
	Ew=3
	for w in G.nodes(True):
		if 'color' not in w[1].keys():
			G.node[w[0]]['color']=dC
		if 'size' not in w[1].keys():
			G.node[w[0]]['size']=dS
	print labels
	pos=nx.spring_layout(G)
	N=nx.get_node_attributes(G,'color')
	nC=N.values()
	z=N.keys()
	z,nC=order(z,nC)
	N=nx.get_node_attributes(G,'size')
	nS=N.values()
	z=N.keys()
	z,nS=order(z,nS)
	nx.draw_networkx_nodes(G, pos,nodelist=z,node_size=nS,node_color=nC)
	if labels:
		t=G.nodes(True)
		a1=[w[0] for w in t if labels in w[1].keys()]
		a2=[w[1][labels] for w in t if labels in w[1].keys()]
		nx.draw_networkx_labels(G,pos, dict(zip(a1,a2)))
	elist=[]
	ew=[]
	for w in G.edges_iter():
		elist.append(w)
		if 'weight' not in G[w[0]][w[1]]:
			ew.append(Ew)
		else:
			ew.append(G[w[0]][w[1]]['weight'])
			
	nx.draw_networkx_edges(G, pos, edgelist=elist, width=ew)
	pl.show()
	#~ nx.draw_networkx_nodes(G, pos,nodelist=nC.keys(),node_label=nC.values())
	#namespace node: 'color','size'
	#namespace edge: 'width'




def s_core(G,s,weight='weight'):
	# label is the property of edges to be considered as weights
	if any(G.nodes()):
		pass
	else:
		print 'Warning:Graph is empty. None returned.'
		return None
	V=G.nodes()
	D=[G.degree(xx,weight) for xx in V]
	D,V=order(D,V)
	while G!={}:
		for i,d in enumerate(D):
			if d>s:
				break
		if i!=0:
			G.remove_nodes_from(V[:i])
		else:
			print 'Go'
			return G
		V=G.nodes()
		D=[G.degree(xx,weight) for xx in V]
		D,V=order(D,V)
	return G
	
def blackHole(G):
	N=G.nodes()
		
	
	
	

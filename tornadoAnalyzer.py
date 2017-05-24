import tornado.ioloop
import tornado.web
import os.path
import pygtk, gtk
import numpy as np
import matplotlib.pyplot as plt
import sys
import pickle
from scipy import linalg
from itertools import chain

class Analyser(tornado.web.RequestHandler):
    def __init__(self,energia,amplituda,s,v):
        Energia=energia
        Amplituda=amplituda
        S=E
        V=D
        #Path=path2
 

    
def PCA(lista, l_com):
	D_T = np.transpose(lista)
	Z = D_T.dot(lista)
	D, V = linalg.eig(Z)
	D2 = np.real(D)
	D3 = np.log(D2)
	sa=V.shape
	print sa[0], l_com, sa
	if l_com >= sa[1]:
		C = V		
		plt.plot(D3)
		plt.show()
	else:
		C=V[:,0:l_com]
	print C
	R = lista.dot(C)
	E = np.transpose(C)
	Drep = R.dot(E)
	return Drep
	  

if gtk.pygtk_version < (2,3,90):
    print "Please upgrade your pygtk"
    #rise SystemExit
    
dialog = gtk.FileChooserDialog("Open...", None,
        gtk.FILE_CHOOSER_ACTION_OPEN, 
        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
         gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        
dialog.set_default_response(gtk.RESPONSE_OK)   
dialog.set_select_multiple(True)

filter = gtk.FileFilter()
filter.set_name("All_files")   
filter.add_pattern("*.asc")
dialog.add_filter(filter)

response = dialog.run()

if response == gtk.RESPONSE_OK:
    #print dialog.get_filenames(), 'selected'
    #dr=np.dtype([('Energia',int),('Amplituda',float)])
    flista = [];
    flista = dialog.get_filenames();
    n = len(flista)
    #wiemy ze plik ma dwie kolumny
    colA, colB = np.loadtxt(flista[0],usecols=(0,1), unpack=True) 
    m = len(colB)
    x = colA   
    E=np.zeros((m,n))
    D=np.zeros((m,n))
    P=np.zeros(3)
    for i in range(n):
		colA, colB = np.loadtxt(flista[i],usecols=(0,1), unpack=True)
		if len(colB) != m:
			print 'Error: rozne dlugosci plikow!'
			sys.exit()
		#print colA, colB
		#if colA != x:
		#	print 'Error: rozne wektory energii'
		#	sys.exit()
		for j in range(m):
			E[j][i] = colA[j]
			D[j][i] = colB[j] 
    plt.plot(D)
    plt.show()
    Drepp = np.zeros((m,n,n))
    for j in range(n):
		print j
		Drepp[:,:,j]=PCA(D,j+1)	
    pplist = np.zeros(n);
    for i in range(n):
		pplist[i]=np.sum(abs(Drepp[:,:,i] - D))
    plt.plot(pplist)
    plt.show()
    plt.plot(D, Drepp[:,:,3],'o', [0,1.2],[0,1.2], '-')
    plt.show()

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')
		
settings=dict(
 #template_path=os.path.join(os.path.dirname(__file__),"temlates"),
 static_path=os.path.join(os.path.dirname(__file__),"static"),
 debug=True)
 
application=tornado.web.Application([(r"/",MainHandler)],**settings)
application=tornado.web.Application([(r"/pca",Analyser)],**settings)


if __name__=="__main__":
	print 'Server is running'
	print 'press ctrl+C to close'
	application.listen(8889)
	tornado.ioloop.IOLoop.instance().start()		

# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import numpy
import matplotlib.pyplot as plt
import pydot
from random import randint
import sys
import Image




"""
 identifiant: l'identifiant ou le nom du noeud
 listeArcE : la liste des arcs pointant vers le noeud
 listeArcS : la liste des sortant du noeud
"""
class Node:
   
    def __init__(self, identifiant):
        self.identifiant=identifiant
        self.listeArcE=list()
        self.listeArcS=list()
        
    def majArcE(self,ArcE):
        self.listeArcE.append(ArcE)
    
    def majArcS(self,ArcS):
        self.listeArcS.append(ArcS)

    
"""
 source : la source de l'arc
 destination: destination de l'arc
 proba: le poid de l'arc et c'est la probabilité que l'arc soit choisi
"""
class Arc:

    def __init__(self, source, destination):
        self.source=source
        self.destination=destination

    def maj(self, proba):
        self.proba=proba


"""
 matrice: matrice de transition
 listeNoeud: la liste des noeud du graphe
 
 def __init__(self,taille): creation de la matrice initialisée à zero, et creation de la listeNoeud
 def addArc(self, source, destination):creation d'un arc entre la source et la destination, mis à jour
            de la matrice ainsi que la liste des arcs sortants de la source et la liste des arcs entrant
            de la destination.

 def updateProbas(self): mis à jour des poids des arcs de manière uniforme
                  afin d'assurer l'homogénéité dans le cas d'un noeud ne pointant
                  vers aucun autre on mets sont auto référence à '1'

 def __str__(self): représentation en mode texte du graphe

 def getGraph(self, nom): représentation en mode graphique du graphe

 def initEstimation(self): estimation de distribution de probabilité

 def nextStep(self,pi_t): calcul la probabilité d'être dans chacun des noeuds dans le futur à partir de
              l'instant présent
              
 
"""
class SimpleWeb:

    def __init__(self,taille):
        self.matrice=numpy.zeros(shape=(taille,taille))
        self.listeNoeud=list()
        for i in range(taille):
            self.listeNoeud.append(Node(i))


    def addArc(self, source, destination):
        try:
            a=Arc(source, destination)
            if self.matrice[source,destination]==0:
                self.matrice[source][destination]=1.0
                
            else:
                print("Un arc entre "+str(source)+" et "+str(destination)+" exite déjà !")
                sys.exit(0)
        except:
            print('Noeud non existant!')
            sys.exit(0)



    def CFC(self):

       a=0
       #Cas noeud ne réferençant aucun autre noeud
       for i in range(len(self.matrice)):
           cpt=0
           for j in range(len(self.matrice)):
               if i!=j:
                   if self.matrice[i][j]==1.0:
                       cpt+=1
           if cpt==0:
                for j in range(len(self.matrice)):
                    self.matrice[i][j]=1.0
                    a+=1
       #Cas d'un noeud référencé par personne 
       for j in range(len(self.matrice)):
            cpt=0
            for i in range(len(self.matrice)):
                if self.matrice[j][i]==1.0:
                    cpt+=1
            if cpt==0:
               for i in range(len(self.matrice)):
                    self.matrice[j][i]=1.0
                    a+=1
       #Cas où on n'a pas rencontré les deux problèmes précédents on cree une autoreference
       if a==0:
           a=randint(0,len(self.matrice)-1)
           self.matrice[a][a]=1.0

       #lier les différentes composante connexte (pas fortement connexe)
       successeur=dict()
       for i in range(len(self.matrice)):
           successeur[i]=list()
           successeur[i].append(i)
           for j in range(len(self.matrice)):
               if self.matrice[i][j]==1.0:
                    successeur[i].append(j)
                    successeur[i]=list(set(successeur[i]))
       b=1 
       while b:
           for i in range(len(self.matrice)):
               b=0
               for j in range(len(self.matrice)):
                    successeur[i]=list(set(successeur[i]))
                    successeur[j]=list(set(successeur[j]))
                    if j in successeur[i]:
                       cpt=0
                       for k in range(len(successeur[j])):
                           if successeur[j][k] in successeur[i]:
                               cpt+=1
                       if cpt!=len(successeur[j]):        
                           b=1
                           for k in range(len(successeur[j])):
                              successeur[i].append(successeur[j][k])
                       successeur[i]=list(set(successeur[i]))
                   
       composanteConnexe=list()
       for i in range(len(self.matrice)):
           if successeur[i] not in composanteConnexe:
              composanteConnexe.append(successeur[i])
      
       if len(composanteConnexe)>1:
           prem=composanteConnexe[0][1]
           for i in range(len(composanteConnexe)-1):
               k=composanteConnexe[i][0]
               self.matrice[prem][k]=1.0
               self.matrice[k][prem]=1.0

               
    def updateProbas(self):
        for i in range(len(self.matrice)):
            cpt=0
            for j in range(len(self.matrice)):
                if self.matrice[i][j]==1.0:
                    cpt=cpt+1

            for j in range(len(self.matrice)):
                #Mis à jour de la matrice
                if self.matrice[i][j]==1.0 :
                    if cpt!=0:
                        self.matrice[i][j]=float(float(self.matrice[i][j])/float(cpt))                
                    #Creation des arcs
                        a=Arc(i,j)
                        a.maj(self.matrice[i][j])
                        self.listeNoeud[i].majArcS(a)
                        self.listeNoeud[j].majArcE(a)
                            

    def __str__(self):
        print('\n***************************Affichage des successeurs ****************************')
        s=str()

        for i in range(len(self.listeNoeud)):
            s=s+'\n'+str(i)+'----'

            for j in range(len(self.listeNoeud[i].listeArcS)):
                s=s+"|"+str(self.listeNoeud[i].listeArcS[j].destination)+'('+str(self.listeNoeud[i].listeArcS[j].proba)+')'

        return s
    
                           
    def getGraph(self, nom):
        graph=pydot.Dot(graph_type='digraph')

        for i in range(len(self.listeNoeud)):
            graph.add_node(pydot.Node("%d"%self.listeNoeud[i].identifiant,style="filled",fillcolor="green"))

        for i in range(len(self.listeNoeud)):
            for j in range(len(self.listeNoeud[i].listeArcS)):
                graph.add_edge(pydot.Edge(self.listeNoeud[i].listeArcS[j].source,self.listeNoeud[i].listeArcS[j].destination, label="%f"%self.listeNoeud[i].listeArcS[j].proba))

        graph.write_png(nom)
        im=Image.open(nom)
        im.show()
        
        
    def initEstimation(self):
        self.estimation=dict()
        for i in range(len(self.listeNoeud)):
            self.estimation[self.listeNoeud[i].identifiant]=0


    def nextStep(self,pi_t):
        return np.dot(pi_t,self.matrice) 
        

    def convergencePuissanceP(self,nombreLimiteIt,valConvergence,nbIt,fichier):
        epsilon=valConvergence+1
        iteration=1
        fichier=open(fichier,'w')
        while epsilon>=valConvergence and iteration<nombreLimiteIt:
            matricePlus=np.dot(self.matrice,self.matrice)
            p=abs(self.matrice-matricePlus)
            epsilon=p.max()
            fichier.write(str(iteration)+'\t'+str(epsilon)+'\n')
            self.matrice=matricePlus
            iteration+=1

    def showFrequence(self,fichier):
            listex=list()
            listey=list()
            with open(fichier, "r") as f:
                for l in f:
                    a=l.split()
                    listex.append(a[0])
                    listey.append(a[1])
            plt.plot(listex,listey)
            plt.xlabel('Temps')
            plt.ylabel('Epsilon')
            plt.title('Convergence au cours du temps')
            plt.show()
             


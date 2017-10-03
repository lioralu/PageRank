# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import numpy as np
import matplotlib.pyplot as plt
import pydot
from random import randint
import sys
import Image

class Node:
   
    def __init__(self, identifiant):
        self.identifiant=identifiant
        self.listeArcE=list()
        self.listeArcS=list()
        
    def majArcE(self,ArcE):
        self.listeArcE.append(ArcE)
    
    def majArcS(self,ArcS):
        self.listeArcS.append(ArcS)


class Arc:

    def __init__(self, source, destination):
        self.source=source
        self.destination=destination

    def maj(self, proba):
        self.proba=proba

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
        except:
            print('Noeud non existant!')




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
        return iteration     


import numpy
import matplotlib.pyplot as plt
import pydot
from random import randint
import sys
import Image


class Internaute:

    def __init__(self,nanoweb):
        self.web=nanoweb
        self.web.initEstimation()

    def goTo(self,identifiant):
        self.web.estimation[identifiant]+=1
        self.noeudActuel=identifiant

    def trace(self, nbIt, fichier):
        self.nombreIt=nbIt
        self.fichier=fichier
        

    def walk(self,nbLimiteNavigation, valConvergence):
        iteration=1                             #représente le temps
        epsilon=valConvergence+1                #seuil 
        fichier=open(self.fichier,'w')          #fichier contenant la variation d'epsilon dans le temps
        
        while iteration<nbLimiteNavigation and epsilon>=valConvergence:
            
            #estimateur à t=itération-1
            ancien=self.web.estimation
            
            if len(self.web.listeNoeud[self.noeudActuel].listeArcS)>0:                        #si le noeud possède au moins un successeur
                a=randint(0,len(self.web.listeNoeud[self.noeudActuel].listeArcS)-1)           #choix aléatoire du noeud suivant parmi les successeurs du noeud courant
                self.goTo(self.web.listeNoeud[self.noeudActuel].listeArcS[a].destination)     #positionnement dans le nouveau noeud

            else:
                self.goTo(self.noeudActuel)                                                   #rester dans le meme noeud
                
            if (iteration > 1): #on ne peut determiner le seuil que si l'on dispose d'au moins 2 estimation à des instants différents
                    #initialisation du seuil par la différence entre les estimations du noeud '0' au temps 't' et 't-1'
                epsilon=abs(float(ancien[0]*1.0/float(iteration-1))-float(self.web.estimation[0]*1.0/float(iteration)))
                for i in range(len(self.web.listeNoeud)-1):
                    epsilonPlus = abs(float(ancien[i+1]*1.0/float(iteration-1))-float(self.web.estimation[i+1]*1.0/float(iteration)))
                    epsilon=max(epsilon,epsilonPlus)
                        
                    #ecrire la valeur du seuil tous les self.nombreIt    
                if iteration % self.nombreIt ==0:
                    fichier.write(str(iteration)+'\t'+str(epsilon)+'\n')
            
                        
            iteration+=1

        return iteration
     
                    
class Simulation:
    
    def __init__(self,nanoweb):
        self.web=nanoweb

    def trace(self, nbIt, fichier):
        self.nombreIt=nbIt
        self.fichier=fichier

    def estimate(self,nbLimiteNavigation, valConvergence, pi_0):

        iteration=1
        epsilon=valConvergence+1
        fichier=open(self.fichier,'w')
        pi_t=pi_0

        while iteration<nbLimiteNavigation and epsilon>=valConvergence:
              
            if iteration > 1 :
                pi_tPlus1=self.web.nextStep(pi_t)
                epsilon=abs(float(pi_t[0])-float(pi_tPlus1[0]))
                for i in range(len(self.web.matrice)-1):
                    epsilonPlus = abs(float(pi_t[i])-float(pi_tPlus1[i]))
                    epsilon=max(epsilon,epsilonPlus)
                pi_t=pi_tPlus1
                if iteration % self.nombreIt ==0 and iteration!=0 :
                    fichier.write(str(iteration)+'\t'+str(epsilon)+'\n')
                        
            iteration+=1


        return iteration
        
    
 
def creeEstimation(taille):
    pi_t=dict()
    for i in range(taille):
        pi_t[i]=1.0/float(taille)
    return np.array(pi_t.values())




def creeNanoWeb1():
    
    n=SimpleWeb(10)
    n.addArc(0,1);n.addArc(0,4)
    n.addArc(1,2)
    n.addArc(2,3);n.addArc(2,4)
    n.addArc(3,9)
    n.addArc(4,2);n.addArc(4,5);n.addArc(4,6)
    n.addArc(5,6)
    n.addArc(6,5);n.addArc(6,7)
    n.addArc(7,8)
    n.addArc(8,7)
    n.CFC()
    n.updateProbas()
    return n

def creeNanoWeb2():
    n=SimpleWeb(10)
    n.addArc(0,9)
    n.addArc(1,0);n.addArc(1,5)
    n.addArc(2,1);n.addArc(2,4)
    n.addArc(3,2)
    n.addArc(4,3)
    n.addArc(5,4)
    n.addArc(6,5)
    n.addArc(7,3);n.addArc(7,6)
    n.addArc(8,7)
    n.addArc(9,2);n.addArc(9,8)
    n.CFC()
    n.updateProbas()

    return n

    
def creeNanoWeb3():
    n=SimpleWeb(10)
    n.addArc(0,1)
    n.addArc(1,2);n.addArc(1,3)
    n.addArc(2,3);n.addArc(2,9)
    n.addArc(4,5)
    n.addArc(5,4)
    n.addArc(6,7)
    n.addArc(7,8)
    n.addArc(8,7)
    n.CFC()
    n.updateProbas()

    return n


####################Reservé pour les test###########################
def creeNanoWeb100():
    n=SimpleWeb(100)
    #on cree 120 arcs
    for i in range(120):
        a=randint(0,99)
        b=randint(0,99)
        n.addArc(a,b)
    n.CFC()
    n.updateProbas()

    return n

def creeNanoWeb50():
    n=SimpleWeb(50)
    #on cree 50 arcs
    for i in range(75):
        a=randint(0,49)
        b=randint(0,49)
        n.addArc(a,b)
    n.updateProbas()

    return n

def creeNanoWeb300():
    n=SimpleWeb(300)
    #on cree 120 arcs
    for i in range(320):
        a=randint(0,299)
        b=randint(0,299)
        n.addArc(a,b)
    n.CFC()
    n.updateProbas()

    return n

def creeNanoWeb5():
    n=SimpleWeb(5)
    #on cree 10 arcs
    for i in range(10):
        a=randint(0,9)
        b=randint(0,9)
        n.addArc(a,b)
    n.CFC()
    n.updateProbas()

    return n






#def main():


listeBob=dict()

liste2=dict()

liste3=dict()


nanoweb=creeNanoWeb1()
bob=Internaute(nanoweb)
bob.goTo(0)
bob.trace(100,"epsilon.txt")
listeBob[0]=bob.walk(100000,0.0001)


s=Simulation(nanoweb)
s.trace(10,"epsilon1.txt")

liste2[0]=s.estimate(10000,0.01,creeEstimation(len(nanoweb.matrice)))


liste3[0]=nanoweb.convergencePuissanceP(100,0.01,10,"puissance.txt")
  #############################################################
nanoweb=creeNanoWeb50()
bob=Internaute(nanoweb)
bob.goTo(0)
bob.trace(100,"epsilon.txt")
listeBob[1]=bob.walk(10000,0.01)

s=Simulation(nanoweb)
s.trace(10,"epsilon1.txt")

liste2[1]=s.estimate(10000,0.01,creeEstimation(len(nanoweb.matrice)))


liste3[1]=nanoweb.convergencePuissanceP(100,0.01,10,"puissance.txt")

#############################################################
nanoweb=creeNanoWeb100()
bob=Internaute(nanoweb)
bob.goTo(0)
bob.trace(100,"epsilon.txt")
listeBob[2]=(bob.walk(10000,0.01))

s=Simulation(nanoweb)
s.trace(10,"epsilon1.txt")

liste2[2]=s.estimate(10000,0.01,creeEstimation(len(nanoweb.matrice)))


liste3[2]=nanoweb.convergencePuissanceP(100,0.01,10,"puissance.txt")


#############################################################
nanoweb=creeNanoWeb300()
bob=Internaute(nanoweb)
bob.goTo(0)
bob.trace(300,"epsilon.txt")
listeBob[3]=bob.walk(10000,0.01)

s=Simulation(nanoweb)
s.trace(10,"epsilon1.txt")

liste2[3]=s.estimate(10000,0.01,creeEstimation(len(nanoweb.matrice)))


liste3[3]=nanoweb.convergencePuissanceP(100,0.01,10,"puissance.txt")

print(liste2)
listex=[10,50,100,300]
listey=listeBob.values()

plt.plot(listex,listey)
plt.show()
#plt.plot(liste2.keys(),liste2.values())
#plt.xlabel("Nombre de noeud")
#plt.ylabel("Nombre d'itération")
#plt.title('Methode2')
#plt.show()
#plt.plot(liste3.keys(),liste3.values())
#plt.xlabel("Nombre de noeud")
#plt.ylabel("Nombre d'itération")
#plt.title('Methode3')
#plt.show()


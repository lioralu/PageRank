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
 web : le réseau dans lequel circulera l'internaute
 noeudActuel : noeud dans le quel se trouve l'internaute
 nombreIt : le pas pour conserver les valeurs d'epsilon
 fichier : fichier contenant la fréquence de la présence d'un internaute dans chaque
            noeud durant sa promenade
 
 def __init__(self,nanoweb): initialisation du web à parcourir
 def goTo(self,identifiant): placer l'internaut dans un noeud de départ ayant 'identifiant' comme identifiant
 def trace(self, nbIt, fichier): attribution d'une valeur à 'nombreIt' et 'fichier'
 def walk(self,nbLimiteNavigation, valConvergence): l'internaute se balade dans le graphe jusqu'à atteindre
          nbLimiteNavigation ou avoir un epsilon inférieur strictement à valConvergence
 def showFrequencies(self): affiche la variation de epsilon dans le tems 

"""

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

        if epsilon<valConvergence:
            print("Convergence, la valeur de epsilon :"+str(epsilon)+" le nombre d'itération :"+str(iteration))
        else:
            print("Fin d'itération, pas de convergence")
        
     
            
        #Distribution de probabilité en cas de convergence seulement
        if epsilon <valConvergence:
            print('\n\n*** Estimation de la distribution de probabilité *** ')
            for i in range(len(self.web.listeNoeud)):
                self.web.estimation[i]=float(self.web.estimation[i])/float(iteration)
            
        print(self.web.estimation.items())
       
                            

    def showFrequencies(self):
            listex=list()
            listey=list()
            with open(self.fichier, "r") as f:
                for l in f:
                    a=l.split()
                    listex.append(a[0])
                    listey.append(a[1])
            plt.plot(listex,listey)
            plt.xlabel('Temps')
            plt.ylabel('Epsilon')
            plt.title('Convergence au cours du temps')
            plt.show()
                    


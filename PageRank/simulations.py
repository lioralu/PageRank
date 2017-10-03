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
Vecteurs-matrices
web : le réseau web considéré
 nombreIt : indique après combien de temps faut il sauvegarder epsilon
 fichier : le fichier dans le quel sauvegarder les valeurs d'epsilon

 def __init__(self,nanoweb): initialisation du web
 def trace(self, nbIt, fichier): initaliser 'nombreIt' et 'fichier'
 def estimate(self,nbLimiteNavigation, valConvergence, pi_0): caclul des futures probabilitées
              d'être dans chacun des neoud à partir des probabilitées présentes
 def showFrequencies(self): construction d'un graphe de variation des valeurs d'epsilon

"""
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

        if epsilon<valConvergence:
            print("Convergence, la valeur de epsilon :"+str(epsilon)+" le nombre d'itération :"+str(iteration))
        else:
            print("Fin d'itération, pas de convergence")
     
            
        #Distribution de probabilité en cas de convergence seulement
        if epsilon <valConvergence:
            print('\n\n*** Estimation de la distribution de probabilité *** ')
        
        print(pi_tPlus1)#.items())
        return iteration
        
     

    
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
                    
 

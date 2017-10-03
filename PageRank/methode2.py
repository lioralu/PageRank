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
import numpy as np
       
            
from sys import path
path.append('.')

from nanowebs import creeNanoWeb1
from nanowebs import creeNanoWeb2
from nanowebs import creeNanoWeb3

from simulations import Simulation

#Créer une ditribution de probabilité uniforme
def creeEstimation(taille):
    pi_t=dict()
    for i in range(taille):
        pi_t[i]=1.0/float(taille)
    return np.array(pi_t.values())

pi_t=np.array([0.08,0.1,0.1,0.05,0.3,0.05,0.01,0.02,0.09,0.02])


nanoweb=creeNanoWeb3()
s=Simulation(nanoweb)
s.trace(10,"epsilon1.txt")
#s.estimate(10000,0.0001,pi_t)
s.estimate(10000,0.0001,creeEstimation(len(nanoweb.matrice)))
s.showFrequencies()

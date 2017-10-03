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

       
            
from sys import path
path.append('.')

from nanowebs import creeNanoWeb1
from nanowebs import creeNanoWeb2
from nanowebs import creeNanoWeb3
n1=creeNanoWeb3()
n1.convergencePuissanceP(100,0.0001,10,"puissance.txt")
n1.showFrequence("puissance.txt")


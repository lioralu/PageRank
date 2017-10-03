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

from nanowebsErgo import creeNanoWeb1
from nanowebsErgo import creeNanoWeb2
from nanowebsErgo import creeNanoWeb3
from internautes import Internaute


nanoweb=creeNanoWeb3()
bob=Internaute(nanoweb)
bob.goTo(0)
bob.trace(100,"epsilon.txt")
bob.walk(100000,0.0001)
bob.showFrequencies()


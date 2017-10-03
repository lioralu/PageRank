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

from datastructuresErgo import SimpleWeb
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

if __name__ == "__main__":
    print("_________________________________NANO WEB 1 __________________________________")
    n1=creeNanoWeb1()
    print(n1)
    n1.getGraph("nano1.png")
    print("_________________________________NANO WEB 2 __________________________________")
    n2=creeNanoWeb2()
    print(n2)
    n2.getGraph("nano2.png")
    print("_________________________________NANO WEB 3 __________________________________")
    n3=creeNanoWeb3()
    print(n3)
    n3.getGraph("nano3.png")



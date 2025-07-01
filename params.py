#### Librerias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import itertools
import sys

import riroriro.inspiralfuns as ins
import riroriro.mergerfirstfuns as me1
import riroriro.matchingfuns as mat
import riroriro.mergersecondfuns as me2

#### Parametros 
#GW150914-like
logMc =1.2
q     =0.8

#defaults
flow=10.0           #(Hz)
merger_type='BH'
D=100.0             #(Mpc)


path = "./results/"
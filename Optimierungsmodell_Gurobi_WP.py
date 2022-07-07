from pythena_lite import pivot_and_resample_iot_data
import pandas as pd
import gurobipy as gp
import matplotlib
from datetime import datetime
import datetime as dt
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.dates as md
import functools as ft
import cplex
from gurobipy import *
import docplex
import random
import array



start = 0
ende = 96

Periode = list(range(start, ende))
Anzahl_WP = list(range (0,88))

M = 100000
Aufheizfaktor_DHW = 2
loss_DHW = 0.03

m = gp.Model("mip1")

WP_Betrieb_DHW = m.addVars(Periode, Anzahl_WP, vtype=GRB.BINARY, name= "WP_Betrieb_DHW")
WP_Anfahrtvorgang_DHW = m.addVars(Periode, Anzahl_WP,vtype=GRB.BINARY, name = "WP_Anfahrtvorgang_DHW ")
DHW_Speichertemperatur = m.addVars(Periode, Anzahl_WP,lb=43.0, ub= 53.0, vtype=GRB.CONTINUOUS, name = "DHW_Speichertemperatur")
Wärmemenge_DHW = m.addVars(Periode,  Anzahl_WP,lb =0, vtype=GRB.CONTINUOUS, name = "Wärmemenge_DHW")
Stromverbrauch = m.addVars(Periode, Anzahl_WP,lb=0,vtype=GRB.CONTINUOUS, name = "Stromverbrauch")


#m.modelSense =  GRB.MINIMIZE
m.setObjective(sum(WP_Anfahrtvorgang_DHW[i,j] for i in Periode for j in Anzahl_WP))


m.addConstrs((WP_Betrieb_DHW[i,j] * 0.4 <= Stromverbrauch[i,j] 
                for i in Periode for j in Anzahl_WP))

m.addConstrs((WP_Betrieb_DHW[i,j] * 4.0 >= Stromverbrauch[i,j]
                for i in Periode for j in Anzahl_WP))

m.addConstrs((Wärmemenge_DHW[i,j] == (Stromverbrauch[i,j] * 3)
                for i in Periode for j in Anzahl_WP))

m.addConstrs((WP_Anfahrtvorgang_DHW[i,j] >= (WP_Betrieb_DHW[i,j] - WP_Betrieb_DHW[(i-1),j])
                for i in range(start+1,ende) for j in Anzahl_WP))

m.addConstrs((DHW_Speichertemperatur[i,j] == ((DHW_Speichertemperatur[i-1,j] *(1-loss_DHW)) + (Aufheizfaktor_DHW * Wärmemenge_DHW[i,j]))
                    for i in range(start+1,ende) for j in Anzahl_WP))


#m.params.Presolve = 2
#m.params.Prepasses = 5
#m.params.MIPFocus=1
#m.params.MIPGap = 0.05
#m.setParam("TimeLimit", timeLimit)
m.optimize()
print("Runtine = ", m.Runtime)

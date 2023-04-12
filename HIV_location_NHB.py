from gurobipy import *
import pandas as pd
import numpy as np


#load the NHB computed for each facility using POC
aj= pd.read_excel('a_NHB_POC.xlsx',header=None)
aj=np.array(aj)

#load the NHB computed for each facility using LAB
rj= pd.read_excel('r_NHB_LAB.xlsx',header=None) #NHB when tested with LAB
rj=np.array(rj)


# Parameters
district = [1, 2, 3, 4, 5, 6, 7] #Number of districts
health_facilities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
11, 12 ,13, 14, 15, 16, 17, 18, 19, 20,
21, 22 ,23 ,24 ,25 ,26 ,27 ,28 ,29 ,30,
31, 32 ,33 ,34 ,35 ,36 ,37 ,38 ,39 ,40,
41, 42 ,43 ,44 ,45 ,46 ,47 ,48 ,49 ,50,
51, 52 ,53 ,54 ,55 ,56 ,57 ,58 ,59, 60,
61 ,62 ,63 ,64 ,65 ,66 ,67 ,68 ,69 ,70,
71 ,72 ,73 ,74 ,75 ,76 ,77 ,78 ,79 ,80,
81 ,82 ,83 ,84 ,85 ,86 ,87 ,88 ,89 ,90,
91 ,92, 93 ,94 ,95 ,96 ,97 ,98 ,99 ,100,
101 ,102 ,103 ,104 ,105 ,106 ,107 ,108 ,109 ,110,
111 ,112 ,113 ,114 ,115 ,116 ,117 ,118 ,119 ,120,
121, 122] #Number of health facilities >0 demand

num_facilities = len(health_facilities)
district = len(district)


#model formulation
m = Model('facility_location')
select = {}
for j in range(num_facilities):
    select[j] = m.addVar(vtype=GRB.BINARY, lb=0, name="Select")



#Objective diff (gain in net health benefit)
m.setObjective(quicksum(select[j] *(aj[0,j]-rj[0,j]) for j in range(num_facilities)), GRB.MAXIMIZE)


#Constraint
#current number of POC available 11

m.addConstr(quicksum(select[j] for j in range(num_facilities)) <=11, name='NumberofPOC')

m.update()
m.optimize()

selected=[select[j].x for j in range(num_facilities)] # Optimal Placement of Machines

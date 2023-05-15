from gurobipy import *
import pandas as pd
import numpy as np

dem1= pd.read_excel('D1.xlsx',header=None) #Demand for Jan 2019
dem1=np.array(dem1)

dem2= pd.read_excel('D2.xlsx',header=None)  #Demand for Feb 2019
dem2=np.array(dem2)

dem3= pd.read_excel('D3.xlsx',header=None)  #Demand for Mar 2019
dem3=np.array(dem3)

dem4= pd.read_excel('D4.xlsx',header=None)  #Demand for Apr 2019
dem4=np.array(dem4)

dem5= pd.read_excel('D5.xlsx',header=None)  #Demand for May 2019
dem5=np.array(dem5)

dem6= pd.read_excel('D6.xlsx',header=None)  #Demand for Jun 2019
dem6=np.array(dem6)

dem7= pd.read_excel('D7.xlsx',header=None)  #Demand for July 2019
dem7=np.array(dem7)

dem8= pd.read_excel('D8.xlsx',header=None)  #Demand for Aug 2019
dem8=np.array(dem8)

dem9= pd.read_excel('D9.xlsx',header=None)  #Demand for Sep 2019
dem9=np.array(dem9)

dem10= pd.read_excel('D10.xlsx',header=None)  #Demand for Oct 2019
dem10=np.array(dem10)

dem11= pd.read_excel('D11.xlsx',header=None)  #Demand for Nov 2019
dem11=np.array(dem11)

dem12= pd.read_excel('D12.xlsx',header=None)  #Demand for Dec 2019
dem12=np.array(dem12)

dem=[]
for d in range(12):
    dem.append(np.array(eval('dem'+str(d+1))))
dem=np.array(dem)

aj= pd.read_excel('Ai.xlsx',header=None) #ART initiation prob
aj=np.array(aj)

rij= pd.read_excel('Rij.xlsx',header=None) #Increased demand (baseline no increased demand so rij = 1)
rij=np.array(rij)

qij= pd.read_excel('Qij.xlsx',header=None) #result-return POC
qij=np.array(qij)

pij= pd.read_excel('Pij.xlsx',header=None) #result-return Lab
pij=np.array(pij)

vi= pd.read_excel('Vi2.xlsx',header=None) #Test positivity rate
vi=np.array(vi)

yi= pd.read_excel('Yi.xlsx',header=None)   #POC machine utilities
yi=np.array(yi)

# Parameters
patients = [1, 2, 3, 4, 5, 6, 7] #Number of districts
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

t=[1,2,3,4,5,6,7,8,9,10,11,12] #Time
num_facilities = len(health_facilities)
patients = len(patients)
time = len(t)

#model formulation
m = Model('facility_location')
select = {}
for j in range(num_facilities):
    select[j] = m.addVar(vtype=GRB.BINARY, lb=0, name="Select")

#Objective
m.setObjective(quicksum(select[j] * yi[i,0] *rij[i, j] * aj[0,j] * vi[i,0]  * qij[i, j] * dem[t,i, j] for t in range(time) for j in range(num_facilities) for i in range(patients)) + quicksum((1-select[j])  * pij[i, j] * aj[0,j] * vi[i,0] * dem[t,i, j] for t in range(time) for j in range(num_facilities) for i in range(patients)), GRB.MAXIMIZE)

#Constraint
m.addConstr(quicksum(select[j] for j in range(num_facilities)) == 11, name='NumberofPOC')

m.update()
m.optimize()

selected=[select[j].x for j in range(num_facilities)] # Optimal Placement of Machines


#END OF OPT CODE############################################################

#PLACEMENT PLANS
#Upper POC func
select =[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

#Lower POC func
select =[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

#MiddlePOC func (baseline)
select =[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

#Current location
select=[1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	1,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1.176,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]

#Heuristic 1
select=[1,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]

#Heuristic 2
select=[1,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	1,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	1,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]

#Heuristic 3
select=[1,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	1,	0,	0,	0,	1,	0,	0,	1,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0]

#Heuristic 4
select= [1,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0]

#Check Objective for Other Placements
a=quicksum(select[j] * yi[i,0]* rij[i, j] * aj[0,j] * vi[i,0] * qij[i, j]  * dem[t,i, j] for t in range(time) for j in range(num_facilities) for i in range(patients)) + quicksum((1-select[j])   * pij[i, j] * aj[0,j] * vi[i,0]  * dem[t,i, j] for t in range(time) for j in range(num_facilities) for i in range(patients))

result_return_POC= quicksum(select[j] * yi[i,0] * vi[i,0] * rij[i, j] * qij[i, j] * dem[t,i, j] for t in range(time) for j in range(num_facilities) for i in range(patients))
result_return_Lab= quicksum((1-select[j])  * pij[i, j] * vi[i,0] * dem[t,i, j] for t in range(time) for j in range(num_facilities) for i in range(patients))
result_return=result_return_POC+result_return_Lab

#Obj for each District 
i=5 #Number of district 0 to 6 (alphabetical order)
b=quicksum(select[j] * yi[i,0]* rij[i, j] * aj[0,j] * vi[i,0] * qij[i, j]  * dem[t,i, j] for t in range(time) for j in range(num_facilities)) + quicksum((1-select[j])   * pij[i, j] * aj[0,j] * vi[i,0]  * dem[t,i, j] for t in range(time) for j in range(num_facilities))
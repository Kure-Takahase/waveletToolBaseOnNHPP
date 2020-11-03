import DT_WSE
import SRMtool
from scipy.optimize import minimize_scalar

# python c:\\xampp\\htdocs\\waveletShrinkage.py
filename = 'C:\\xampp\\htdocs\\DS1.txt'
thresholdMode = 's'
thresholdName = 'lht'

data = SRMtool.getData(filename)

'''
res = DT_WSE.HAT(filename,thresholdMode,thresholdName,1)

mes1 = SRMtool.MSE(SRMtool.toCulData(res),SRMtool.toCulData(data))
mes2 = SRMtool.MSE(res,data)
print("当前:")
print("%.3f %.3f" % (mes1,mes2))
print("目标:")
print("0.115 0.010")
#print("0.191 0.036")
'''
group = data[0:32]
A_group = DT_WSE.AnscombeTransformFromGroup(group,1)
lht_last = DT_WSE.AnscombeTransformFromGroup([data[32],],1)[0]
print(lht_last)
lht_last = A_group[0]
print(lht_last)
i = 0
while i < 1:
	lost = DT_WSE.lostFunction(i,A_group,lht_last)
	#print(lost)
	i = i + 0.1
#print(A_group)
i = 1
while i < 6:
	lost = DT_WSE.lostFunction(i,A_group,lht_last)
	#print(lost)
	i = i + 1

#print("MVP")
lost = DT_WSE.lostFunction(0.17,A_group,lht_last)
#print(lost)

bounds=(0, 3)
#print(D)

import numpy as np
from scipy.optimize import minimize

x0 = np.array([0])
res = minimize(DT_WSE.lostFunction, x0,(A_group,lht_last), method='nelder-mead',
               options={'xatol': 1e-8, 'disp': True})
print("123")
resu = minimize_scalar(DT_WSE.lostFunction,args=(A_group,lht_last), method='brent')
print(resu)


import DT_WSE,SRMtool,copy,math
from scipy.optimize import minimize_scalar
#import time
#import random

'''
#python c:\\xampp\\htdocs\\test.py C:\\xampp\\htdocs\\DS1.txt
#pypy3 c:\\xampp\\htdocs\\test.py
#预测调试代码
filename = 'DS1.txt'

filename = 'C:\\xampp\\htdocs\\DS1.txt'
weightMethods = ['none','boxcar','Gaussian','Epanechnikov','tricube']
costMethods = ['origin','denoise'];
costDataMethods = ['quota','grow'];
thresholdMethods = ['ut','ldt'];
thresholdRules = ['s','h'];
dataTransforms = ['TranslationInvariant','Bartlett','Fisz','Anscombe'];
predictionIntervals = [3/10,5/10,7/10];
vares = [1/4,1]

weightMethods = ['none']
costMethods = ['origin'];
costDataMethods = ['quota'];
thresholdMethods = ['ut'];
thresholdRules = ['s'];
dataTransforms = ['Anscombe'];
predictionIntervals = [3/10];
vares = [1/4]

#DT_WSE.predictionTest(filename,weightMethods,costMethods,costDataMethods,thresholdMethods,thresholdRules,dataTransforms,predictionIntervals,vares)
#DT_WSE.predictionMultiThreadingTest(filename,weightMethods,costMethods,costDataMethods,thresholdMethods,thresholdRules,dataTransforms,predictionIntervals,vares)
'''

import numpy as np
from scipy.optimize import minimize
from scipy.optimize import Bounds

# python c:\\xampp\\htdocs\\test.py


#原方法
#获取下一天的预测值
dataTransform = 'Anscombe'
thresholdRule = 's'
thresholdMethod = 'ut'
weightMethod = 'boxcar'
h = 1.1
var = 1
filename = 'C:\\xampp\\htdocs\\DS1.txt'
predictionInterval = 0.3

data = SRMtool.getData(filename)
#after_data = data[43:62]
groupLength = len(data)
predictionPoint = math.floor(groupLength * predictionInterval);
after_data = data[predictionPoint: groupLength];
print(len(after_data))
data = data[0: predictionPoint];
#data = data[0:43]#0号下标元素开始，到第20个元素。总共20个元素
data = copy.deepcopy(data);
max_data = max(data) * 5;
#print(max_data)
bounds=(0, max_data);
arg = (data,dataTransform,thresholdRule,thresholdMethod,weightMethod,h,var)
#res = minimize_scalar(DT_WSE.prediction_cost1,None,bounds,arg, method='bounded')
#print(res.x)
'''
#多元方法
def rosen(x):
    """The Rosenbrock function"""
    return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)
def Get_Average(list):
   sum = 0
   for item in list:     
      sum += item  
   return sum/len(list)

ave = Get_Average(data)+1
print(ave)
i = 0;
x0list = []          ## 空列表
while i < 19:
	x0list.append(ave)
	i = i + 1
x0 = np.array(x0list)
res = minimize(DT_WSE.prediction_cost3, x0,arg,method='nelder-mead',
               options={'xatol': 1e-8, 'disp': False})
print(res.x)
print(after_data)
'''

'''
x0 = np.array([1.3, 0.7, 0.8, 1.9, 1.2])
res = minimize(rosen, x0, method='nelder-mead',
               options={'xatol': 1e-8, 'disp': True})
'''
# python c:\\xampp\\htdocs\\test.py

result = DT_WSE.costPrediction(data,'origin','grow',weightMethod,h,groupLength - predictionPoint,dataTransform,thresholdRule,thresholdMethod,var)
result = result[predictionPoint: groupLength];
print(len(after_data))
print(len(result))
mse1 = SRMtool.MSE(after_data,result);
mse2 = SRMtool.MSE(SRMtool.toCulData(after_data),SRMtool.toCulData(result));
print(mse1)
print(mse2)

'''
i = 0;
x0list = []          ## 空列表
while i < len(result):
	x0list.append(result[i])
	i = i + 1
print(x0list[len(x0list)-1])
print(result[len(result)-1])
x0 = np.array(x0list)
arg = (data,'Fisz',thresholdRule,'ut','none',h,var)
res = minimize(DT_WSE.prediction_cost3, x0,arg,method='nelder-mead',
               options={'xatol': 1e-8, 'disp': False})

print(res.x)
print(after_data)

mse1 = SRMtool.MSE(after_data,res.x);
mse2 = SRMtool.MSE(SRMtool.toCulData(after_data),SRMtool.toCulData(res.x));
print(mse1)
print(mse2)
'''











'''
#预测调试代码2
result1 = DT_WSE.getPrediction1(o_data[0:30],31,'Anscombe','s','ut')
result2 = DT_WSE.getPrediction2(o_data[0:30],31,'Anscombe','s','ut')


i = 0;
while(i < len(o_data)):
	print(str(round(result1[i],3))+" "+str(round(result2[i],3))+" "+str(round(o_data[i],3)));
	i = i + 1;


o_data = o_data[31: 61];
result1 = result1[31: 61];
result2 = result2[31: 61];
mse2_2 = SRMtool.MSE(o_data,result2);
mse2_1 = SRMtool.MSE(SRMtool.toCulData(o_data),SRMtool.toCulData(result2));
print(str(round(mse2_2,3))+" "+str(round(mse2_1,3))+" denoise_quota_Anscombe");

mse1_2 = SRMtool.MSE(o_data,result1);
mse1_1 = SRMtool.MSE(SRMtool.toCulData(o_data),SRMtool.toCulData(result1));
print(str(round(mse1_2,3))+" "+str(round(mse1_1,3))+" origin_quota_Anscombe");
'''

'''
#调试lht代码
#filename = sys.argv[1];
filename = 'C:\\xampp\\htdocs\\DS1.txt'
origin_data = SRMtool.getData(filename);
result = DT_WSE.HFT(filename,'s','lht');
#print(result)
mse2 = SRMtool.MSE(origin_data,result);
mse1 = SRMtool.MSE(SRMtool.toCulData(origin_data),SRMtool.toCulData(result));
print(str(round(mse1,3))+" "+str(round(mse2,3))+" HFT");
'''

'''
print(Ds[0][0])
groupLength = len(Ds[0][0])
bounds=(0, 20)
print(DT_WSE.lostFunction_1(0.25,Ds[0][0]))
res = minimize_scalar(DT_WSE.lostFunction_1,None,bounds,Ds[0][0], method='bounded')
print(res)


bounds=(0, 20)
print(DT_WSE.lostFunction_1(0.25,Ds[0][0]))
res = minimize_scalar(DT_WSE.lostFunction_1,None,bounds,Ds[0][0], method='bounded')
print(res)

'''
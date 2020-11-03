import SRMtool
import DT_WSE
import math
import numpy as np
from scipy.optimize import minimize

# 设置任务名
taskName = 'DS1_pre'
# 设置待处理的数据
fileName = 'C:\\xampp\\htdocs\\DS4.txt'
# 设置参数文件
paraFileName = 'C:\\xampp\\htdocs\\multi_para1.txt'

# 设置Task所需依赖包
libFiles = ('SRMtool','DT_WSE')

# 设置结果保存excel表的所有工作簿的名称元组
workbookNames = ('PredictionResult_3','PredictionStudy_3','PredictionResult_5','PredictionStudy_5','PredictionResult_7','PredictionStudy_7')

# 设置每个工作簿内的列名元组
PredictionResult_3 = ()
PredictionStudy_3 = ('MSE1','MSE2','weightMethods','costMethods','costDataMethods','thresholdMethods','thresholdRules','dataTransforms','predictionIntervals','vares','bandwidth','fullName')
PredictionResult_5 = ()
PredictionStudy_5 = PredictionStudy_3
PredictionResult_7 = ()
PredictionStudy_7 = PredictionStudy_3
# 将每个工作簿内的列名元组汇总为一个元组
workbookRawNames = (PredictionResult_3,PredictionStudy_3,PredictionResult_5,PredictionStudy_5,PredictionResult_7,PredictionStudy_7)

#读取数据文件方法
def readDataFunction(dataFile):
	o_data = SRMtool.getData(dataFile)
	return (tuple(o_data),)

#读取参数文件方法
def readParaFunction(ParaFile):
	paraTuple = SRMtool.multi_ReadParaFunction(ParaFile)
	return paraTuple

#Task方法
def taskFunction(dataTuple,paraTuple):
	# 读取参数
	weightMethod = paraTuple[0]
	costMethod = paraTuple[1]
	costDataMethod = paraTuple[2]
	thresholdMethod = paraTuple[3]
	thresholdRule = paraTuple[4]
	dataTransform = paraTuple[5]
	predictionInterval = paraTuple[6]
	var = paraTuple[7]
	# 预准备,分割数据
	o_data = list(dataTuple)
	groupLength = len(o_data);
	predictionPoint = math.floor(groupLength * predictionInterval);
	ahead_data = o_data[0: predictionPoint];
	after_data = o_data[predictionPoint: groupLength];
	# 开始计算
	h = 1.1
	if(weightMethod == 'none'):
		h = -1;
	if(dataTransform == 'TranslationInvariant'):
		var = -1;
	result = DT_WSE.costPrediction(ahead_data,costMethod,costDataMethod,weightMethod,h,groupLength - predictionPoint,dataTransform,thresholdRule,thresholdMethod,var);
	'''
	#加强版
	if(dataTransform == 'TranslationInvariant' and thresholdMethod == 'ut') or (dataTransform != 'TranslationInvariant' and thresholdMethod == 'ldt'):
		pass
	else:
		result1 = result[predictionPoint: groupLength];
		i = 0;
		x0list = []          ## 空列表
		while i < len(result1):
			x0list.append(result1[i])
			i = i + 1
		x0 = np.array(x0list)
		arg = (ahead_data,'Fisz',thresholdRule,'ut','none',h,var)
		res = minimize(DT_WSE.prediction_cost3, x0,arg,method='nelder-mead',
		               options={'xatol': 1e-8, 'disp': False})
		i = 0;
		for re in res.x:
			result[predictionPoint + i] = re;
			i = i + 1
	'''
	#分析结果
	ahead  = result[0 : predictionPoint];
	after_result = result[predictionPoint: groupLength];
	parameterCombination = "PredictionInterval:"+str(predictionInterval)+" "+costMethod+"_"+costDataMethod+"_"+dataTransform+"_"+weightMethod+"_"+thresholdRule+"_"+thresholdMethod+"_var="+str(var)+"_h="+str(h)
	mse1 = SRMtool.MSE(after_data,after_result);
	mse2 = SRMtool.MSE(SRMtool.toCulData(after_data),SRMtool.toCulData(after_result));
	PredictionStudyTuple = (mse1,mse2)+paraTuple+(h,parameterCombination)
	PredictionResultTuple = (result,parameterCombination)
	return (PredictionResultTuple,PredictionStudyTuple,predictionInterval)

#结果保存方法
def saveFunction(taskResultTuple):
	#保存分析结果(接TaskFunction)
	predictionInterval = taskResultTuple[2]
	if(predictionInterval == 0.3):
		workbookNum = 0
	if(predictionInterval == 0.5):
		workbookNum = 1
	if(predictionInterval == 0.7):
		workbookNum = 2
	#第二个参数为False时，表示写入一列数据(从第一列起,纵向写入),此时需指定列名.应由第四个元素给出.
	PredictionResultTuple = (workbookNum * 2,False,taskResultTuple[0][0],taskResultTuple[0][1])
	#第二个参数为True时,表示写入一行数据(从第二行开始写起，不用指定列名)
	PredictionStudyTuple = (workbookNum * 2 + 1,True,taskResultTuple[1])
	return (PredictionResultTuple,PredictionStudyTuple)

#若不满意系统提供的结果保存框架或其他，亦可自行处理
def finalCust(taskResultTuples):
	print("这里是finalCust")
	pass

#-------------------------------------------------------------------------#
#python c:\\xampp\\htdocs\\multi_DTWSE.py

'''

# 设置待处理的数据
fileName = 'C:\\xampp\\htdocs\\DS1.txt'
dataTuples = readDataFunction(fileName)
# 设置参数文件
paraFileName = 'C:\\xampp\\htdocs\\multi_para2.txt'
paraTuples = readParaFunction(paraFileName)
print(paraTuples)
# 运行一个Task
paraTuple = paraTuples[0]
dataTuple = dataTuples[0]
resTuple = taskFunction(dataTuple,paraTuple)
# 计算结果转换为数据记录指令
saveTuple = saveFunction(resTuple)

print(saveTuple[0])
print(saveTuple[1])

'''






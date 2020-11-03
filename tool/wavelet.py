import DT_WSE
import sys
import time
import random
import xlsxwriter
import SRMtool

#参数读取
filename = sys.argv[1];
mode = sys.argv[2]; #mode = 1时，执行所有组合，非1时指定特定组合
if( mode != '1'):
	dataTransform = sys.argv[3];
	thresholdRule = sys.argv[4];
	thresholdMethod = sys.argv[5];
	var = sys.argv[6];
#excel准备写入
col = 0;
res_filename = str(time.time()) + str(random.randint(0,9999)) + ".xlsx";
desktop_path = '/var/www/html/wavelet/'+res_filename;
desktop_path = "C:\\xampp\\htdocs\\" + res_filename;
workbook = xlsxwriter.Workbook(desktop_path)
worksheet = workbook.add_worksheet('Result');
worksheet2 = workbook.add_worksheet('NumericalStudy');
worksheet2.write(0, 0, 'Method');
worksheet2.write(0, 1, 'MSE_cumulative_time');
worksheet2.write(0, 2, 'MSE_time_interval');
worksheet2.write(0, 3, 'MLL');

worksheet2.set_column(0, 0, 30);
worksheet2.set_column(1, 3, 20);
#读取原始数据并写入excel
origin_data = SRMtool.getData(filename);
i = 1;
worksheet.set_column(col, col, 20);
worksheet.write(0, col, 'originData')
for data in origin_data:
	worksheet.write(i, col, data)
	i = i + 1;
col = col + 1; #写完一列就换列
#数据处理

#全排列组合
if(mode == '1'):
	thresholdRules = ['s','h']
	#thresholdMethods = ['ut','lht','ldt']
	thresholdMethods = ['ut','ldt']
	dataTransforms = ['Anscombe','Fisz','Bartlett','TranslationInvariant']
	vares = [1/4,1];
	for dataTransform in dataTransforms:
		for thresholdMethod in thresholdMethods:
			for thresholdRule in thresholdRules :
				for var in vares:
					if(dataTransform == 'Anscombe'):
						result = DT_WSE.HAT(filename,thresholdRule,thresholdMethod,var)
					elif(dataTransform == 'Fisz'):
						result = DT_WSE.HFT(filename,thresholdRule,thresholdMethod,var)
					elif(dataTransform == 'Bartlett'):
						result = DT_WSE.HBT(filename,thresholdRule,thresholdMethod,var)
					elif(dataTransform == 'TranslationInvariant'):
						result = DT_WSE.HTI(filename,thresholdRule,thresholdMethod)
					#print("9")
					i = 1
					worksheet.set_column(col, col, 27);
					worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
					for data in result:
						worksheet.write(i, col, data)
						i = i + 1;
					mse2 = SRMtool.MSE(origin_data,result);
					mse1 = SRMtool.MSE(SRMtool.toCulData(origin_data),SRMtool.toCulData(result));
					#mll  = SRMtool.MLL2(origin_data,result);
					mll = 1;
					print(str(round(mse1,3))+" "+str(round(mse2,3))+" "+str(round(mll,3))+" "+dataTransform+"_"+thresholdRule+"_"+thresholdMethod+"_"+str(var))
					worksheet2.write(col, 0, dataTransform+"_"+thresholdRule+"_"+thresholdMethod);
					worksheet2.write(col, 1, mse1);
					worksheet2.write(col, 2, mse2);
					worksheet2.write(col, 3, mll);
					col = col + 1; #写完一列就换列
#某一组合
else:
	if(dataTransform == 'Anscombe'):
		result = DT_WSE.HAT(filename,thresholdRule,thresholdMethod,var)
	elif(dataTransform == 'Fisz'):
		result = DT_WSE.HFT(filename,thresholdRule,thresholdMethod)
	elif(dataTransform == 'Bartlett'):
		result = DT_WSE.HBT(filename,thresholdRule,thresholdMethod,var)
	elif(dataTransform == 'TranslationInvariant'):
		result = DT_WSE.HTI(filename,thresholdRule,thresholdMethod)
	else :
		sys.exit(1);
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	mse2 = SRMtool.MSE(origin_data,result);
	mse1 = SRMtool.MSE(SRMtool.toCulData(origin_data),SRMtool.toCulData(result));
	mll  = SRMtool.MLL2(origin_data,result);
	print(str(round(mse1,3))+" "+str(round(mse2,3))+" "+str(round(mll,3))+" "+dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	worksheet2.write(col, 0, dataTransform+"_"+thresholdRule+"_"+thresholdMethod);
	worksheet2.write(col, 1, mse1);
	worksheet2.write(col, 2, mse2);
	worksheet2.write(col, 3, mll);

#预测
worksheet3 = workbook.add_worksheet('PredictionStudy');
h = 20;
ahead_data = origin_data[0: 31];
after_data = origin_data[31: 62];
i = 1;
col = 0;
worksheet3.set_column(col, col, 20);
worksheet3.write(0, col, 'originData')
for data in origin_data:
	worksheet3.write(i, col, data)
	i = i + 1;
col = col + 1;
#开始预测
results = DT_WSE.costPrediction(ahead_data,'denoise','grow','boxcar',1.1,31,'Fisz','s','ut',1/4);
#写入预测值 单日
i = 1;
col = 0;
worksheet3.set_column(col, col, 20);
worksheet3.write(0, col, 'originData')
for data in origin_data:
	worksheet3.write(i, col, data)
	i = i + 1;
col = col + 1;
i = 1;
worksheet3.set_column(col, col, 20);
worksheet3.write(0, col, 'Prediction')
for data in results:
	worksheet3.write(i, col, data)
	i = i + 1;
col = col + 1;
results_cul = SRMtool.toCulData(results);
origin_data_cul = SRMtool.toCulData(origin_data);
results = results[31:62];
i = 0;
while i < len(results):
	print(str(results[i])+" "+str(after_data[i]));
	i = i + 1
mse1 = SRMtool.MSE(after_data,results);
mse2 = SRMtool.MSE(SRMtool.toCulData(after_data),SRMtool.toCulData(results));
print(str(round(mse1,3))+" "+str(round(mse2,3)));
#累计
i = 1;
worksheet3.set_column(col, col, 20);
worksheet3.write(0, col, 'originData_cul')
for data in origin_data_cul:
	worksheet3.write(i, col, data)
	i = i + 1;
col = col + 1;
i = 1;
worksheet3.set_column(col, col, 20);
worksheet3.write(0, col, 'Prediction_cul')
for data in results_cul:
	worksheet3.write(i, col, data)
	i = i + 1;
col = col + 1;


workbook.close();
print(res_filename);

#python c:\\xampp\\htdocs\\wavelet.py c:\\xampp\\htdocs\\DS1.txt 1
#旧版
'''
#Anscombe_s_ut
if (dataTransform == 'Anscombe' and thresholdMethod == 'ut' and thresholdRule == 's') or mode == '1':
	dataTransform = 'Anscombe';
	thresholdMethod = 'ut';
	thresholdRule = 's';
	#print("1")
	result = DT_WSE.HAT(filename,thresholdRule,thresholdMethod)
	#print("9")
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	mse2 = SRMtool.MSE(origin_data,result);
	mse1 = SRMtool.MSE(SRMtool.toCulData(origin_data),SRMtool.toCulData(result));
	print(str(round(mse1,3))+" "+str(round(mse2,3))+" "+dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	worksheet2.write(col, 0, dataTransform+"_"+thresholdRule+"_"+thresholdMethod);
	worksheet2.write(col, 1, mse1);
	worksheet2.write(col, 2, mse2);
	col = col + 1; #写完一列就换列
#Anscombe_h_ut
if (dataTransform == 'Anscombe' and thresholdMethod == 'ut' and thresholdRule == 'h') or mode == '1':
	dataTransform = 'Anscombe';
	thresholdMethod = 'ut';
	thresholdRule = 'h';
	result = DT_WSE.HAT(filename,thresholdRule,thresholdMethod)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	mse2 = SRMtool.MSE(origin_data,result);
	mse1 = SRMtool.MSE(SRMtool.toCulData(origin_data),SRMtool.toCulData(result));
	#print(str(round(mse1,3))+" "+str(round(mse2,3))+" "+dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	worksheet2.write(col, 0, dataTransform+"_"+thresholdRule+"_"+thresholdMethod);
	worksheet2.write(col, 1, mse1);
	worksheet2.write(col, 2, mse2);
	col = col + 1; #写完一列就换列
#Anscombe_s_lht
if(dataTransform == 'Anscombe' and thresholdMethod == 'lht' and thresholdRule == 's') or mode == '1':
	dataTransform = 'Anscombe';
	thresholdMethod = 'lht';
	thresholdRule = 's';
	result = DT_WSE.HAT(filename,thresholdRule,thresholdMethod)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	mse2 = SRMtool.MSE(origin_data,result);
	mse1 = SRMtool.MSE(SRMtool.toCulData(origin_data),SRMtool.toCulData(result));
	print(str(round(mse1,3))+" "+str(round(mse2,3))+" "+dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	worksheet2.write(col, 0, dataTransform+"_"+thresholdRule+"_"+thresholdMethod);
	worksheet2.write(col, 1, mse1);
	worksheet2.write(col, 2, mse2);
	col = col + 1; #写完一列就换列
#Anscombe_h_lht
if(dataTransform == 'Anscombe' and thresholdMethod == 'lht' and thresholdRule == 'h') or mode == '1':
	dataTransform = 'Anscombe';
	thresholdMethod = 'lht';
	thresholdRule = 'h';
	result = DT_WSE.HAT(filename,thresholdRule,thresholdMethod)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	mse2 = SRMtool.MSE(origin_data,result);
	mse1 = SRMtool.MSE(SRMtool.toCulData(origin_data),SRMtool.toCulData(result));
	worksheet2.write(col, 0, dataTransform+"_"+thresholdRule+"_"+thresholdMethod);
	worksheet2.write(col, 1, mse1);
	worksheet2.write(col, 2, mse2);
	col = col + 1; #写完一列就换列
#Fisz_s_ut
if(dataTransform == 'Fisz' and thresholdMethod == 'ut' and thresholdRule == 's') or mode == '1':
	dataTransform = 'Fisz';
	thresholdMethod = 'ut';
	thresholdRule = 's';
	result = DT_WSE.HFT(filename,thresholdRule,thresholdMethod)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	mse2 = SRMtool.MSE(origin_data,result);
	mse1 = SRMtool.MSE(SRMtool.toCulData(origin_data),SRMtool.toCulData(result));
	print(str(round(mse1,3))+" "+str(round(mse2,3))+" "+dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	worksheet2.write(col, 0, dataTransform+"_"+thresholdRule+"_"+thresholdMethod);
	worksheet2.write(col, 1, mse1);
	worksheet2.write(col, 2, mse2);
	col = col + 1; #写完一列就换列
#Fisz_h_ut
if(dataTransform == 'Fisz' and thresholdMethod == 'ut' and thresholdRule == 'h') or mode == '1':
	dataTransform = 'Fisz';
	thresholdMethod = 'ut';
	thresholdRule = 'h';
	result = DT_WSE.HFT(filename,thresholdRule,thresholdMethod)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	mse2 = SRMtool.MSE(origin_data,result);
	mse1 = SRMtool.MSE(SRMtool.toCulData(origin_data),SRMtool.toCulData(result));
	#print(str(round(mse1,3))+" "+str(round(mse2,3))+" "+dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	worksheet2.write(col, 0, dataTransform+"_"+thresholdRule+"_"+thresholdMethod);
	worksheet2.write(col, 1, mse1);
	worksheet2.write(col, 2, mse2);
	col = col + 1; #写完一列就换列
#Fisz_s_lht
if(dataTransform == 'Fisz' and thresholdMethod == 'lht' and thresholdRule == 's') or mode == '1':
	dataTransform = 'Fisz';
	thresholdMethod = 'lht';
	thresholdRule = 's';
	result = DT_WSE.HFT(filename,thresholdRule,thresholdMethod)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	mse2 = SRMtool.MSE(origin_data,result);
	mse1 = SRMtool.MSE(SRMtool.toCulData(origin_data),SRMtool.toCulData(result));
	print(str(round(mse1,3))+" "+str(round(mse2,3))+" "+dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	worksheet2.write(col, 0, dataTransform+"_"+thresholdRule+"_"+thresholdMethod);
	worksheet2.write(col, 1, mse1);
	worksheet2.write(col, 2, mse2);
	col = col + 1; #写完一列就换列
#Fisz_h_lht
if(dataTransform == 'Fisz' and thresholdMethod == 'lht' and thresholdRule == 'h') or mode == '1':
	dataTransform = 'Fisz';
	thresholdMethod = 'lht';
	thresholdRule = 'h';
	result = DT_WSE.HFT(filename,thresholdRule,thresholdMethod)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	mse2 = SRMtool.MSE(origin_data,result);
	mse1 = SRMtool.MSE(SRMtool.toCulData(origin_data),SRMtool.toCulData(result));
	worksheet2.write(col, 0, dataTransform+"_"+thresholdRule+"_"+thresholdMethod);
	worksheet2.write(col, 1, mse1);
	worksheet2.write(col, 2, mse2);
	col = col + 1; #写完一列就换列
#Bartlett_s_ut
if(dataTransform == 'Bartlett' and thresholdMethod == 'ut' and thresholdRule == 's') or mode == '1':
	dataTransform = 'Bartlett';
	thresholdMethod = 'ut';
	thresholdRule = 's';
	result = DT_WSE.HBT_ut(filename,thresholdRule)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	mse2 = SRMtool.MSE(origin_data,result);
	mse1 = SRMtool.MSE(SRMtool.toCulData(origin_data),SRMtool.toCulData(result));
	worksheet2.write(col, 0, dataTransform+"_"+thresholdRule+"_"+thresholdMethod);
	#print(str(round(mse1,3))+" "+str(round(mse2,3))+" "+dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	worksheet2.write(col, 1, mse1);
	worksheet2.write(col, 2, mse2);
	col = col + 1; #写完一列就换列
#Bartlett_h_ut
if(dataTransform == 'Bartlett' and thresholdMethod == 'ut' and thresholdRule == 'h') or mode == '1':
	dataTransform = 'Bartlett';
	thresholdMethod = 'ut';
	thresholdRule = 'h';
	result = DT_WSE.HBT_ut(filename,thresholdRule)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	mse2 = SRMtool.MSE(origin_data,result);
	mse1 = SRMtool.MSE(SRMtool.toCulData(origin_data),SRMtool.toCulData(result));
	worksheet2.write(col, 0, dataTransform+"_"+thresholdRule+"_"+thresholdMethod);
	worksheet2.write(col, 1, mse1);
	worksheet2.write(col, 2, mse2);
	col = col + 1; #写完一列就换列
#Bartlett_s_lht	
if(dataTransform == 'Bartlett' and thresholdMethod == 'lht' and thresholdRule == 's') or mode == '1':
	dataTransform = 'Bartlett';
	thresholdMethod = 'lht';
	thresholdRule = 's';
	result = DT_WSE.HBT_lht(filename,thresholdRule)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	mse2 = SRMtool.MSE(origin_data,result);
	mse1 = SRMtool.MSE(SRMtool.toCulData(origin_data),SRMtool.toCulData(result));
	worksheet2.write(col, 0, dataTransform+"_"+thresholdRule+"_"+thresholdMethod);
	worksheet2.write(col, 1, mse1);
	worksheet2.write(col, 2, mse2);
	col = col + 1; #写完一列就换列
#Bartlett_h_lht	
if(dataTransform == 'Bartlett' and thresholdMethod == 'lht' and thresholdRule == 'h') or mode == '1':
	dataTransform = 'Bartlett';
	thresholdMethod = 'lht';
	thresholdRule = 'h';
	result = DT_WSE.HBT_lht(filename,thresholdRule)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	mse2 = SRMtool.MSE(origin_data,result);
	mse1 = SRMtool.MSE(SRMtool.toCulData(origin_data),SRMtool.toCulData(result));
	worksheet2.write(col, 0, dataTransform+"_"+thresholdRule+"_"+thresholdMethod);
	worksheet2.write(col, 1, mse1);
	worksheet2.write(col, 2, mse2);
	col = col + 1; #写完一列就换列

workbook.close();
print(res_filename);
'''
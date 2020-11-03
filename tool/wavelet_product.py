import DT_WSE
import sys
import json
import time
import random
import xlsxwriter
filename = sys.argv[1];
dataTransform = sys.argv[2];
thresholdRule = sys.argv[3];
thresholdMethod = sys.argv[4];
mode = sys.argv[5];
col = 0;
res_filename = str(time.time()) + str(random.randint(0,9999)) + ".xlsx";
desktop_path = '/var/www/html/wavelet/'+res_filename;
#desktop_path = "C:\\xampp\\htdocs\\" + res_filename;
workbook = xlsxwriter.Workbook(desktop_path)
worksheet = workbook.add_worksheet('result');
origin_data = DT_WSE.getData(filename);
i = 1;
worksheet.set_column(col, col, 20);
worksheet.write(0, col, 'originData')
for data in origin_data:
	worksheet.write(i, col, data)
	i = i + 1;
col = col + 1;
#Anscombe_s_ut
if (dataTransform == 'Anscombe' and thresholdMethod == 'ut' and thresholdRule == 's') or mode == '1':
	dataTransform = 'Anscombe';
	thresholdMethod = 'ut';
	thresholdRule = 's';
	result = DT_WSE.HAT_ut(filename,thresholdRule)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	col = col + 1;
#Anscombe_h_ut
if (dataTransform == 'Anscombe' and thresholdMethod == 'ut' and thresholdRule == 'h') or mode == '1':
	dataTransform = 'Anscombe';
	thresholdMethod = 'ut';
	thresholdRule = 'h';
	result = DT_WSE.HAT_ut(filename,thresholdRule)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	col = col + 1;
#Anscombe_s_lht
if(dataTransform == 'Anscombe' and thresholdMethod == 'lht' and thresholdRule == 's') or mode == '1':
	dataTransform = 'Anscombe';
	thresholdMethod = 'lht';
	thresholdRule = 's';
	result = DT_WSE.HAT_lht(filename,thresholdRule)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	col = col + 1;
#Anscombe_h_lht
if(dataTransform == 'Anscombe' and thresholdMethod == 'lht' and thresholdRule == 'h') or mode == '1':
	dataTransform = 'Anscombe';
	thresholdMethod = 'lht';
	thresholdRule = 'h';
	result = DT_WSE.HAT_lht(filename,thresholdRule)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	col = col + 1;
#Fisz_s_ut
if(dataTransform == 'Fisz' and thresholdMethod == 'ut' and thresholdRule == 's') or mode == '1':
	dataTransform = 'Fisz';
	thresholdMethod = 'ut';
	thresholdRule = 's';
	result = DT_WSE.HFT_ut(filename,thresholdRule)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	col = col + 1;
#Fisz_h_ut
if(dataTransform == 'Fisz' and thresholdMethod == 'ut' and thresholdRule == 'h') or mode == '1':
	dataTransform = 'Fisz';
	thresholdMethod = 'ut';
	thresholdRule = 'h';
	result = DT_WSE.HFT_ut(filename,thresholdRule)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	col = col + 1;
#Fisz_s_lht
if(dataTransform == 'Fisz' and thresholdMethod == 'lht' and thresholdRule == 's') or mode == '1':
	dataTransform = 'Fisz';
	thresholdMethod = 'lht';
	thresholdRule = 's';
	result = DT_WSE.HFT_lht(filename,thresholdRule)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	col = col + 1;
#Fisz_h_lht
if(dataTransform == 'Fisz' and thresholdMethod == 'lht' and thresholdRule == 'h') or mode == '1':
	dataTransform = 'Fisz';
	thresholdMethod = 'lht';
	thresholdRule = 'h';
	result = DT_WSE.HFT_lht(filename,thresholdRule)
	i = 1
	worksheet.set_column(col, col, 20);
	worksheet.write(0, col, dataTransform+"_"+thresholdRule+"_"+thresholdMethod)
	for data in result:
		worksheet.write(i, col, data)
		i = i + 1;
	col = col + 1;
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
	col = col + 1;
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
	col = col + 1;
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
	col = col + 1;
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
	col = col + 1;

workbook.close();
print(res_filename);
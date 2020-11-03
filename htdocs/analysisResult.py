import xlrd,xlsxwriter,sys,random,time

# 合并文件
# 将多个经过基础分析的文件合并为一个文件
def analysis_merge(args,sheetSum,dataSetSum):
	nowSheet = 0
	sheetNames = ('weightMethods_origin','weightMethods_denoise','costDataMethods_origin','costDataMethods_denoise',
		'thresholdMethods_origin','thresholdMethods_denoise','thresholdRules_origin','thresholdRules_denoise'
		,'dataTransforms_origin','dataTransforms_denoise','vares_origin','vares_denoise')
	bookNames = ('weightMethods','weightMethods',
		'costDataMethods','costDataMethods','thresholdMethods','thresholdMethods',
		'thresholdRules','thresholdRules','dataTransforms','dataTransforms','vares','vares')
	predictionInterval = (0.3,0.5,0.7)
	# 设定数据集名称
	dataName = str(dataSetSum)
	# 创建excel文件
	desktop_path = sys.path[0]+"\\excel_save\\"
	# 不附加末尾随机数字
	excel_fileName = "合并_"+dataName+".xlsx"
	# 附加末尾随机数字
	excel_fileName = "合并_"+dataName+'_'+str(int(time.time()))+str(random.randint(0,9999))+ ".xlsx" 
	desktop_path = desktop_path + excel_fileName;
	workbook = xlsxwriter.Workbook(desktop_path)
	mse_format = workbook.add_format({
	    'align': 'center',  # 水平对齐方式
	    'valign': 'vcenter',  # 垂直对齐方式
	    'left':1,
	    'right':1
	})
	mse_bottom_format = workbook.add_format({
	    'align': 'center',  # 水平对齐方式
	    'valign': 'vcenter',  # 垂直对齐方式
	    'left':1,
	    'right':1,
	    'bottom':1,
	})
	cell_format = workbook.add_format({
	    'align': 'center',  # 水平对齐方式
	    'valign': 'vcenter',  # 垂直对齐方式
	    'num_format': '0%',
	    'top':1,
	    'bottom':1,
	    'left':1,
	    'right':1
	})
	mse_red_format = workbook.add_format({
		'color':'red',
	    'align': 'center',  # 水平对齐方式
	    'valign': 'vcenter',  # 垂直对齐方式
	    'left':1,
	    'right':1
	})
	mse_red_bottom_format = workbook.add_format({
		'color':'red',
	    'align': 'center',  # 水平对齐方式
	    'valign': 'vcenter',  # 垂直对齐方式
	    'left':1,
	    'right':1,
	    'bottom':1,
	})
	merge_format = workbook.add_format({
	    'align': 'center',  # 水平对齐方式
	    'valign': 'vcenter',  # 垂直对齐方式
	    'top':1,
	    'bottom':1,
	    'left':1,
	    'right':1
	})
	# 循环合并每个工作簿
	while nowSheet < sheetSum:
		print("合并第"+str(nowSheet+1)+"个工作簿...")
		# 此循环内工作簿不变
		# 保存同一工作簿下所有数据集的内容
		dataContent = []
		dataSetNum = 0

		while dataSetNum < dataSetSum:
			# 保存同一数据集中所有文件的内容
			filesContent = []
			# 记录一个数据集中有多少个文件
			filesSum = 0
			for arg in args:
				# 此循环内文件不变
				fileName 	= arg[0]
				dataSet 	= arg[1]
				PreModel 	= arg[2]
				costModel 	= arg[3]
				# 每次只处理外层循环对应的数据集

				if( int(dataSet) != dataSetNum + 1 ):
					continue
				filesSum = filesSum + 1
				#读取当前工作簿
				readbook = xlrd.open_workbook(fileName)
				sheet = readbook.sheet_by_index(nowSheet)
				# 在我的基础分析的格式中，每页工作簿有2行是标题，剩下的行数才是内容
				nrows = sheet.nrows - 2
				raw = 0
				# 保存一个文件内(某一工作簿的)所有数据信息
				fileContent = []
				title = sheet.row_values(0, start_colx=0, end_colx=1)[0]
				while raw < nrows:
					#逐行读取
					res = (title,)+ tuple( sheet.row_values(raw + 2, start_colx=1, end_colx=5) )
					#print(res)
					fileContent.append(res)
					raw = raw + 1
				filesContent.append(fileContent)
			dataContent.append(filesContent)
			dataSetNum = dataSetNum + 1
		# 数据读取完毕,开始处理内容
		sheetName = sheetNames[nowSheet]
		worksheet = workbook.add_worksheet(sheetName)
		worksheet.set_column(1,1,16)
		# 锚定光标
		global_j 	= 0 # 锚定全局
		data_j 		= 0 # 锚定数据集
		titleChar = 67
		mergeStr = 'A'+str(global_j + 1)+':'+'A'+str(global_j + 2)
		worksheet.merge_range(mergeStr, 'DataSet', merge_format)
		mergeStr = 'B'+str(global_j + 1)+':'+'B'+str(global_j + 2)
		worksheet.merge_range(mergeStr, bookNames[nowSheet], merge_format)
		#数据集循环
		dataSetNum = 0
		while dataSetNum < dataSetSum:
			files = dataContent[dataSetNum]
			#文件循环
			col = 0
			
			while col < len(files):
				file = files[col]
				# 写入小标题
				if(dataSetNum == 0):
					mergeStr = chr(titleChar + col * 3 )+str(global_j + 1)+':'+chr(titleChar + 2 + col * 3)+str(global_j + 1)
					mergeStr = str(mergeStr)
					#print(mergeStr)
					worksheet.merge_range(mergeStr, file[0][0], merge_format)
				worksheet.write(global_j+1, 2 + col*3, predictionInterval[0], cell_format)
				worksheet.write(global_j+1, 3 + col*3, predictionInterval[1], cell_format)
				worksheet.write(global_j+1, 4 + col*3, predictionInterval[2], cell_format)
				raw = 0
				while raw < len(file):
					if(raw + 1 < len(file)):
						worksheet.write(data_j + 2 + raw, 1	, file[raw][1], mse_format)
						worksheet.write(data_j + 2 + raw, 2 + col*3, file[raw][2], mse_format)
						worksheet.write(data_j + 2 + raw, 3 + col*3, file[raw][3], mse_format)
						worksheet.write(data_j + 2 + raw, 4 + col*3, file[raw][4], mse_format)
					else:
						worksheet.write(data_j + 2 + raw, 1	, file[raw][1], mse_bottom_format)
						worksheet.write(data_j + 2 + raw, 2 + col*3, file[raw][2], mse_bottom_format)
						worksheet.write(data_j + 2 + raw, 3 + col*3, file[raw][3], mse_bottom_format)
						worksheet.write(data_j + 2 + raw, 4 + col*3, file[raw][4], mse_bottom_format)
					raw = raw + 1
				col = col + 1

			content = 'DS'+str(dataSetNum+1)
			if(data_j+3 != data_j+raw+2):
				# 合并数据集名称单元格
				mergeStr = 'A'+str(data_j+3)+':'+'A'+str(data_j+raw+2)
				worksheet.merge_range(mergeStr, content, merge_format)
			else:
				worksheet.write(data_j+2,0,content,mse_bottom_format)
				
			data_j = data_j + raw
			dataSetNum = dataSetNum + 1
		nowSheet = nowSheet + 1
	print("开始生成文件...")
	workbook.close()
	print("完成!")

# 基础分析。
# 将最原始的数据结果文件分析逐个分析
# 一份原始数据文件 分析出 一个基础分析文件
# 输入是原始数据文件列表，可以用同样的基础分析方法一次性分析出很多原始数据文件
def analysis_base(args):
	for arg in args:
		fileName 	= arg[0]
		dataSet 	= arg[1]
		PreModel 	= arg[2]
		costModel 	= arg[3]
		readbook = xlrd.open_workbook(fileName)
		taskResultTuples = ()
		#预测点所在的excel表格页
		predictionPointPages = [1,3,5]
		for Page in predictionPointPages:
			sheet = readbook.sheet_by_index(Page) # 1 3 5
			nrows = sheet.nrows#行
			raw = 1
			while raw < nrows:
				res = tuple( sheet.row_values(raw, start_colx=0, end_colx=10) )
				taskResultTuples = taskResultTuples + (res,)
				raw = raw + 1
		# 设定数据集名称
		dataName = "DS"+dataSet
		modelName = PreModel+costModel
		# 创建excel文件
		desktop_path = sys.path[0]+"\\excel_save\\"
		# 不附加末尾随机数字
		excel_fileName = "重构_"+dataName+modelName+".xlsx" 
		# 附加末尾随机数字
		#excel_fileName = "重构_"+dataName+modelName+'_'+str(int(time.time()))+str(random.randint(0,9999))+ ".xlsx" 
		desktop_path = desktop_path + excel_fileName;
		workbook = xlsxwriter.Workbook(desktop_path)
		'''
		worksheet = workbook.add_worksheet("AllPara")
		j = 0 # 控制外循环中记录到了第j行
		'''
		bookNames = ('weightMethods','costMethods','costDataMethods','thresholdMethods','thresholdRules','dataTransforms','vares')
		paraLists = []
		i = 0 # 控制内循环中计算第i项参数的最小mse值
		for bookName in bookNames:
			paraList_o = []
			paraList_d = []
			# 跳过第七项，因为第七项是predictionInterval
			if(i == 6):
				i = 7
			# 跳过第二项。因为此处恒要求比较第二项
			if(i == 1):
				i = i + 1
				continue
			# 重组数据
			for paraTuple in taskResultTuples:
				mse2 = paraTuple[1]
				# 读取参数
				weightMethod = paraTuple[0+2]
				costMethod = paraTuple[1+2]
				costDataMethod = paraTuple[2+2]
				thresholdMethod = paraTuple[3+2]
				thresholdRule = paraTuple[4+2]
				dataTransform = paraTuple[5+2]
				predictionInterval = paraTuple[6+2]
				var = paraTuple[7+2]
				# 排除非法参数组合
				if(dataTransform == 'TranslationInvariant' and thresholdMethod == 'ut') or (dataTransform != 'TranslationInvariant' and thresholdMethod == 'ldt'):
					continue
				# 只计算无权重的结果
				#if(weightMethod != 'none'):
				#	continue
				# 只计算有权重的结果
				#if(weightMethod == 'none'):
				#	continue	
				#只保留gauus 和 boxcar
				if(weightMethod != 'boxcar' and weightMethod != 'Gaussian'):
					continue
				# 只计算quota
				if(costDataMethod == 'grow'):
					continue
				# denoise 只对 N+1 生效
				#if(costMethod == 'denoise' and ifCompareNewData == 0):
				#	continue
				# compare 只对 none 生效
				#if(weightMethod != 'none' and compare != 0):
				#	continue
				# 不计算 TranslationInvariant
				#if(dataTransform == 'TranslationInvariant'):
				#	continue
				# 只计算 Anscome
				#if(dataTransform != 'Anscombe'):
				#	continue
				# 只考虑0.25的情况
				if(var == 1):
					continue
				# 只考虑soft的情况
				if(thresholdRule == 'h'):
					continue
				para = paraTuple[i+2]
				# s 与 h 显示上不好看。更改为 soft 与 hard
				if(i == 4):
					if(paraTuple[i+2] == 's'):
						para = 'soft'
					if(paraTuple[i+2] == 'h'):
						para = 'hard'
				if(costMethod == 'origin'):
					dictPara = dict()
					dictPara["para"] = para
					dictPara["predictionPoint"] = predictionInterval
					dictPara["mse"] = mse2
					paraList_o.append(dictPara)
				if(costMethod == 'denoise'):
					dictPara = dict()
					dictPara["para"] = para
					dictPara["predictionPoint"] = predictionInterval
					dictPara["mse"] = mse2
					paraList_d.append(dictPara)

			# 记录 origin 下的最佳记录
			sheetName = bookName+"_origin_"+PreModel+costModel
			titleName = "origin_"+PreModel+costModel
			worksheet = workbook.add_worksheet(sheetName)
			#j = sort_and_write(titleName,dataName,j,paraList_o,workbook,worksheet)
			sort_and_write(titleName,dataName,0,paraList_o,workbook,worksheet)

			# 记录 denoise 下的最佳记录
			sheetName = bookName+"_denoise_"+PreModel
			titleName = "denoise_"+PreModel
			worksheet = workbook.add_worksheet(sheetName)
			#j = sort_and_write(titleName,dataName,j,paraList_d,workbook,worksheet)
			sort_and_write(titleName,dataName,0,paraList_d,workbook,worksheet)

			i = i + 1
		workbook.close();
		print("运行结果")
		print("读取文件:"+fileName)
		print("输出文件:"+desktop_path)

# 将排序和写入工作簿的部分单独提出来
# j 是写入光标的锚点，paraList是待写入的列表
def sort_and_write(titleName,dataName,j,paraList,workbook,worksheet):
	mse_format = workbook.add_format({
	    'align': 'center',  # 水平对齐方式
	    'valign': 'vcenter',  # 垂直对齐方式
	    'left':1,
	    'right':1
	})
	mse_bottom_format = workbook.add_format({
	    'align': 'center',  # 水平对齐方式
	    'valign': 'vcenter',  # 垂直对齐方式
	    'left':1,
	    'right':1,
	    'bottom':1,
	})
	cell_format = workbook.add_format({
	    'align': 'center',  # 水平对齐方式
	    'valign': 'vcenter',  # 垂直对齐方式
	    'num_format': '0%',
	    'top':1,
	    'bottom':1,
	    'left':1,
	    'right':1
	})
	mse_red_format = workbook.add_format({
		'color':'red',
	    'align': 'center',  # 水平对齐方式
	    'valign': 'vcenter',  # 垂直对齐方式
	    'left':1,
	    'right':1
	})
	mse_red_bottom_format = workbook.add_format({
		'color':'red',
	    'align': 'center',  # 水平对齐方式
	    'valign': 'vcenter',  # 垂直对齐方式
	    'left':1,
	    'right':1,
	    'bottom':1,
	})
	merge_format = workbook.add_format({
	    'align': 'center',  # 水平对齐方式
	    'valign': 'vcenter',  # 垂直对齐方式
	    'top':1,
	    'bottom':1,
	    'left':1,
	    'right':1
	})
	worksheet.set_column(1,1,22)
	# 记录参数名
	mergeStr = 'A'+str(j+1)+':'+'E'+str(j+1)
	worksheet.merge_range(mergeStr, titleName, merge_format)
	mergeStr = 'A'+str(j+2)+':'+'B'+str(j+2)
	worksheet.merge_range(mergeStr, '', merge_format)
	# 对数据进行排序
	#print(str(taskResultTuples[0][i+2])+" 开始排序")
	l = sorted(paraList, key=lambda x:(x['predictionPoint'], x['para'], x['mse']))
	# 记录某预测点下最小的MSE 与 全部MSE(上色模块)
	minMse = 999999999
	MseList = []
	if(minMse > l[0]["mse"]):
		minMse = l[0]["mse"]
	MseList.append(l[0]["mse"])

	col = 0
	raw = 1
	nowPredictionPoint = l[0]["predictionPoint"]
	nowPara = l[0]["para"]
	worksheet.write(j+1,2+col,nowPredictionPoint,cell_format)
	worksheet.write(j+1+raw,2+col,l[0]["mse"],mse_format)
	worksheet.write(j+1+raw,1,l[0]["para"],mse_format)
	worksheet.write(j+1+raw,0,dataName,mse_format)

	for x in l:
		if(x["predictionPoint"] != nowPredictionPoint):
			# 重新写入上一条信息，并加入下边框样式
			worksheet.write(j+1+raw,2+col,MseList[len(MseList)-1],mse_bottom_format)
			worksheet.write(j+1+raw,1,nowPara,mse_bottom_format)
			# 结算、上色单元格、初始化、更新(上色模块)
			# 若所有mse都一样，则不上色
			judge = False
			for the_mse in MseList:
				if(minMse != the_mse):
					judge = True
					break
			#if(dataName == 'DS1') and (nowPara == 'grow' or nowPara == 'quota'):
			#	print(judge)
			if(judge):
				now_raw = 0
				for the_mse in MseList:
					if(the_mse == minMse):

						#if(dataName == 'DS1') and (nowPara == 'grow' or nowPara == 'quota'):
						#	print(MseList)
						#	print(now_raw)
						#若是最后一行，则需要加下边框样式
						if(len(MseList) == now_raw + 1):
							worksheet.write(j+2+now_raw,2+col,the_mse,mse_red_bottom_format)
						else:
							worksheet.write(j+2+now_raw,2+col,the_mse,mse_red_format)
					now_raw = now_raw + 1
			minMse = 999999999
			MseList = []
			if(minMse > x["mse"]):
				minMse = x["mse"]
			MseList.append(x["mse"])
			
			nowPara = x["para"]
			nowPredictionPoint = x["predictionPoint"]
			# 预测点更换
			col = col + 1
			raw = 1
			worksheet.write(j+1,2+col,nowPredictionPoint,cell_format)
			worksheet.write(j+1+raw,2+col,x["mse"],mse_format)
		elif(x["para"] != nowPara):
			nowPara = x["para"]
			raw = raw + 1
			# 更新最小Mse值 与 MSE列表(上色模块)
			if(minMse > x["mse"]):
				minMse = x["mse"]
			MseList.append(x["mse"])

			#print(str(j+1+raw)+","+str(2+col)+":"+str(x["mse"]))
			worksheet.write(j+1+raw,2+col,x["mse"],mse_format)
			worksheet.write(j+1+raw,1,x["para"],mse_format)
	# 重新写入上一条信息，并加入下边框样式
	worksheet.write(j+1+raw,2+col,MseList[len(MseList)-1],mse_bottom_format)
	worksheet.write(j+1+raw,1,nowPara,mse_bottom_format)
	# 结算、上色单元格、初始化(上色模块)
	# 若所有mse都一样，则不上色
	judge = False
	for the_mse in MseList:
		if(minMse != the_mse):
			judge = True
			break
	if(judge):
		now_raw = 0
		for the_mse in MseList:
			if(the_mse == minMse):
				#若是最后一行，则需要加下边框样式
				if(len(MseList) == now_raw + 1):
					worksheet.write(j+2+now_raw,2+col,the_mse,mse_red_bottom_format)
				else:
					worksheet.write(j+2+now_raw,2+col,the_mse,mse_red_format)
			now_raw = now_raw + 1
	# 数据集名称只有一格时无法合并
	if(j+3 != j+raw+2):
		# 合并数据集名称单元格
		mergeStr = 'A'+str(j+3)+':'+'A'+str(j+raw+2)
		#box(workbook,worksheet,j+2,1,j+raw+1,1)
		worksheet.merge_range(mergeStr, dataName, merge_format)
	else:
		worksheet.write(j+2,0,dataName,mse_bottom_format)
	# 数据录入完成，向下移动光标
	j = j + raw + 3
	return j
import analysisResult

# python c:\\xampp\\htdocs\\readResult.py
choose = 0

if(choose == 1) or (choose == 0):
	# 基础分析
	# 将最原始的数据结果文件分析逐个分析
	# 一份原始数据文件 分析出 一个基础分析文件
	# 输入是原始数据文件列表，可以用同样的基础分析方法一次性分析出很多原始数据文件
	dataSets = ['1','2','3','4','5','6','7']
	PreModels = ['q1','~q1']
	costModels = ['N+1','N']
	args = []
	for dataSet in dataSets:
		for PreModel in PreModels:
			for costModel in costModels:
				fileName = 'C:\\Users\\hello\\Documents\\report\\DS'+dataSet+PreModel+costModel+'.xlsx'
				arg = [fileName,dataSet,PreModel,costModel]
				args.append(arg)

	analysisResult.analysis_base(args)

if(choose == 2) or (choose == 0):
	# 合并文件
	# 将多个经过基础分析的文件合并为一个文件
	dataSets = ['1','2','3','4','5','6','7']
	PreModels = ['q1','~q1']
	costModels = ['N+1','N']
	# 每份文件都有12页工作簿
	sheetSum = 12
	# 数据集数
	dataSetSum = len(dataSets)
	args = []
	for dataSet in dataSets:
		for PreModel in PreModels:
			for costModel in costModels:
				fileName = 'C:\\xampp\\htdocs\\excel_save\\重构_DS'+dataSet+PreModel+costModel+'.xlsx'
				arg = [fileName,dataSet,PreModel,costModel]
				args.append(arg)

	analysisResult.analysis_merge(args,sheetSum,dataSetSum)


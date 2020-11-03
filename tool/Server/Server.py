from master import Master
from multiprocessing import freeze_support
import os

#春雪分布式计算系统v1.0

#简介:
#本分布式计算系统以WEB为交互接口,可运行特定结构的python代码.
#利用分布式集群的强大算力快速完成计算,随后将计算结果保存在一个excel表格中.

#安装说明

#本系统安装简单,由一个服务端与若干个工作端组成.
#服务端以WEB为交互接口,控制此分布式计算系统的开启、提交任务、查询任务进度、下载计算结果等.只需部署Server文件夹中的WEB项目,访问其首页即可.
#工作端只需要修改Work文件夹中的配置文件config.txt,随后运行work.py即可
#
#注意事项:
#	应先部署Server中的WEB项目,并启动分布式计算系统后,再在工作端运行work.py

#使用说明

#用户必须提供:
#		1.特定结构的python任务代码 (以下简称为 任务代码 )
#		2.数据文件
#		3.参数文件
#
#用户可选提供:
#		1.任务代码的 依赖包

#任务代码详细构造:
#	用户需在任务代码中按照以下定义实现4个方法,分别是:
#		1.读取数据文件方法
#		Tuple readDataFunction(dataFile = string)
#		2.读取参数文件方法
#		Tuple readParaFunction(ParaFile = string)
#		3.任务方法
#		Tuple taskFunction(dataTuple = Tuple,paraTuple = Tuple)
#		4.结果保存方法
#		Tuple saveFunction(taskResultTuple = Tuple)
#
#	同时,用户还需在任务代码中定义两个元组 workbookNames 与 workbookRawNames
#	有关这两个元组的详细说明见后文	

#对于一次计算任务,系统运行流程如下:
#	第一步:
#		用户上传 任务代码、数据文件、参数文件 (可选上传 任务代码的依赖包)
#
#	第二步:
#		系统运行任务代码,系统首先执行其中的 readDataFunction 方法 与 readParaFunction 方法.
#		readDataFunction 方法将返回一个 二维元组dataTuples, 并看做一个 Nx1 的矩阵,
#		readParaFunction 方法也将返回一个 二维元组paraTuples, 并看做一个 1xN 的矩阵,
#		系统将 矩阵dataTuples 与 矩阵paraTuples 相乘,得到 每一组数据与每一组参数的组合 形成的 矩阵Data-ParaTuples,
#		该矩阵中的任一元素均为 (dataTuple,paraTuple)
#
#	第三步:
#		生成保存本次计算任务结果用的空excel表格.
#		该excel表格将含有 len(workbookNames) 个工作簿,其中第i个工作簿的簿名为workbookNames[i-1]
#		对于excel表格中的每一个工作簿,都会在第一行表格中写入一行 列名,其中第i个工作簿的第j列的列名为 workbookRawNames[i-1][j-1]
#
#	第四步:
#		将第二步中生成的 矩阵Data-ParaTuples 中的每一个元素 (dataTuple,paraTuple) 都作为参数,传递给 taskFunction 方法执行.
#		taskFunction 方法将利用 (dataTuple,paraTuple) 进行计算,返回一个 一维元组taskResultTuple
#
#	第五步:
#		saveFunction 方法将接受 taskFunction 方法的返回值 ———— 元组taskResultTuple, 并返回一个 二维元组resultCommandTuples.
#		二维元组resultCommandTuples 保存着多个 一维元组resultCommandTuple.
# 		一维元组resultCommandTuple 的作用是指示系统向第三步中生成的excel表格中写入一行数据.
#		一维元组resultCommandTuple 由以下结构组成:
#			(workbookNum = int, right = Bool, resultTuple = Tuple)
#		其内每个元素的详细见后文 方法说明
#		
#	第六步:
#		当矩阵Data-ParaTuples 中的每一个元素都被 taskFunction 方法执行完毕后,系统将返回第三步时创建excel表格作为计算结果给用户

#方法说明
#	readDataFunction 方法
#		参数 dataFile 是 数据文件 的存放路径.(例如 C:\\data.txt)
#		返回值是一个二维Tuple,Tuple[0]表示数据文件中第一行数据,Tuple[0][0]表示数据文件中第一行第一列的数据
#
#	readParaFunction 方法
#		参数 ParaFile 是 参数文件 的存放路径.(例如 C:\\para.txt)
#		返回值是一个二维Tuple,Tuple[0]表示参数文件中第一行参数,Tuple[0][0]表示参数文件中第一行的第一个参数
#
#	taskFunction 方法
#		参数 dataTuple 为 readDataFunction 方法返回值二维Tuple中的某一行
#		参数 paraTuple 为 readParaFunction 方法返回值二维Tuple中的某一行
#		返回值是一个一维Tuple,为本次任务在利用 dataTuple 与 paraTuple 的情况下得到的计算结果
#
#	saveFunction 方法
#		参数 taskResultTuple 为taskFunction 方法返回的一维元组.
#		返回值是一个二维Tuple,该二维Tuple中每一个 一维Tuple都将指示系统向保存计算结果的excel表格中写入一行数据
#		该一维Tuple由以下结构组成:
#			(workbookNum = int, right = Bool, resultTuple = Tuple)
#		其含义是,向 第 workbookNum + 1 个工作簿, 写入 一行或一列 数据resultTuple.
#		其中,当 right 为 True 时,写入一行数据; 当 right 为 False 时,写入一列数据.

# python c:\\xampp\\htdocs\\Server\\Server.py
if __name__ == "__main__":
	freeze_support()

	#配置调度服务器(master)信息
	#服务器的IP地址
	#本地环境
	server = '10.30.87.77';
	#服务器环境
	server = '127.0.0.1';
	server = '172.17.25.109';
	#master与slave内部通信端口,需slave与之一致
	port = 9002;
	#master对外通信端口
	socket_port = 8500
	#设定连接秘钥,需slave与之一致
	authkeys = 'jobs'
	# 设定ftp服务器信息
	ftp_server = server
	ftp_user = 'ftpuser'
	ftp_pass = 'wJc@19961221'
	#创建服务器
	master = Master(server,port,authkeys,socket_port,ftp_server,ftp_user,ftp_pass)
	#启动Master服务器 timeout单位为分钟
	master.start(120)

	print("Server close")
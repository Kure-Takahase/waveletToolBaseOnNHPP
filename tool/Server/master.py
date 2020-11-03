import queue
from multiprocessing import Process, Queue, Manager, Lock
from multiprocessing.managers import BaseManager
#from job import Job
from multiprocessing import freeze_support
import xlsxwriter
import random
import time
import sys,os,importlib,signal,stat
import socket,json
from ftplib import FTP
import getpass
import importlib.util

#调试用
#import multi_DTWSE
#python c:\\xampp\\htdocs\\master.py

# 第一步：定义三个Queue队列，一个用于发送任务，一个接收结果, 一个发送生成excel表格请求
momentum_task_queue     = queue.Queue() # 待发布任务队列
task_queue              = queue.Queue() # 已发布任务队列(将待发布任务队列的任务计时后，发布)
result_queue            = queue.Queue() # 已发布任务队列的计算结果
resultFile_queue        = queue.Queue() # 已发布任务队列的计算结果转换为excel表格生成指令的队列，内含生成excel表格的请求
#excel_file_name_dict    = list()        # 任务保存时使用的工作簿名与列名


# 定义三个函数，返回结果就是Queue队列
def return_momentum_task_queue():
    global momentum_task_queue # 定义成全局变量
    return momentum_task_queue # 返回待发布任务队列
def return_task_queue():
    global task_queue # 定义成全局变量
    return task_queue # 返回发送任务的队列
def return_result_queue():
    global result_queue
    return result_queue # 返回接收结果的队列
def return_resultFile_queue():
    global resultFile_queue
    return resultFile_queue # 返回发送生成excel表格请求的队列
'''
def return_excel_file_name_dict():
    global excel_file_name_dict
    return excel_file_name_dict # 返回任务保存时工作簿名与列名字典
'''

# ftp下载
def download(IP, username, password, remote_path, local_path):
    #print(getpass.getuser())
    #print_out(outputList,output_lock,"ftp:下载 "+remote_path)
    ftp = FTP()
    ftp.connect(IP, 21)      # 第一个参数可以是ftp服务器的ip或者域名，第二个参数为ftp服务器的连接端口，默认为21
    ftp.login(username, password)     # 匿名登录直接使用ftp.login()
    #ftp.cwd("tmp")                # 切换到tmp目录
    fp = open(local_path, "wb")
    buf_size = 1024
    ftp.retrbinary('RETR {}'.format(remote_path), fp.write, buf_size)
    fp.close()
    ftp.quit()

# ftp上传
def upload(IP, username, password, remote_path, local_path):
    #print_out(outputList,output_lock,"ftp:上传 "+local_path)
    ftp = FTP()
    ftp.connect(IP, 21)      # 第一个参数可以是ftp服务器的ip或者域名，第二个参数为ftp服务器的连接端口，默认为21
    ftp.login(username, password)     # 匿名登录直接使用ftp.login()
    bufsize = 1024
    fp = open(local_path, 'rb')
    ftp.storbinary('STOR ' + remote_path, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()
    ftp.quit()

def print_out(outputList,output_lock,message):
    # 只保存150条消息
    max_count = 150

    output_lock.acquire()
    if(len(outputList) >= max_count):
        del outputList[0]
    if(len(outputList)-1 < 0):
        num = 1
    else:
        num = outputList[len(outputList)-1][0]
    t = (num + 1,message)
    outputList.append(t)
    output_lock.release()
    print(message)

def get_output(outputList,output_lock):
    output_lock.acquire()
    t = tuple(outputList)
    output_lock.release()
    return t


# Master通信进程: 输入: socket通信 输出 待发布队列,socket通信
# 收到Task创建请求后，需将Task的关联文件发放给所有Slave,待Slave全部更新关联文件后,将Task放入待发布队列
def masterSocket(server_ip,task_port,authkeys,socket_port,ftp_server,ftp_user,ftp_password,excel_filename_dict,outputList,output_lock,excel_save_List,excel_save_List_lock,pid):
    while True:
        try:
            # 注册 待发布队列 与 Task队列
            BaseManager.register('get_momentum_task_queue')

            print_out(outputList,output_lock,'Master通信进程: 开始连接服务器 %s...' % server_ip)
            # 监听端口和启动服务
            manager = BaseManager(address=(server_ip,task_port), authkey=authkeys)
            manager.connect()
            
            # 使用上面注册的方法获取队列
            momentum_queue = manager.get_momentum_task_queue()

            # 获取待更新excel_save文件
            ftp = FTP()
            ftp.connect(ftp_server, 21)      # 第一个参数可以是ftp服务器的ip或者域名，第二个参数为ftp服务器的连接端口，默认为21
            ftp.login(ftp_user, ftp_password)     # 匿名登录直接使用ftp.login()
            ftp.cwd('excel_save')
            arr = ftp.nlst()                        #获取目录下的文件
            ftp.quit()
            excel_save_List_lock.acquire()
            for x in arr:
                excel_save_List.append(x)
            excel_save_List_lock.release()

            #是否向sys.path内增加过路径
            ifAddPath = False

            # 建立一个服务端
            server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((server_ip,socket_port)) # 绑定要监听的端口
            server.listen(5) # 开始监听 表示可以使用五个链接排队
            while True:# conn就是客户端链接过来而在服务端为期生成的一个链接实例
                #print_out(outputList,output_lock,'Master通信进程: 开始监听外部连接...')
                print("socket通信: 开始监听外部连接")
                conn,addr = server.accept() # 等待链接,多个链接的时候就会出现问题,其实返回了两个值
                #print_out(outputList,output_lock,'Master通信进程: 收到一个连接请求'+str(addr))
                try:
                    # 接收数据
                    data = conn.recv(1024).decode()
                    # 转换数据
                    #print(data)
                    data = json.loads(data)
                except Exception as e:
                    print('socket通信: 收到异常消息，放弃处理此次消息')
                    print(data)
                    # 关闭连接
                    conn.shutdown(2)
                    conn.close()
                    continue
                #print_out(outputList,output_lock,'Master通信进程: recive '+data['type']) #打印接收到的数据
                # 若Web发来Task创建请求
                if(data['type'] == 'createTask'):
                    # 关闭连接
                    conn.shutdown(2)
                    conn.close()
                    print_out(outputList,output_lock,'Master通信进程: 收到任务'+data['taskName']+'的创建请求')
                    # 创建临时文件夹
                    if not os.path.exists(sys.path[0]+"/"+data['dateNum']):
                        oldmask = os.umask (0o22)
                        print_out(outputList,output_lock,'Master通信进程: 创建日期编号文件夹')
                        os.mkdir(sys.path[0]+"/"+data['dateNum'],0o777)
                        os.umask (oldmask)
                    else :
                        print_out(outputList,output_lock,'Master通信进程: 日期编号文件夹已存在')
                    if not os.path.exists(sys.path[0]+"/"+data['dateNum']+"/"+data['uniqueNum']):
                        oldmask = os.umask (0o22)
                        print_out(outputList,output_lock,'Master通信进程: 创建专属编号文件夹')
                        os.mkdir(sys.path[0]+"/"+data['dateNum']+"/"+data['uniqueNum'],0o777)
                        os.umask (oldmask)
                    else :
                        print_out(outputList,output_lock,'Master通信进程: 专属编号文件夹已存在')

                    #print(getpass.getuser())
                    # 下载文件
                    print_out(outputList,output_lock,'Master通信进程: 生成基础路径')
                    remote_path = data['dateNum']+"/"+data['uniqueNum']+"/"
                    local_path = sys.path[0]+"/"+data['dateNum']+"/"+data['uniqueNum']+"/"
                    # 数据文件
                    print_out(outputList,output_lock,'Master通信进程: 开始下载数据文件')
                    download(ftp_server,ftp_user,ftp_password,remote_path+data['dataFile'],local_path+data['dataFile'])
                    # 参数文件
                    print_out(outputList,output_lock,'Master通信进程: 开始下载参数文件')
                    download(ftp_server,ftp_user,ftp_password,remote_path+data['paraFile'],local_path+data['paraFile'])
                    # 任务代码
                    print_out(outputList,output_lock,'Master通信进程: 开始下载任务代码')
                    download(ftp_server,ftp_user,ftp_password,remote_path+data['taskCodeFile'],local_path+data['taskCodeFile'])
                    # 依赖项
                    if(data['otherCodeFiles'] != ''):
                        otherCodeFiles = json.loads(data['otherCodeFiles'])
                        if(len(otherCodeFiles) != 0):
                            print_out(outputList,output_lock,'Master通信进程: 开始下载依赖项')
                            otherFiles = ();
                            for otherCodeFile in otherCodeFiles:
                                download(ftp_server,ftp_user,ftp_password,remote_path+otherCodeFile,local_path+otherCodeFile)
                                otherFiles = otherFiles + (local_path+otherCodeFile,)
                        else:
                            print_out(outputList,output_lock,'Master通信进程: 无依赖项')
                    # 创建Task
                    base_url = local_path
                    if (ifAddPath):
                        del sys.path[-1]
                    try:
                        task_tuples = createTask(base_url,data['dateNum'],data['uniqueNum'],data['taskCodeFile'],otherFiles,data['dataFile'],data['paraFile'],data['taskName'],excel_filename_dict,outputList,output_lock)
                        ifAddPath = True
                        #print_out(outputList,output_lock,task_tuples[0])
                        # 发布Task
                        for task in task_tuples:
                            print_out(outputList,output_lock,'Master通信进程: 开始发布Task'+str(task[1]))
                            momentum_queue.put(task)
                    except Exception as e:
                        print_out(outputList,output_lock,'Master通信进程: 创建Task 出错!')
                        print_out(outputList,output_lock,'Master通信进程: '+str(e))

                elif (data['type'] == 'ping'):
                    print_out(outputList,output_lock,'Master通信进程: 收到一个心跳包')
                    #返回心跳
                    conn.send(b'pong')
                    # 关闭连接
                    conn.shutdown(2)
                    conn.close()

                elif (data['type'] == 'getOutput'):
                    #print_out(outputList,output_lock,'Master通信进程: 收到一个获取外部输出列表请求')
                    outputT = get_output(outputList,output_lock)
                    #print(data['last_num'])

                    last_num = int(data['last_num'])
                    new_T = ()
                    if(len(outputT) == 0) or (outputT[len(outputT)-1][0] <= last_num):
                        pass
                    else:
                        for x in outputT:
                            if(x[0] > last_num):
                                new_T = new_T + (x,)
                    outputS = json.dumps(new_T)
                    conn.sendall(outputS.encode())
                    # 关闭连接
                    conn.shutdown(2)
                    conn.close()

                elif (data['type'] == 'getExcelSaveFiles'):
                    excel_save_file_tuples = ()
                    excel_save_List_lock.acquire()
                    i = len(excel_save_List) - 1
                    while i >= 0:
                        excel_save_file_tuples = excel_save_file_tuples + (excel_save_List[i],)
                        #从列表中去除
                        del excel_save_List[i]
                        i = i - 1;
                    excel_save_List_lock.release()
                    excel_save_file_str = json.dumps(excel_save_file_tuples)
                    conn.sendall(excel_save_file_str.encode())
                    # 关闭连接
                    conn.shutdown(2)
                    conn.close()

                elif (data['type'] == 'stop'):
                    conn.shutdown(2)
                    conn.close()
                    print_out(outputList,output_lock,"执行特殊的方法")
                    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect( (server_ip,socket_port))
                    print_out(outputList,output_lock,"执行server.shutdown()")
                    server.shutdown(2)
                    print_out(outputList,output_lock,"执行server.close()")
                    server.close()
                    os.kill(pid, signal.SIGTERM)
                    pass
                # 调试用
                elif (data['type'] == 'addExcelSaveFiles'):
                    # 关闭连接
                    conn.sendall(b'ok')
                    conn.shutdown(2)
                    conn.close()

                    # 获取待更新excel_save文件
                    ftp = FTP()
                    ftp.connect(ftp_server, 21)      # 第一个参数可以是ftp服务器的ip或者域名，第二个参数为ftp服务器的连接端口，默认为21
                    ftp.login(ftp_user, ftp_password)     # 匿名登录直接使用ftp.login()
                    ftp.cwd('excel_save')
                    arr = ftp.nlst()                        #获取目录下的文件
                    ftp.quit()
                    excel_save_List_lock.acquire()
                    for x in arr:
                        excel_save_List.append(x)
                    excel_save_List_lock.release()

                else :
                    # 关闭连接
                    conn.shutdown(2)
                    conn.close()
                    print_out(outputList,output_lock,'Master通信进程: 收到了未定义的请求')
        except Exception as e:
            print(e)
        print("socket崩溃，重新启动外部通信进程")

# 生成Task,返回所有生成的Task元组
def createTask(base_url,dateNum,uniqueNum,taskCodeFile,otherCodeFile,dataFileName,paraFileName,taskName,excel_filename_dict,outputList,output_lock):

    # 获取任务代码名称(去掉.py)
    taskFileName = taskCodeFile[0:len(taskCodeFile)-3]

    #taskFileName 自动导入代码,生成、并发布Task
    #导入本次任务代码
    if not os.path.exists(base_url+taskCodeFile):
        print_out(outputList,output_lock,"Master通信进程: 任务文件 "+taskCodeFile+" 不存在!")
        return ();
    #修改sys.path
    sys.path.append(base_url)

    # 若已加载过同名模块，则先清除同名模块
    taskModule = importlib.import_module(taskFileName)
    for modulesName in taskModule.libFiles + (taskFileName,):
        if(modulesName in sys.modules.keys()):
            print_out(outputList,output_lock,"Master通信进程: 已加载过同名模块"+modulesName+"，先清除同名模块")
            del sys.modules[modulesName]

    taskModule          = importlib.import_module(taskFileName)
    # 设置读取数据的方法(由用户提供,用于读取fileName.输入为fileName,返回值为二维Tuple)
    readDataFunction    = taskModule.readDataFunction
    # 设置读取参数的方法(由用户提供,用于读取paraFileName,并返回所有待计算的参数组合.输入为paraFileName,返回值为二维Tuple)
    readParaFunction    = taskModule.readParaFunction
    # 设置处理数据的方法(由用户提供,最小的任务计算单元.)
    # 输入为两个参数.第一个参数为readDataFunction的返回值的其中一个元素,第二个参数为readParaFunction的返回值的其中一个元素)
    taskFunction        = taskModule.taskFunction

    # 设置结果保存excel表的所有工作簿的名称元组
    workbookNames       = taskModule.workbookNames
    # 设置工作簿内的列名元组
    # 将每个工作簿内的列名元组汇总为一个元组
    workbookRawNames    = taskModule.workbookRawNames

    # 设置保存处理结果的方法(由用户提供,输入为一个Tuple,数据处理结果的元组)
    # 返回值为一个二维Tuple,其中每个Tuple内规定格式为(workbookNum = int, right = Bool, ResultData = Tuple)
    # ResultData表示待写入excel表中的结果元组,workbookNum表示写入第几个工作簿(0表示第一个),
    # right为True表示将ResultData写入一行(横向写入),为False时表示写入一列(纵向写入)
    saveFunction        = taskModule.saveFunction

    # 设置Task所需依赖包
    libFiles = taskModule.libFiles + (taskFileName,)
    print_out(outputList,output_lock,'Master通信进程: Task所需依赖包 '+str(libFiles))
    libFiles = (dateNum,uniqueNum,libFiles)


    # 在进程中，应监听以上信息,监听到后，执行以下代码
    # 获取数据和待计算参数
    dataTuples = readDataFunction(base_url+dataFileName)
    paraTuples = readParaFunction(base_url+paraFileName)
    print(paraTuples)
    print(base_url+paraFileName)

    #保存此任务的excel工作簿名 与 列名
    nameTuple = (workbookNames,workbookRawNames)
    excel_filename_dict[ taskName ] = nameTuple

    taskSum = len(dataTuples) * len(paraTuples)
    # 放入待发布队列,等待任务发布进程发布
    taskNum = 0
    result  = ()
    for dataTuple in dataTuples:
        for paraTuple in paraTuples:
            task = (taskFileName,taskNum,taskSum,dataTuple,paraTuple,libFiles,taskName,1)
            result = result + (task,)
            taskNum = taskNum + 1
            if(taskNum == 97):
                print(paraTuple)
    print_out(outputList,output_lock,"Master通信进程: 已生成"+str(taskNum)+"个Task")
    return result

# Task发布进程: 输入: 待发布队列, 输出: Task队列 与 计时List
def distributionTask(server,port,authkeys,ReDistributeLict,lock,outputList,output_lock):

    # 注册 待发布队列 与 Task队列
    BaseManager.register('get_momentum_task_queue')
    BaseManager.register('get_dispatched_job_queue')

    print_out(outputList,output_lock,'Task发布进程: 开始连接服务器 %s...' % server)
    # 监听端口和启动服务
    manager = BaseManager(address=(server,port), authkey=authkeys)
    manager.connect()

    # 使用上面注册的方法获取队列
    momentum_queue = manager.get_momentum_task_queue()
    dispatched_jobs = manager.get_dispatched_job_queue()

    # 持续处理
    while True:
        # 获取一个待发布任务
        job = momentum_queue.get();
        #print_out(outputList,output_lock,"发布进程: 成功获取Task_"+str(job.getTaskNum()))

        #等待Task队列为空(所有已发布Task都被取走)
        while not dispatched_jobs.empty():
            time.sleep(1)
            pass

        #记录当前时间,并放入Task队列与计时List,等待被计算.
        #job.setStartTime(int(time.time()))
        job = job + (int(time.time()),)
        #进程锁
        lock.acquire()
        ReDistributeLict.append(job)
        lock.release()
        dispatched_jobs.put(job)
        #print_out(outputList,output_lock,"发布进程: 成功发布Task_"+str(job.getTaskNum()))
        print_out(outputList,output_lock,"发布进程: 成功发布Task_"+str(job[1]))

        #print_out(outputList,output_lock,"发布进程: 超时队列当前Task数量:"+str(len(ReDistributeLict)))

# Task重发进程: 输入: 计时List, 输出: 待发布队列 或 结果队列 timeout单位为分钟
def reDistributionTask(server,port,authkeys,ReDistributeLict,timeout,lock,outputList,output_lock):
    # 注册 待发布队列 与 结果队列
    BaseManager.register('get_momentum_task_queue')
    #BaseManager.register('get_dispatched_job_queue')
    BaseManager.register('get_finished_job_queue')

    print_out(outputList,output_lock,'Task重发进程: 开始连接服务器 %s...' % server)
    # 监听端口和启动服务
    manager = BaseManager(address=(server,port), authkey=authkeys)
    manager.connect()

    # 使用上面注册的方法获取队列
    momentum_queue = manager.get_momentum_task_queue()
    #dispatched_jobs = manager.get_dispatched_job_queue()
    finished_jobs = manager.get_finished_job_queue()

    print_out(outputList,output_lock,"重发进程: 开始循环查询计时List")
    # 持续处理
    while True:
        time.sleep(1)
        #进程锁
        lock.acquire()
        if(len(ReDistributeLict) <= 0):
            lock.release()
            continue
        job = ReDistributeLict[0]
        #获取job信息
        taskFileName = job[0]
        taskNum = job[1]
        taskSum = job[2]
        dataTuples = job[3]
        paraTuples = job[4]
        job_files = job[5]
        taskName = job[6]
        CalculateTime = job[7]
        start_time = job[8]

        now_time = int(time.time());
        left_time = now_time - start_time
        m, s = divmod(int(left_time), 60)
        if(m > timeout): #30分钟还未完成该Task的计算
            #从列表中去除
            del ReDistributeLict[0]
            # 若多次超时，则取消任务.若首次超时，则重新发布
            if( CalculateTime > 1):
                resultCommandTuples = (job,(),())
                finished_jobs.put( resultCommandTuples )
                print_out(outputList,output_lock,"Task重发进程: Task_"+str(taskNum)+" 超时多次,取消任务，返回空结果")
            else:
                job = job[0:7] + (2,)
                # 重新加入待发布队列,最后处理
                momentum_queue.put( job )
                print_out(outputList,output_lock,"Task重发进程: Task_"+str(taskNum)+" 超时一次,重新将Task_"+str(job[1])+"放入待发布队列")
        lock.release()

# 结果处理进程: 输入: 结果队列, 输出: excel表格生成队列 与 计时List
def dealResult(server,port,authkeys,ReDistributeLict,lock,outputList,output_lock):
    # 注册 结果队列 与 excel表格生成队列
    BaseManager.register('get_finished_job_queue')
    BaseManager.register('get_excel_file_queue')

    print_out(outputList,output_lock,'结果处理进程: 开始连接服务器 %s...' % server)
    # 监听端口和启动服务
    manager = BaseManager(address=(server,port), authkey=authkeys)
    manager.connect()

    # 使用上面注册的方法获取队列
    finished_jobs = manager.get_finished_job_queue()
    excel_files = manager.get_excel_file_queue()

    # 汇总Task结果(所有SaveFunction的输出),用于创建excel表格
    allResult = dict();
    # 汇总已完成的Task编号
    allTaskNum = dict();
    # 汇总所有TaskFunction的输出
    allresTuple = dict()

    # 持续处理
    while True:
        try:
            # 抓取一组Task结果
            resultCommandTuples = finished_jobs.get()
            resultCommandTuples = tuple(resultCommandTuples)

            # 查询此Task实例,并移除计时List
            job         = resultCommandTuples[ 0 ]
            #获取job信息
            taskFileName = job[0]
            taskNum = job[1]
            taskSum = job[2]
            dataTuples = job[3]
            paraTuples = job[4]
            job_files = job[5]
            dateNum = job_files[0]
            uniqueNum = job_files[1]
            job_files = job_files[2]
            taskName = job[6]
            CalculateTime = job[7]
            start_time = job[8]

            #print(dateNum)
            #print(uniqueNum)


            index = 0
            #进程锁
            lock.acquire()
            for li_job in ReDistributeLict:
                if(li_job[5][1] == uniqueNum) and (li_job[1] == taskNum):
                    del ReDistributeLict[index]
                    #print_out(outputList,output_lock,"结果处理进程: 已移除计时List中"+taskName+" Task_"+str(taskNum)+"计时List中剩余Task数为:"+str(len(ReDistributeLict)))
                    break
                index = index + 1
            #进程锁
            lock.release()

            # 进程内部处理
            # 查询此Task所属的任务名称(唯一)
            uniqueNum    = uniqueNum
            # 查询此结果的Task编号
            TaskNum     = taskNum
            # 查询此Task所属任务的任务总数
            TaskSum     = taskSum
            # 获取taskFunction的原始结果输出
            resTuple = resultCommandTuples[2]
            # 将输入还原成原本的结果(传输前在原结果前追加了 Task实例 )
            resultCommandTuples = resultCommandTuples[1]
            

            # 若此组结果为所属任务的第一个到来的结果,则追加属于该任务的结果储存元组
            # (所有SaveFunction的输出)
            if uniqueNum not in allResult:
                allResult[uniqueNum] = ()
            # 任务完成进度元组
            if uniqueNum not in allTaskNum:
                allTaskNum[uniqueNum] = [0 for x in range(0, TaskSum)]
            # 原始结果元组(所有TaskFunction的输出)
            if uniqueNum not in allresTuple:
                allresTuple[uniqueNum] = ()

            #与其他进程交流
            s = sum(allTaskNum[uniqueNum])
            print_out(outputList,output_lock,"结果处理进程: 已获得任务"+taskName+"中Task_"+str(taskNum)+"的结果("+str(s+1)+"/"+str(taskSum)+") "+"当前计时List中Task数为:"+str(len(ReDistributeLict)))

            # 若所有任务都已经完成
            if(sum(allTaskNum[uniqueNum]) == TaskSum):
                print_out(outputList,output_lock,"结果处理进程: 任务"+uniqueNum+" 已结束。不再处理此结果")
                continue;
            # 若此Task结果已被处理过
            if(allTaskNum[uniqueNum][TaskNum] == 1):
                print_out(outputList,output_lock,"结果处理进程: "+uniqueNum+" Task_"+str(taskNum)+"已被处理过。不再处理此结果")
                continue;

            # 储存此次结果
            for resultCommandTuple in resultCommandTuples:
                allResult[uniqueNum] = allResult[uniqueNum] + (resultCommandTuple,)
            # 储存resTuple
            if(resTuple != ()):
                allresTuple[uniqueNum] = allresTuple[uniqueNum] + (resTuple,)
            #print_out(outputList,output_lock,"结果处理进程: 调试打印excel生成指令")
            #for x in allResult[uniqueNum]:
            #    print_out(outputList,output_lock,x)
            # 设置 编号TaskNum 的Task已完成
            allTaskNum[uniqueNum][TaskNum] = 1;

            # 若所有任务都已经完成
            if(sum(allTaskNum[uniqueNum]) == TaskSum):
                jobInfo = (dateNum,uniqueNum,job_files[len(job_files)-1])
                # 提交给excel表格生成进程处理
                excel_files.put((taskName,tuple(allResult[uniqueNum]),tuple(allresTuple[uniqueNum]),jobInfo))
        except Exception as e:
            print("结果处理进程: 出现无法预料的错误。放弃处理此Task。5秒后重新开始工作...")
            print(e)
            print("Task内容:")
            print(resultCommandTuples)
            time.sleep(5)
        else:
            pass

        

# excel表格生成进程: 输入: excel表格生成队列 与 工作簿名与列名字典, 输出: excel表格
def excel_save(server,port,authkeys,excel_filename_dict,ftp_server,ftp_user,ftp_password,outputList,output_lock,excel_save_List,excel_save_List_lock):
    # 注册 excel表格生成队列 与 工作簿名与列名字典
    BaseManager.register('get_excel_file_queue')

    print_out(outputList,output_lock,'excel_save 进程: 开始连接服务器 %s...' % server)
    # 监听端口和启动服务
    manager = BaseManager(address=(server,port), authkey=authkeys)
    manager.connect()

    # 使用上面注册的方法获取队列
    excel_files = manager.get_excel_file_queue()

    # fileList 储存已下载的依赖包
    fileList = []

    #检查本地目录是否存在
    if not os.path.exists(sys.path[0]+"/excel_save"):
        os.mkdir(sys.path[0]+"/excel_save")
    #检查远程目录是否存在
    ftp = FTP()
    ftp.connect(ftp_server, 21)      # 第一个参数可以是ftp服务器的ip或者域名，第二个参数为ftp服务器的连接端口，默认为21
    ftp.login(ftp_user, ftp_password)     # 匿名登录直接使用ftp.login()
    arr = ftp.nlst()                        #获取目录下的文件
    if not ('excel_save' in arr):
        print ("excel_save 进程: 远程目录不存在,创建远程目录")
        ftp.mkd('excel_save')                 #新建远程目录
    else:
        print ("excel_save 进程: 远程目录已存在")
    ftp.quit()

    # 持续处理
    while True:
        # 获得一个excel表格生成请求
        excelFileCommandTuples = excel_files.get()
        print_out(outputList,output_lock,"excel表格生成进程: 已获得excel表格生成请求")
        # 获取此excel表格名称
        excelFileName = excelFileCommandTuples[ 0 ];
        print_out(outputList,output_lock,"excel表格生成进程: 任务"+str(excelFileName)+" 已完成，正在生成excel报告")
        # 获取resTuples
        resTuples = excelFileCommandTuples[2]
        # 获取任务代码实例
        job = excelFileCommandTuples[3]
        # 获取生成excel表格指令
        excelFileCommandTuples = excelFileCommandTuples[1]

        # 获取工作簿名称元组 与 列名元组
        workbookNames = excel_filename_dict[excelFileName][0]
        workbookRawNames = excel_filename_dict[excelFileName][1]

        # 创建excel文件
        desktop_path = sys.path[0]+"/excel_save/"
        fileName = excelFileName +'_'+str(int(time.time()))+str(random.randint(0,9999))+ ".xlsx"
        desktop_path = desktop_path + fileName;
        workbook = xlsxwriter.Workbook(desktop_path)

        # 根据指令写入数据
        bookNum = 0;
        for workbookName in workbookNames:
            worksheet = workbook.add_worksheet(workbookName)
            workbookRawName = workbookRawNames[ bookNum ]
            excel_WriteRaw(workbookRawName,0,0,worksheet)
            raw = 1
            col = 0
            for excelFileCommandTuple in excelFileCommandTuples:
                if(excelFileCommandTuple[0] == bookNum):
                    right       = excelFileCommandTuple[1]
                    resultTuple = excelFileCommandTuple[2]
                    if(right == True):
                        excel_WriteRaw(resultTuple,raw,0,worksheet)
                        raw = raw + 1
                    else:
                        excel_WriteCol(resultTuple,0,col,worksheet)
                        col = col + 1
            bookNum = bookNum + 1

        # 保存excel文件到ftp服务器,并将路径返回给WEB
        workbook.close();
        upload(ftp_server,ftp_user,ftp_password,"excel_save/"+fileName,desktop_path)
        # 加入到反馈WEB更新列表
        excel_save_List_lock.acquire()
        excel_save_List.append(fileName)
        excel_save_List_lock.release()
        print_out(outputList,output_lock,"excel表格生成进程: 成功保存结果！"+fileName);

        # 运行用户自定义的结果处理程序
        dateNum         = job[0]
        uniqueNum       = job[1]
        taskFileName    = job[2]
        
        # 清除之前加入的路径,避免干扰
        listLen = len(fileList)
        i = 0
        while i < listLen:
            print_out(outputList,output_lock,"excel表格生成进程: 清除之前加入的路径")
            del sys.path[-1]
            i = i + 1
        fileList = []
        # 若已加载过同名模块，则先清除同名模块
        if(taskFileName in sys.modules.keys()):
            print_out(outputList,output_lock,"excel表格生成进程: 已加载过同名模块，先清除同名模块")
            del sys.modules[taskFileName]
        # 加入新路径
        if uniqueNum not in fileList:
            print_out(outputList,output_lock,"excel表格生成进程: 当前目录 "+sys.path[len(sys.path) -1])
            #修改sys.path
            sys.path.append(sys.path[0]+"/"+str(dateNum)+"/"+str(uniqueNum))
            fileList.append(uniqueNum)
            print_out(outputList,output_lock,"excel表格生成进程: 新追加的目录 "+sys.path[len(sys.path) -1])

        # 获取任务文件的实例
        taskModule = importlib.import_module(taskFileName)
        #print(sys.modules[taskFileName])
        try:
            taskModule.finialCust(excelFileName,resTuples)
        except Exception as e:
            print_out(outputList,output_lock,"excel表格生成进程: 用户自定义结果处理程序出错!")
            print(e)
        else:
            print_out(outputList,output_lock,"excel表格生成进程: 用户自定义结果处理程序已完成")

#将datas内的数据写入一列。从(raw,col)开始往下写入.(0,0)为第一行第一列
def excel_WriteCol(datas,raw,col,worksheet):
    i = 0;
    for data in datas:
        worksheet.write(raw + i,col,data);
        i = i + 1;

#将datas内的数据写入一行。从(raw,col)开始往右写入.(0,0)为第一行第一列
def excel_WriteRaw(datas,raw,col,worksheet):
    i = 0;
    for data in datas:
        worksheet.write(raw,col + i,data);
        i = i + 1;

def term(sig_num, addtion):
    print('term current pid is %s, group id is %s' % (os.getpid(), os.getpgrp()))
    os.killpg(os.getpgid(os.getpid()), signal.SIGKILL)

class Master:

    def __init__(self,server,task_port,authkeys,socket_port,ftp_server,ftp_user,ftp_password):
        self.server         = server;
        self.port           = task_port;
        self.authkeys       = authkeys.encode('utf-8');
        self.socket_port    = socket_port;
        self.ftp_server     = ftp_server;
        self.ftp_user       = ftp_user;
        self.ftp_password   = ftp_password;
        # Create queues
        #self.task_queue = Queue()
        #self.done_queue = Queue()

    def start(self,timeout):
        # 任务重发监听列表
        ReDistributeLict =  Manager().list();
        # 任务保存时工作簿名与列名字典
        excel_filename_dict = Manager().dict();
        # 外部输出列表
        outputList =  Manager().list();
        # 工作簿名与列名字典锁
        lock = Lock()
        # 外部输出列表锁
        output_lock = Lock()
        # 外部excel文件更新列表
        excel_save_List =  Manager().list();
        # 外部excel文件更新列表锁
        excel_save_List_lock = Lock()

        print_out(outputList,output_lock,"主线程: 注册系统信号量")
        signal.signal(signal.SIGTERM, term)

        print_out(outputList,output_lock,"主线程: 注册队列到网络")
        # 把派发作业队列和完成作业队列以及请求生成excel表格队列注册到网络上
        BaseManager.register('get_momentum_task_queue', callable=return_momentum_task_queue)
        BaseManager.register('get_dispatched_job_queue', callable=return_task_queue)
        BaseManager.register('get_finished_job_queue', callable=return_result_queue)
        BaseManager.register('get_excel_file_queue', callable=return_resultFile_queue)
        # 任务保存时工作簿名与列名字典
        #BaseManager.register('get_excel_file_name_dict',callable=return_excel_file_name_dict)

        print_out(outputList,output_lock,"主线程: 启动网络队列服务")
        # 监听端口和启动服务
        self.manager = BaseManager(address=(self.server,self.port), authkey=self.authkeys)
        self.manager.start()
        momentum_task_queue = self.manager.get_momentum_task_queue()

        ProcessList = []
        print_out(outputList,output_lock,"主线程: 创建服务进程")
        # 创建master通信进程,监听socket端口,等待Web发来Task请求
        p0 = Process(target=masterSocket, args=(self.server,self.port,self.authkeys,self.socket_port,self.ftp_server,self.ftp_user,self.ftp_password,excel_filename_dict,outputList,output_lock,excel_save_List,excel_save_List_lock,os.getpid()))
        p0.start()
        ProcessList.append(p0)

        # 创建Task发布进程
        p1 = Process(target=distributionTask, args=(self.server,self.port,self.authkeys,ReDistributeLict,lock,outputList,output_lock))
        p1.start()
        ProcessList.append(p1)
        
        # 创建Task重发进程
        p2 = Process(target=reDistributionTask, args=(self.server,self.port,self.authkeys,ReDistributeLict,timeout,lock,outputList,output_lock))
        p2.start()
        ProcessList.append(p2)
        # 创建结果处理进程
        p3 = Process(target=dealResult, args=(self.server,self.port,self.authkeys,ReDistributeLict,lock,outputList,output_lock))
        p3.start()
        ProcessList.append(p3)
        # 创建excel表格生成进程
        p4 = Process(target=excel_save, args=(self.server,self.port,self.authkeys,excel_filename_dict,self.ftp_server,self.ftp_user,self.ftp_password,outputList,output_lock,excel_save_List,excel_save_List_lock))
        p4.start()
        ProcessList.append(p4)
        
        #time.sleep(3)
        #print_out(outputList,output_lock,"主线程: 模拟发布任务")
        #self.addTask(excel_filename_dict,momentum_task_queue)

        print_out(outputList,output_lock,"主线程: 阻塞主进程")
        for p in ProcessList:
            p.join()
        print_out(outputList,output_lock,"主线程: 所有子线程运行结束，退出。")

    def close(self):
        self.manager.shutdown()
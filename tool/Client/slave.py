import time,sys,os,importlib
import queue
from multiprocessing.managers import BaseManager
from job import Job
from multiprocessing import freeze_support,Process,cpu_count,Queue
from ftplib import FTP

# ftp下载
def download(IP, username, password, remote_path, local_path):
    ftp = FTP()
    ftp.connect(IP, 21)      # 第一个参数可以是ftp服务器的ip或者域名，第二个参数为ftp服务器的连接端口，默认为21
    ftp.login(username, password)     # 匿名登录直接使用ftp.login()
    ftp.set_pasv(0)
    fp = open(local_path, "wb")
    buf_size = 1024
    ftp.cwd('')
    ftp.retrbinary('RETR {}'.format(remote_path), fp.write, buf_size)
    fp.close()
    ftp.quit()

def createJob(taskName,taskNum,taskSum,dataTuple,paraTuple,start_time):
    print("work进程: 载入 任务代码...")
    taskModule = importlib.import_module(taskName)
    # 设置处理数据的方法(由用户提供,最小的任务计算单元.)
    # 输入为两个参数.第一个参数为readDataFunction的返回值的其中一个元素,第二个参数为readParaFunction的返回值的其中一个元素)
    taskFunction        = taskModule.taskFunction

    # 设置保存处理结果的方法(由用户提供,输入为一个Tuple,数据处理结果的元组)
    # 返回值为一个二维Tuple,其中每个Tuple内规定格式为(workbookNum = int, right = Bool, ResultData = Tuple)
    # ResultData表示待写入excel表中的结果元组,workbookNum表示写入第几个工作簿(0表示第一个),
    # right为True表示将ResultData写入一行(横向写入),为False时表示写入一列(纵向写入)
    saveFunction        = taskModule.saveFunction

    # 设置Task所需依赖包
    libFiles = taskModule.libFiles

    job = Job(taskName,taskNum,taskSum,dataTuple,paraTuple,taskFunction,saveFunction,libFiles)
    job.setCalculateTime(1)
    job.setStartTime(start_time)
    return job

# python c:\\xampp\\htdocs\\slave.py
class Slave:

    def __init__(self,server,port,authkeys,ftp_server,ftp_username, ftp_password):
        self.server = server;
        self.port = port;
        self.authkeys = authkeys.encode('utf-8');
        self.ftp_server = ftp_server
        self.ftp_username = ftp_username
        self.ftp_password = ftp_password

    def start(self,idle_core):
        print("创建 待处理Task队列 和 TaskResult队列")
        # 创建 待处理Task队列 和 TaskResult队列
        moTask_queue = Queue()
        resTask_queue = Queue()

        # 创建N-1个工作进程,N为CPU核心数
        ProcessList = []
        core_count = int(cpu_count());
        print("获取CPU核心数:"+str(core_count))
        if(core_count - idle_core <= 0):
            print('start fail! idle_core must be less than work_core!')
            return 'start fail! idle_core must be less than work_core!'
        i = 0
        while i < core_count - idle_core: # idle_core决定空闲几个核
            print("启动工作进程_"+ str(i+1))
            p = Process(target=self.work, args=(moTask_queue,resTask_queue))
            p.start()
            ProcessList.append(p)
            i = i + 1
        print("启动Task分配进程")
        # 创建Task分配进程
        p1 = Process(target=self.taskDistribution, args=(self.server,self.port,self.authkeys,moTask_queue,self.ftp_server,self.ftp_username, self.ftp_password))
        p1.start()
        ProcessList.append(p1)
        print("启动TaskResult进程")
        # 创建TaskResult进程,处理工作进程返回的结果,并返回给Master服务器
        p2 = Process(target=self.taskResult, args=(self.server,self.port,self.authkeys,resTask_queue))
        p2.start()
        ProcessList.append(p2)

        print("开始阻塞主进程")
        for p in ProcessList:
            p.join()


    def taskDistribution(self,server,port,authkeys,moTask_queue,ftp_server,ftp_username,ftp_password):
        # 把 Task队列 注册到网络上
        BaseManager.register('get_dispatched_job_queue')

        # 连接master
        print('taskDistribution Connect to server %s...' % server)
        self.manager = BaseManager(address=(server, port), authkey=authkeys)
        self.manager.connect()

        # 使用上面注册的方法获取队列
        dispatched_jobs = self.manager.get_dispatched_job_queue()

        # fileList 储存已下载的依赖包
        fileList = []

        # 持续处理
        while True:
            time.sleep(0.05)
            # 监听 待处理Task队列,若存在空闲,则尝试分配一个Task
            while not moTask_queue.empty():
                pass

            # 获取并分配Task
            job = dispatched_jobs.get()
            job_name = job[0]
            taskNum = job[1]
            taskSum = job[2]
            dataTuples = job[3]
            paraTuples = job[4]
            job_files = job[5]
            dateNum = job_files[0]
            uniqueNum = job_files[1]
            job_files = job_files[2:len(job_files)]
            taskName = job[6]
            CalculateTime = job[7]
            start_time = job[8]
            print("taskDistribution进程: 工作进程已空闲,从Master获取一个Task")
            if uniqueNum not in fileList:
                print("taskDistribution进程: 未发现该Task所需依赖包")
                if not os.path.exists(sys.path[0]+"\\"+dateNum):
                    os.mkdir(sys.path[0]+"\\"+dateNum)
                if not os.path.exists(sys.path[0]+"\\"+dateNum+"\\"+uniqueNum):
                    os.mkdir(sys.path[0]+"\\"+dateNum+"\\"+uniqueNum)

                for job_file in job_files:
                    remote_path = dateNum+'/'+uniqueNum+'/'+job_file+".py"
                    local_path  = sys.path[0]+"\\"+dateNum+'\\'+uniqueNum+'\\'+job_file+".py"
                    print(remote_path)
                    print(local_path)
                    print("taskDistribution进程: 开始下载Task所需依赖包 "+job_file+".py")
                    #print("远程路径 "+remote_path)
                    #print("本地路径 "+local_path)
                    download(ftp_server, ftp_username, ftp_password, remote_path, local_path)
                print("taskDistribution进程: Task所需依赖包全部下载完成")
                #修改sys.path
                #sys.path.append(sys.path[0]+"\\"+job_name)
                fileList.append(uniqueNum)
            #开始创建job
            #print("taskDistribution进程: 开始创建job")
            #job = createJob(job_name,taskNum,taskSum,dataTuples,paraTuples,start_time)

            # 加入 待处理Task队列
            moTask_queue.put(job)
            print("taskDistribution进程: job创建成功,等待job被work进程取走")

    def work(self,moTask_queue,resTask_queue):
        # fileList 储存已下载的依赖包
        fileList = []
        while True:
            # 获取一个Task
            job         = moTask_queue.get()
            res_job     = job
            job_name = job[0]
            taskNum = job[1]
            taskSum = job[2]
            dataTuples = job[3]
            paraTuples = job[4]
            job_files = job[5]
            dateNum = job_files[0]
            uniqueNum = job_files[1]
            job_files = job_files[2:len(job_files)]
            taskName = job[6]
            CalculateTime = job[7]
            start_time = job[8]
            if uniqueNum not in fileList:
                print("work进程: 当前目录 "+sys.path[len(sys.path) -1])
                #修改sys.path
                sys.path.append(sys.path[0]+"\\"+dateNum+"\\"+uniqueNum)
                fileList.append(uniqueNum)
                print("work进程: 新追加的目录 "+sys.path[len(sys.path) -1])
            #print("work进程: 获取了一个Task_"+str(job.getTaskNum()))
            print("work进程: 获取了一个Task_"+str(taskNum))
            print("work进程: 开始创建job")
            job = createJob(job_name,taskNum,taskSum,dataTuples,paraTuples,start_time)
            # 获取 当前Task的参数与数据
            DataTuple   = job.getDataTuple()
            ParaTuple   = job.getParaTuple()
            # 计算此Task
            print("work进程 开始计算job")
            resTuple    = job.taskFunction(DataTuple,ParaTuple)
            taskRes     = job.saveFunction(resTuple)

            # 提交结果给TaskResult队列
            taskRes = (res_job,) + taskRes
            resTask_queue.put(taskRes)
            print("work 完成了一个Task_"+str(taskNum))

    def taskResult(self,server,port,authkeys,resTask_queue):
        # 把 结果队列 注册到网络上
        BaseManager.register('get_finished_job_queue')

        # 连接master
        print('taskResult Connect to server %s...' % server)
        self.manager = BaseManager(address=(server, port), authkey=authkeys)
        self.manager.connect()

        # 使用上面注册的方法获取队列
        dispatched_jobs = self.manager.get_finished_job_queue()

        # fileList 储存已下载的依赖包
        fileList = []

        # 持续处理
        while True:
            resTaskResult = resTask_queue.get()
            dispatched_jobs.put(resTaskResult)
            print("taskResult 进程 返回了一个结果")
from slave import Slave
from multiprocessing import freeze_support
# python c:\\xampp\\htdocs\\Client\\Client.py

if __name__ == "__main__":
    freeze_support()
    # master服务器的IP地址
    server = '47.100.98.37';
    # master服务器的端口
    port = 9002;
    # 设定连接秘钥
    authkeys = 'jobs'
    # 设定ftp服务器信息
    ftp_user = 'ftpuser'
    ftp_pass = 'wJc@19961221'
	# 创建Slave
    slave = Slave(server,port,authkeys,server,ftp_user,ftp_pass)
    # 启动Slave(连接master服务器后，开始循环 获取任务包→计算→返回结果)
    slave.start(1) # 空闲核数
    
    print("Slave close")
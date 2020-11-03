from ftplib import FTP


def upload(f, remote_path, local_path):
    fp = open(local_path, "rb")
    buf_size = 1024
    f.storbinary("STOR {}".format(remote_path), fp, buf_size)
    fp.close()


def download(f, remote_path, local_path):
    fp = open(local_path, "wb")
    buf_size = 1024
    f.retrbinary('RETR {}'.format(remote_path), fp.write, buf_size)
    fp.close()

#python c:\\xampp\\htdocs\\ftptest.py
if __name__ == "__main__":
	username = 'ftpuser'
	password = 'q12345'
	ftp = FTP()
	ftp.connect("10.30.87.77", 21)      # 第一个参数可以是ftp服务器的ip或者域名，第二个参数为ftp服务器的连接端口，默认为21
	ftp.login(username, password)     # 匿名登录直接使用ftp.login()
	#ftp.cwd("tmp")                # 切换到tmp目录
	#upload(ftp, "ftp_a.txt", "a.txt")   # 将当前目录下的a.txt文件上传到ftp服务器的tmp目录，命名为ftp_a.txt
	download(ftp, "c:\\xampp\\htdocs\\local_test\\local_test.py", "c:\\xampp\\htdocs\\abc\\local_test\\local_test.py")  # 将ftp服务器tmp目录下的ftp_a.txt文件下载到当前目录，命名为b.txt
	ftp.quit()
	print("ok")
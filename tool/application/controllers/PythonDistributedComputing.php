<?php
defined('BASEPATH') OR exit('No direct script access allowed');
require ('Calendar.php');

//加载GatewayClient。关于GatewayClient参见本页面底部介绍
require_once 'GatewayClient/Gateway.php';
// GatewayClient 3.0.0版本开始要使用命名空间
use GatewayClient\Gateway;

class PythonDistributedComputing extends CI_Controller {

	public function __construct()    //父类构造函数
	{
		parent::__construct();
	    $this->load->helper('path');
	    $this->load->helper('url');
	    #$this->load->model('IP_model');//IP相关模块
	    #$this->load->model('Monitor_model');//行为监控模块
	    Gateway::$registerAddress = $this->config->item('gateway_registerAddress');

	    //ftp服务器基本信息
	    $this->ftp_IP = '172.17.25.109';
		$this->ftp_username = 'ftpuser';
		$this->ftp_password = 'wJc@19961221';

/*
		$this->ftp_IP = '10.30.87.77';
		$this->ftp_username = 'ftpuser';
		$this->ftp_password = 'q12345';
*/
		//master服务器基本信息
		$this->master_ip = $this->ftp_IP;
		$this->master_port = 8500;
	}

	//调试用
	public function addExcelSaveFiles()
	{
		//获取master服务器信息
		$master_ip 		= $this->master_ip;
		$master_port 	= $this->master_port;
		$type 			= 'addExcelSaveFiles';
		//请求excel_save更新文件列表
		$answer = $this->askTypeQuestion($master_ip,$master_port,$type);
		echo $answer;
	}

	public function startServer()
	{
		$status = $this->input->post('status');
		$result['action'] = $status;
		//启动Master服务器
		if($status == '1')
		{
			$result['result'] = dirname(__FILE__);
			$commod = 'nohup python -u /var/www/html/tool/Server/Server.py &';
			//$commod = 'ls /var/www/html/';
			//$result['result'] = exec('nohup python -u ../../Server/Server.py > test.out 2>&1 &');
			$a = exec($commod,$out,$astatus);  
			$result['a'] = $a;
			$result['out'] = $out;  
			$result['status'] = $astatus;

		}
		//停止Master服务器
		if($status == '0')
		{
			//获取master服务器信息
			$master_ip 		= $this->master_ip;
			$master_port 	= $this->master_port;
			$type 			= 'stop';
			//询问心跳
			$answer = $this->askTypeQuestion($master_ip,$master_port,$type);
			$result['answer'] = $answer;
		}
		$arr = json_encode($result);
		echo $arr;
	}

	public function getExcelSaveFilesList()
	{
		$dir = '/var/www/html/waveletToolBaseOnNHPP/tool/Server/excel_save';
		#更新本地excel_save文件
		$this->updateExcelSaveFilesList();
		#获取本地excel_save文件列表
		$arr = scandir($dir);
		array_shift($arr);
		array_shift($arr);
		$json = json_encode($arr);
		echo $json;
	}

	public function updateExcelSaveFilesList()
	{
		//获取master服务器信息
		$master_ip 		= $this->master_ip;
		$master_port 	= $this->master_port;
		$type 			= 'getExcelSaveFiles';
		//请求excel_save更新文件列表
		$answer = $this->askTypeQuestion($master_ip,$master_port,$type);
		$arr = json_decode($answer);
		$len = count($arr);
		if($len != 0 )
		{
			for ($i = 0; $i < $len; $i++) 
			{
				$local_file 	= 'excel_save/'.$arr[ $i ];
				$remote_file 	= '/excel_save/'.$arr[ $i ];
				$this->ftp_download($local_file,$remote_file);
			}
		}
	}
	public function isMasterLive()
	{
		//获取master服务器信息
		$master_ip 		= $this->master_ip;
		$master_port 	= $this->master_port;
		$type 			= 'ping';
		//询问心跳
		$answer = $this->askTypeQuestion($master_ip,$master_port,$type);
		echo $answer;
	}
	public function getOutput()
	{
		//获取master服务器信息
		$master_ip 		= $this->master_ip;
		$master_port 	= $this->master_port;
		$type 			= 'getOutput';
		//请求master的外部输出
		$result['type'] = $type;
		$result['last_num'] = $this->input->post('last_num');
		$json = json_encode($result);
		$answer = $this->askQuestion($master_ip,$master_port,$json);
		
		echo $answer;
	}
	public function getTaskList()
	{	
		$arres = array();

		$arr['id'] = '1';
		$arr['status'] = '1';
		$arr['complete'] = '1';
		$arr['time'] = '1';
		$arr['active'] = '<button type="button" class="layui-btn layui-btn-xs layui-btn-radius">下载</button>';

		$arres[] = $arr;
		$arres[] = $arr;

		$result['code'] = 0;
		$result['msg'] 	= "";
		$result['count'] 	= 2;
		$result['data'] = $arres;
		$json = json_encode($result);
		echo $json;
	}
	public function addTask()
	{
		
		//获取Task信息
		$taskName 		= $this->input->post('taskName');
		$taskCodeFile 	= $this->input->post('taskCodeFile');
		$dataFile 		= $this->input->post('dataFile');
		$paraFile 		= $this->input->post('paraFile');
		$otherCodeFiles = $this->input->post('otherCodeFile');
		$dateNum 		= $this->input->post('date');
		$uniqueNum 		= $this->input->post('uniqueNum');
	
		$result['type'] 			= 'createTask';
		$result['taskName'] 		= $taskName;
		$result['taskCodeFile']		= $taskCodeFile;
		$result['dataFile'] 		= $dataFile;
		$result['paraFile'] 		= $paraFile;
		$result['otherCodeFiles'] 	= $otherCodeFiles;
		$result['uniqueNum'] 		= $uniqueNum;
		$result['dateNum'] 			= $dateNum;
		
		/*
		$result['type'] 			= 'createTask';
		$result['taskName'] 		= 'hihihi';
		$result['taskCodeFile']		= 'Client.py';
		$result['dataFile'] 		= 'DS4.txt';
		$result['paraFile'] 		= 'multi_para1.txt';
		$result['otherCodeFiles'] 	= '';
		$result['uniqueNum'] 		= '1597641446951';
		$result['dateNum'] 			= '2020_8';
		*/

		$json = json_encode($result);
		
		//获取master服务器信息
		$master_ip 		= $this->master_ip;
		$master_port 	= $this->master_port;

		//向master服务器发送信息
		$this->sendMessage($master_ip,$master_port,$json);

		echo $json;
	}
	public function fileUpload()
	{
		//获取文件信息
		$filename 	= $_FILES["file"]["name"];
		$fileURL 	= $_FILES["file"]["tmp_name"];
		$dateNum 	= $this->input->post('date');
		$uniqueNum 	= $this->input->post('uniqueNum');

		//保存文件
		$local_file		=	$fileURL;
		$remote_file	=	$dateNum.'/'.$uniqueNum.'/'.$filename;

		$messgae = $this->ftp_upload($local_file,$remote_file,$dateNum,$uniqueNum);

		$result['messgae'] = $messgae;
		$result['filename'] = $filename;
		$result['local_file'] = $fileURL;
		$result['remote_file'] = $remote_file;
		$result['uniqueNum'] = $uniqueNum;
		$json = json_encode($result);
		echo $json;
	}


	public function askTypeQuestion($ip,$port,$type)
	{
		//请求master的外部输出
		$result['type'] = $type;
		$json = json_encode($result);
		$answer = $this->askQuestion($ip,$port,$json);
		return $answer;
	}
	public function askQuestion($ip,$port,$json)
	{
		$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
		$result = socket_connect($socket, $ip, $port);
		$in = $json;
		# 询问
		socket_write($socket, $in, strlen($in));
		# 接受回答
		$out = socket_read($socket, 8192);
		# 若回答较长,则反复接受
		$total_out = $out;
		socket_set_nonblock($socket);
		while (strlen($out) != 0)
		{
			$out = socket_read($socket, 8192);
			$total_out = $total_out.$out;
		}
		socket_close($socket);
		return $total_out;
	}
	public function sendMessage($ip,$port,$message)
	{
		$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
		$result = socket_connect($socket, $ip, $port);
		$in = $message;
		socket_write($socket, $in, strlen($in));
		socket_close($socket);
	}
	public function ftp_download($local_file,$remote_file)
	{
		// 连接FTP服务器 
		$conn = ftp_connect($this->ftp_IP); 
		// 使用username和password登录 
		ftp_login($conn, $this->ftp_username, $this->ftp_password);
		//下载文件
		ftp_get($conn, $local_file, $remote_file, FTP_BINARY);
		//关闭连接
		ftp_quit($conn);
	}
	public function ftp_upload($local_file,$remote_file,$dateNum,$uniqueNum)
	{
		// 连接FTP服务器 
		$conn = ftp_connect($this->ftp_IP); 
		// 使用username和password登录 
		ftp_login($conn, $this->ftp_username, $this->ftp_password);
		//下载文件
		//ftp_get($conn, 'c:\\xampp\\abc.txt','master.py' , FTP_BINARY);

		//检查仓库目录
		$arr = ftp_nlist($conn,'.');
		if(in_array($dateNum,$arr) == false)
		{
			$message = '仓库目录未创建 ';
			@ftp_mkdir($conn,$dateNum);
		}
		else
			$message = '仓库目录已创建 ';

		//检查目录
		$arr = ftp_nlist($conn,'./'.$dateNum);
		if(in_array($uniqueNum,$arr) == false)
		{
			$message = $message.'任务目录未创建 ';
			@ftp_mkdir($conn,'./'.$dateNum.'/'.$uniqueNum);
		}
		else
			$message = $message.'任务目录已创建 ';
		//上传文件
		ftp_put($conn, $remote_file, $local_file, FTP_BINARY);
		//关闭连接
		ftp_quit($conn);
		return $message;
	}

}
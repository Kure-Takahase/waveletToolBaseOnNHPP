<?php
defined('BASEPATH') OR exit('No direct script access allowed');

//加载GatewayClient。关于GatewayClient参见本页面底部介绍
require_once 'GatewayClient/Gateway.php';
// GatewayClient 3.0.0版本开始要使用命名空间
use GatewayClient\Gateway;

class Register extends CI_Controller {

	/**
	 * Index Page for this controller.
	 *
	 * Maps to the following URL
	 * 		http://example.com/index.php/welcome
	 *	- or -
	 * 		http://example.com/index.php/welcome/index
	 *	- or -
	 * Since this controller is set as the default controller in
	 * config/routes.php, it's displayed at http://example.com/
	 *
	 * So any other public methods not prefixed with an underscore will
	 * map to /index.php/welcome/<method_name>
	 * @see https://codeigniter.com/user_guide/general/urls.html
	 */
	public function __construct()    //父类构造函数
	{
		parent::__construct();
	    $this->load->helper('path');
	    $this->load->helper('url');
	    $this->load->model('IP_model');//IP相关模块
	    $this->load->model('Common_model');//通用模块
	    $this->load->model('User_model');//用户信息模块
	    $this->load->model('Monitor_model');//行为监控模块
	    Gateway::$registerAddress = $this->config->item('gateway_registerAddress');
	}
	public function register()
	{
		$json['status'] = "200";//设置默认状态码200 表示成功
		$password = $this->input->post('password');//获取用户提交的密码
		$repass = $this->input->post('repass');//获取用户提交的重复密码
		$passwordLength = $this->input->post('passwordLength');//获取用户提交的密码
		$email = $this->input->post('email');//获取用户提交的email
		$userName = $this->input->post('nickname');//获取用户提交的nickName
		$sex = 0;							//获取用户提交的性别
		$IP = $this->IP_model->getIP();//获取用户IP地址
		$IParea = $this->IP_model->getIPArea($IP);//获取用户真实物理地址
		$time = $this->Common_model->getDate();//获取当前时间
		$this->Monitor_model->logRegisterAction($email, $userName, $password, $repass, $IP, $IParea, $time);//记录本次注册行为
		if($email == null || $userName == null || $password == null || $repass == null)
		{
			echo "大哥，请不要用奇怪的方式访问我！";
			$errorMessage = "异常的注册行为";
			$this->Monitor_model->logIllegalAction($errorMessage, $IP, $IParea, $time);
			return;
		}
		else if($password != $repass)//如果两次密码不一致
		{
			$json['status'] = "502";
			echo json_encode($json);//返回json结果
			return ;
		}
		else if($passwordLength < 8)//如果密码过短
		{
			$json['status'] = "503";
			echo json_encode($json);//返回json结果
			return ;
		}
		else if($passwordLength > 16)//如果密码过长
		{
			$json['status'] = "504";
			echo json_encode($json);//返回json结果
			return ;
		}
		else if($this->User_model->isEmailCover($email) == true)//如果email已存在
		{
			$json['status'] = "500";
			echo json_encode($json);//返回json结果
			return ;
		}
		else if($this->User_model->isUserNameCover($userName) == true)//如果用户名已存在
		{
			$json['status'] = "501";
			echo json_encode($json);//返回json结果
			return ;
		}
		$result = $this->User_model->register($email, $userName, $sex, $password, $IP, $time, $IParea);
		if($result == false)//如果插入错误
			$json['status'] = "600";//状态码600 表示未知的注册数据库错误
		echo json_encode($json);//返回json结果
		return ;
	}
}

?>
<?php
defined('BASEPATH') OR exit('No direct script access allowed');

//加载GatewayClient。关于GatewayClient参见本页面底部介绍
require_once 'GatewayClient/Gateway.php';
// GatewayClient 3.0.0版本开始要使用命名空间
use GatewayClient\Gateway;

class Login extends CI_Controller {

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
	public function login()
	{
		$json['status'] = "200";
		$email = $this->input->post('email');//获取用户提交的email
		$password = $this->input->post('password');//获取用户提交的password
		$IP = $this->IP_model->getIP();//获取用户IP
		$IParea = $this->IP_model->getIPArea($IP);//获取用户物理地址
		$time = $this->Common_model->getDate();//获取当前时间
		$this->Monitor_model->logLoginAction($email,$password,$IP,$IParea,$time);//记录本次登录行为
		if($email == null || $password == null)//遇到非法访问的时候
		{
			echo "大哥，请不要用奇怪的方式访问我！";
			$errorMessage = "异常的登录行为";
			$this->Monitor_model->logIllegalAction($errorMessage,$IP,$IParea,$time);//记录本次异常行为
			return ;
		}
		$res = $this->User_model->isEmailEqualPassword($email,$password);//比对登录信息
		if($res == false)//邮箱与密码不一致
		{
			$json['status'] = "500";
			echo json_encode($json);//返回json结果
			return ;
		}
		$json['userHead'] = $res['userHead'];
		$json['userName'] = $res['userName'];
		echo json_encode($json);//返回json结果
		return ;
	}
}
?>
<?php
defined('BASEPATH') OR exit('No direct script access allowed');
require ('Calendar.php');

//加载GatewayClient。关于GatewayClient参见本页面底部介绍
require_once 'GatewayClient/Gateway.php';
// GatewayClient 3.0.0版本开始要使用命名空间
use GatewayClient\Gateway;

class Wavelet extends CI_Controller {

	public function __construct()    //父类构造函数
	{
		parent::__construct();
	    $this->load->helper('path');
	    $this->load->helper('url');
	    $this->load->model('IP_model');//IP相关模块
	    $this->load->model('Monitor_model');//行为监控模块
	    Gateway::$registerAddress = $this->config->item('gateway_registerAddress');
	}

	public function upload()
	{
		$time = time();
		$rand = mt_rand(0,9999);
		$result['filename']= '/var/www/html/wavelet/'.$time.$rand.'.txt';
		$result['message'] = copy($_FILES["file"]["tmp_name"],$result['filename']);
		$json = json_encode($result);
		echo $json;
	}
	public function execute()
	{
		$dataTransform = $this->input->post("dataTransform");
		$thresholdRule = $this->input->post("thresholdRule");
		$thresholdMethod = $this->input->post("thresholdMethod");
		$filename = $this->input->post("filename");
		$mode = $this->input->post("mode") == 'on' ? '1' : '0';
		$commond = 'python /var/www/html/wavelet/wavelet.py '.$filename.' '.$dataTransform.' '.$thresholdRule.' '.$thresholdMethod.' '.$mode;
		$res = exec($commond,$output, $ret_code);
		$result['ret_code'] = $ret_code;
		$result['commond'] = $commond;
		$result['output'] = $output;
		$result['dataTransform'] = $dataTransform;
		$result['thresholdRule'] = $thresholdRule;
		$result['thresholdMethod'] = $thresholdMethod;
		$result['filename'] = $filename;
		$json = json_encode($result);
		echo $json;
	}


}
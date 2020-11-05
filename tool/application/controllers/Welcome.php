<?php
defined('BASEPATH') OR exit('No direct script access allowed');

//加载GatewayClient。关于GatewayClient参见本页面底部介绍
require_once 'GatewayClient/Gateway.php';
// GatewayClient 3.0.0版本开始要使用命名空间
use GatewayClient\Gateway;

class Welcome extends CI_Controller {

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
	public $host_url_main,$host_url_support,$host_url_local,$CDN_url_main,$CDN_url_support,$CDN_url_local,$ws_url;
	public function __construct()    //父类构造函数
	{
		parent::__construct();
		
	    $this->load->helper('path');
	    $this->load->helper('url');
	    #$this->load->model('IP_model');//IP相关模块
	    #$this->load->model('Monitor_model');//行为监控模块
	    //GatewayWorker框架的注册地址
	    Gateway::$registerAddress = $this->config->item('gateway_registerAddress');
	    //websocket URL
	    $this->ws_url = 'wss://jpcnbbs.wujingchi.com:8484';

	    //国内用户访问时 CI后端地址
	    $this->host_url_main = 'https://tool.wujingchi.com/index.php/';
	    //国外用户访问时 CI后端地址
	    $this->host_url_support = 'https://tool.wujingchi.com/index.php/';
	    //本地测试时 CI后端地址
	    $this->host_url_local = 'http://localhost/index.php/';
	    //$this->host_url_local = 'https://jpcnbbs.wujingchi.com/index.php/';
	    

	    //国内用户访问时 Limit 前端URL
		$this->CDN_url_main = 'https://tool.wujingchi.com/';
		//国外用户访问时 Limit 前端URL
		$this->CDN_url_support = 'https://tool.wujingchi.com/';
		//本地测试时 Limit 前端URL
		$this->CDN_url_local = 'http://localhost/';
		//$this->CDN_url_local = 'https://jpcnbbs.wujingchi.com/limit/';
	}
	public function info()
	{
		phpInfo();
	}
	public function index($pageName = 'waveletShrinkageEstimationTool')
	{
		//$IParea = $this->IP_model->getIPArea( $this->IP_model->getIP() );//获取用户国籍
		//$country = mb_substr($IParea,0,2,'utf-8');
		$country = "中国";
		$host_url = $this->autoChangeSiteUrl( $country );//根据国籍自动变换CI 后端URL
		$CDN_url = $this->autoChangeStaticUrl( $country );//根据国籍自动变换Limit 前端URL
		#$pageName = 'waveletShrinkageEstimationTool';//网页名称
		$config = array(
					'host_url'		=> $host_url,		//CI 后端URL
					'CDN_url'		=> $CDN_url,		//Limit 前端URL
					'ws_url'		=> $this->ws_url,	//websocket URL
					'isWebSocket'	=> false,			//是否开启webSocket
					'title' 		=> '呉敬馳のツール', 	//设置网页title
					'index_page'	=> 'index', 		//设置首页
					'animateTime'	=> '700',			//设置模块出现速度
					'shortcutIcon'	=> 'you.ico',		//设置网站小图标的路径( 相对于 $CDN_url/img/ )
					'pageName'		=> $pageName
					);
		$this->load->view($pageName,$config);
	}
	public function autoChangeSiteUrl( $country )
	{
		$host_url = false;
		if($country == "中国")
			$host_url = $this->host_url_main;
		if($country != "中国")
			$host_url = $this->host_url_support;
		if($country == "保留" || $country == '本机')
			$host_url = $this->host_url_local;
		return $host_url;
	}
	public function autoChangeStaticUrl( $country )
	{
		if($country == "中国")
			$this->config->set_item('base_url', $this->CDN_url_main);
		if($country != "中国")
			$this->config->set_item('base_url', $this->CDN_url_support);
		if($country == "保留" || $country == '本机')
			$this->config->set_item('base_url', $this->CDN_url_local);
		return $this->config->item('base_url');
	}
	public function ajaxTest()
	{
		$message['status'] = '200';
		echo json_encode($message);
	}
	public function test()
	{
		$this->load->view('test');
	}
}

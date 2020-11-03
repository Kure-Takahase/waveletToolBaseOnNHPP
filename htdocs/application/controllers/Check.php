<?php
defined('BASEPATH') OR exit('No direct script access allowed');
require ('Calendar.php');

class Check extends CI_Controller {

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
	    //$this->load->helper('path');
	    //$this->load->helper('url');
	}
	public function test()
	{
		
	}
	public function update()
	{
		$appid = $_GET['appid'];
		$version = $_GET['version'];//客户端版本号  
		$latest_version = "1.0.1";
		$rsp = array('status' => 0,'appid'=>$appid);//默认返回值，不需要升级
		if (isset($appid) && isset($version)) {
		    if($appid=="__W2A__jpcnbbs.wujingchi.com"){//校验appid
		        //这里是示例代码，真实业务上，最新版本号及relase notes可以存储在数据库或文件中  
		        if($version !== $latest_version){
		            $rsp['status'] = 1;
		            $rsp['title'] = "应用更新 " . $latest_version;
		            $rsp['note'] = "修复了已知的问题；\n优化了用户体验；";//release notes，支持换行
		            $rsp['url'] = "https://61jieyou.oss-cn-beijing.aliyuncs.com/jpcnbbs";//应用升级包下载地址
		        }
		    }
		}
		echo json_encode($rsp);
	}
}
?>
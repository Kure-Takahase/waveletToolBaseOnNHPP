<?php
defined('BASEPATH') OR exit('No direct script access allowed');

//加载GatewayClient。关于GatewayClient参见本页面底部介绍
require_once 'GatewayClient/Gateway.php';
// GatewayClient 3.0.0版本开始要使用命名空间
use GatewayClient\Gateway;

class User extends CI_Controller {

	/**
	 * interface List
	 * 1.getEmailByUserName()		根据userName查询email
	 * 2.getUserNameByEmail()		根据email查询userName
	 * 3.login()					登录
	 * 4.register()					注册
	 * 5.setUserName()				修改email的用户名为newUserName
	 */
	
	public function __construct()    //父类构造函数
	{
		parent::__construct();
	    $this->load->helper('path');
	    $this->load->helper('url');
	    $this->load->library('session');
	    $this->load->model('IP_model');//IP相关模块
	    $this->load->model('Common_model');//通用模块
	    $this->load->model('User_model');//用户信息模块
	    $this->load->model('Monitor_model');//行为监控模块
	    $this->load->model('Friend_model');
	    Gateway::$registerAddress = $this->config->item('gateway_registerAddress');
	}
	public function loginOut()
	{
		$client_id = $this->input->post('client_id');
		$email = $this->input->post('email');
		Gateway::unbindUid($client_id, $email);
		$this->session->sess_destroy();

		$friendList = $this->Friend_model->getFriendListByEmail($email);
		$offline_message['type']         = 'friendOnlineStatus';
        $offline_message['friendEmail']  = $email;
        $offline_message['isOnline']     = '0';
        $offline_message = json_encode($offline_message);
        foreach ($friendList as $key => $value)
        {
            Gateway::sendToUid($value['friend_email'], $offline_message);
        }
	}
	public function updateUserMessage()
	{
		//任何操作首先进行鉴权
		$email = $this->input->post('email');
		if($email != $this->session->email)//鉴权失败
		{
			session_write_close();
			//若鉴权失败，则尝试获取 email 与 password
			$password = $this->input->post('password');
			if($password == null)
				return;
			//尝试登录
			$result = $this->User_model->isEmailEqualPassword($email,$password);	
			if($result == false)
			{
				$message['status'] = '600';
				$message['content'] = 'userName or password incorret!';
				$json = json_encode($message);
				echo $json;//ajax 返回结果
				return ;
			}
		}
		session_write_close();
		$sex 	= $this->input->post('sex');
		$intro 	= $this->input->post('intro');
		$userName 	  = $this->input->post('userName');
		$result_email = $this->User_model->getEmailByUserName($userName);
		if($result_email != false && $result_email != $email) //如果用户名已被使用 且 被自己以外的用户使用
		{
			$message['status'] 	= '501';
			$message['message'] = 'UserName is covered!';
			$json = json_encode($message);
			echo $json;
			return ;
		}
		
		$message['email'] = $email;
		$message['userName'] = $userName;
		$message['sex'] = $sex;
		$message['intro'] = $intro;
		$result = $this->User_model->updateUserMessage($email,$userName,$sex,$intro);
		if($result == false) //如果发生数据库错误
		{
			$message['status'] 	= '502';
			$message['message'] = 'database error!';
			$json = json_encode($message);
			echo $json;
			return ;
		}
		$isPassword = $this->input->post('isPassword');
		//如果用户想修改密码
		if($isPassword == 1)
		{
			$old_pass = $this->input->post('old_pass');
			$new_pass = $this->input->post('new_pass');
			//尝试登录
			$result = $this->User_model->isEmailEqualPassword($email,$old_pass);	
			if($result == false)
			{
				$message['status'] = '503';
				$message['content'] = 'change password fail!userName or password incorret!';
				$json = json_encode($message);
				echo $json;//ajax 返回结果
				return ;
			}
			$this->User_model->setPassword($email,$new_pass);
		}
		$message['status'] = '200';
		$message['content'] = 'ok!';
		$json = json_encode($message);
		echo $json;//ajax 返回结果
	}
	public function getUserMessage()
	{
		//任何操作首先进行鉴权
		$email = $this->input->post('email');
		if($email != $this->session->email)//鉴权失败
		{
			session_write_close();
			//若鉴权失败，则尝试获取 email 与 password
			$password = $this->input->post('password');
			if($password == null)
				return;
			//尝试登录
			$result = $this->User_model->isEmailEqualPassword($email,$password);	
			if($result == false)
			{
				$message['status'] = '600';
				$message['content'] = 'userName or password incorret!';
				$json = json_encode($message);
				echo $json;//ajax 返回结果
				return ;
			}
		}
		session_write_close();
		//获取用户信息
		$userMessage = $this->User_model->getUserMessageByEmail($email);
		if($userMessage == false)
		{
			$message['status'] = '500';
			$json = json_encode($message);
			echo $json;
			return;
		}
		$message['status'] = '200';
		$message['userMessage'] = $userMessage;
		$json = json_encode($message);
		echo $json;
	}
	public function setUserName()
	{
		//任何操作首先进行鉴权
		$email = $this->input->post('email');
		if($email != $this->session->email)//鉴权失败
		{
			//session_write_close();
			return ;
		}
		//session_write_close();
		$newUserName = $this->input->post('newUserName');
		$message['type']	= 'RE'.'setUserName';
		$message['status'] 	= 'success';
		if($this->User_model->isUserNameCover($newUserName) == true)
		{
			$message['status'] 	= 'fail';
			$message['message'] = 'userName is cover!';
			$json = json_encode($message);
			Gateway::sendToUid($email, $json);
			return ;
		}
		$oldUserName = $this->session->userName;
		$result = $this->User_model->setUserName($email,$newUserName);
		if($result == false)
		{
			$message['status'] 	= 'fail';
			$message['message'] = 'unknow error!';
		}
		else
		{
			$message['newUserName'] = $newUserName;
			$this->session->set_userdata('userName', $newUserName);
			$this->Friend_model->setCandidateName($oldUserName,$newUserName);
			$this->Friend_model->setFriendName($oldUserName,$newUserName);
		}
		$my_session['color'] 	= $this->session->color;
		$my_session['email']	= $email;
		$my_session['userName'] = $userName;
		Gateway::setSession($client_id,$my_session);

		$json = json_encode($message);
		Gateway::sendToUid($email, $json);
	}
	//根据userName查询email
	public function getEmailByUserName()
	{
		$client_email = $this->session->email;
		session_write_close();
		if($client_email == null)
			return;
		$message['type'] = 'RE'.'getEmailByUserName';
		$message['status'] = 'success';
		$userName = $this->input->post('userName');
		$email = $this->User_model->getEmailByUserName($userName);
		if($email == false)
		{
			$message['status'] = 'fail';
			$json = json_encode($message);
			Gateway::sendToUid($client_email, $json);
		}
		$message['email'] = $email;
		$message['userName'] = $userName;
		$json = json_encode($message);
		Gateway::sendToUid($client_email, $json);

	}
	//根据email查询userName
	public function getUserNameByEmail()
	{
		$client_email = $this->session->email;
		session_write_close();
		if($client_email == null)
			return;
		$message['type'] = 'RE'.'getUserNameByEmail';
		$message['status'] = 'success';
		$email = $this->input->post('email');
		$userName = $this->User_model->getUserNameByEmail($email);
		if($userName == false)
		{
			$message['status'] = 'fail';
			$json = json_encode($message);
			Gateway::sendToUid($client_email, $json);
		}
		$message['email'] = $email;
		$message['userName'] = $userName;
		$json = json_encode($message);
		Gateway::sendToUid($client_email, $json);
	}
	//登录
	public function login()
	{
		$message['type'] = 'RE'.'login';
		$client_id	= $this->input->post('client_id');
		$email 		= $this->input->post('email');
		$password = $this->input->post('password');
		if($client_id == null || $email == null || $password == null)
			return ;
		$result = $this->User_model->isEmailEqualPassword($email,$password);	
		if($result == false)
		{
			$message['status'] = '500';
			$message['content'] = 'userName or password incorret!';
			$json = json_encode($message);
			Gateway::sendToClient($client_id, $json);//websocket 返回结果
			echo $json;//ajax 返回结果
			return ;
		}
		//如已有其他地点登录，则踢掉对方
		$isOnline = Gateway::getClientIdByUid($email);
		if($isOnline != null && $isOnline[0] != $client_id)
			Gateway::closeClient($isOnline[0]);
		$userName = $this->User_model->getUserNameByEmail($email);
		Gateway::bindUid($client_id, $email);
		$this->session->set_userdata('email', $email);
		$this->session->set_userdata('client_id', $client_id);
		//$this->session->set_userdata('userName', $userName);
		session_write_close();
		$message['status'] = '200';
		$message['email'] = $email;
		$message['userName'] = $userName;
		$message['userHead'] = $userName.".jpg";
		$message['content'] = 'I already know '.$client_id.' is '.$email;
		$json = json_encode($message);
		//websocket返回消息
		Gateway::sendToClient($client_id, $json);
		//ajax返回消息
		//echo $json;
		$my_session['email']	= $email;
		$my_session['userName'] = $userName;
		Gateway::setSession($client_id,$my_session);
		//通知该用户的所有好友 您的好友 已上线
		$friendList = $this->Friend_model->getFriendListByEmail($email);
		$online_message['type'] 		= 'friendOnlineStatus';
		$online_message['friendEmail']	= $email;
		$online_message['isOnline']	= '1';
		$online_message = json_encode($online_message);
		$message['friendList'] = $friendList;
		$json = json_encode($message);
		echo $json;
		if($friendList == false)
			return ;
		foreach ($friendList as $key => $value)
		{
			Gateway::sendToUid($value['friend_email'], $online_message);
		}
	}
	//注册
	public function register()
	{
		$message['type'] 	= 'RE'.'register';
		$message['status']	= '200';
		$message['message'] = 'register success!';
		$client_id		= $this->input->post('client_id');
		$email 			= $this->input->post('email');
		$userName 		= $this->input->post('userName');
		$password 		= $this->input->post('password');
		if($client_id == null || $email == null || $userName == null || $password == null)
			return ;
		$isEmailCover	= $this->User_model->isEmailCover($email);
		if($isEmailCover == true) //重复邮箱
		{
			$message['status'] 	= '500';
			$message['message'] = 'Email is covered!';
			$json = json_encode($message);
			Gateway::sendToClient($client_id, $json);
			echo $json;
			return ;
		}
		//不做重名判断
		$isUserNameCover = $this->User_model->isUserNameCover($userName);
		if($isUserNameCover == true) //重复用户名
		{
			$message['status'] 	= '501';
			$message['message'] = 'UserName is covered!';
			$json = json_encode($message);
			Gateway::sendToClient($client_id, $json);
			echo $json;
			return ;
		}
		$IP 	= $this->IP_model->getIP();
		$IParea	= $this->IP_model->getIPArea($IP);
		$time 	= $this->Common_model->getDate();
		$userID = $this->User_model->register($email, $userName, "1", $password, $IP, $time, $IParea);
		$this->session->set_userdata('email', $email);
		$this->session->set_userdata('userName', $userName);
		session_write_close();
		/* 不需要颜色系统
		$R = mt_rand(0,255);//Action
		$G = mt_rand(0,255);
		$B = mt_rand(0,255);
		$Rt = 255 - $R;		//HP
		$Gt = 255 - $G;
		$Bt = 255 - $B;
		$hexR = dechex($R);
		if(strlen($hexR) == 1)
			$hexR = '0'.$hexR;
		$hexG = dechex($G);
		if(strlen($hexG) == 1)
			$hexG = '0'.$hexG;
		$hexB = dechex($B);
		if(strlen($hexB) == 1)
			$hexB = '0'.$hexB;
		$color = $hexR.$hexG.$hexB;
		$userStatus['originalAction']	= $R;
		$userStatus['originalMaxHP']	= $Rt;
		$userStatus['originalDefense']	= $G;
		$userStatus['originalAttack'] 	= $Gt;
		$userStatus['originalDodge'] 	= $B;
		$userStatus['originalHit'] 		= $Bt;
		$userStatus['color']			= $color;
		$userStatus['email']			= $email;
		$this->UserStatus_model->createUserStatus($userStatus);
		$this->session->set_userdata('color', $color);
		$my_session['color'] 	= $color;
		$message['color'] = $color;
		*/
		/*添加头像*/
		copy('/var/www/html/jpcnbbs/limit/img/regular/unknow.jpg', '/var/www/html/jpcnbbs/limit/img/head/'.$userID.'.jpg');
		copy('/var/www/html/jpcnbbs/limit_jp/img/regular/unknow.jpg', '/var/www/html/jpcnbbs/limit_jp/img/head/'.$userID.'.jpg');
		//$message['url'] = '/var/www/html/jpcnbbs/limit/img/head/'.$userName.'.jpg';
		$message['email'] = $email;
		$message['userName'] = $userName;
		$json 	= json_encode($message);
		Gateway::bindUid($client_id, $email);
		Gateway::sendToClient($client_id, $json);
		echo $json;
		$my_session['email'] 	= $email;
		$my_session['userName'] = $userName;
		Gateway::setSession($client_id,$my_session);
	}
	public function uploadHead($email,$password)
	{
		$json['message'] = "ok";//默认表示成功
		if($_FILES["file"]["type"] == 'image/png' || $_FILES["file"]["type"] == 'image/jpg' || $_FILES["file"]["type"] == 'image/jpeg' || $_FILES["file"]["type"] == 'image/bmp' || $_FILES["file"]["type"] == 'image/gif')
		{

		}
		else
		{
			return "error";
		}
		$url = $_FILES["file"]["tmp_name"];
		$id = $this->User_model->getUserID($email,$password);
		if($id == false)
		{
			$json['email'] = $email;
			$json['password'] = $password;
			$json['message'] = "email or password error";
			echo json_encode($json);//返回json结果
			return ;
		}
		$url2 = "/var/www/html/jpcnbbs/limit/img/head/" . $id.".jpg";
	    //$url2 = "/var/www/html/jpcnbbs/limit/img/head/helloworld.jpg";
		$this->ImageToJPG($url,$url2,64,64);
		$json['url'] = $url;
		$json['url2'] = $url2;
		echo json_encode($json);//返回json结果
		return ;
	}
	public function changeHeadFile()
	{
		
	}
	function ImageToJPG($srcFile,$dstFile,$towidth,$toheight)
	{
		$quality=80;
		$data = @GetImageSize($srcFile);
		switch ($data['2'])
		{
		case 1:
			$im = imagecreatefromgif($srcFile);
			break;
		case 2:
			$im = imagecreatefromjpeg($srcFile);
			break;
		case 3:
			$im = imagecreatefrompng($srcFile);
			break;
		case 6:
			$im = ImageCreateFromBMP( $srcFile );
			break;
		}
		// $dstX=$srcW=@ImageSX($im);
		// $dstY=$srcH=@ImageSY($im);
		$srcW=@ImageSX($im);
		$srcH=@ImageSY($im);
		//$towidth,$toheight
		if($toheight/$srcW > $towidth/$srcH)
		{
			$b = $toheight/$srcH;
		}
		else
		{
			$b = $towidth/$srcW;
		}
		//计算出图片缩放后的宽高
		// floor 舍去小数点部分，取整
		$new_w = floor($srcW*$b);
		$new_h = floor($srcH*$b);
		$dstX=$new_w;
		$dstY=$new_h;
		$ni=@imageCreateTrueColor($dstX,$dstY);
		$white = @imagecolorallocate($ni, 255, 255, 255);
		@imagefill($ni, 0,0, $white);

		@ImageCopyResampled($ni,$im,0,0,0,0,$dstX,$dstY,$srcW,$srcH);
		@ImageJpeg($ni,$dstFile,$quality);
		@imagedestroy($im);
		@imagedestroy($ni);
	}

}
?>
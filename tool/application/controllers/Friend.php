<?php
defined('BASEPATH') OR exit('No direct script access allowed');

//加载GatewayClient。关于GatewayClient参见本页面底部介绍
require_once 'GatewayClient/Gateway.php';
// GatewayClient 3.0.0版本开始要使用命名空间
use GatewayClient\Gateway;

class Friend extends CI_Controller {

	/**
	 * interface List
	 * 1.getFriendList()			获取email 的所有好友
	 * 2.getFriendApplication()		获取email 的所有未处理的好友申请
	 * 3.friendApplicationReply()	处理好友申请回复
	 * 4.applicationAddFriend()		申请添加好友
	 * 5.deleteFriend()				删除好友
	 * 6.getChatHistory()			获取聊天记录
	 * 7.sendChatWordMessage()		发送聊天消息给好友
	 * 8.startChatWithFriend		开始与朋友开始私信交流(使未读信息置为已读，并设置session中当前聊天好友为friend)
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
	    $this->load->model('Friend_model');//好友系统模块
	    $this->load->model('UserStatus_model');//玩家状态模块
	    Gateway::$registerAddress = $this->config->item('gateway_registerAddress');
	}
	public function startChatWithFriend()
	{
		//任何操作首先进行鉴权
		$email = $this->input->post('email');
		if($email != $this->session->email)//鉴权失败
		{
			session_write_close();
			return ;
		}
		session_write_close();
		//获取收信方email
		$friendEmail = $this->input->post('friendEmail');
		if($friendEmail == null)
			return ;
		$message['type'] = 'RE'.'startChatWithFriend';
		if($this->Friend_model->isFriend($email,$friendEmail) == false)
		{
			$message['status']	= 'fail';
			$message['message'] = 'user is not your friend!';
			$json = json_encode($message);
			Gateway::sendToUid($email, $json);
			echo $json;
			return ;
		}
		$message['isOnline'] = '0';
		if(Gateway::isUidOnline($friendEmail) == true)
			$message['isOnline'] = '1';
		session_start();
		$this->session->set_userdata('chatFriend', $friendEmail);
		session_write_close();
		$result = $this->Friend_model->setUnreadMessage($email,$friendEmail,"0");
		$message['status'] 	= 'success';
		$message['message'] = 'ok';
		if($result == false)
		{
			$message['status'] 	= 'fail';
			$message['message'] = 'setUnreadMessage fail!';
		}
		$json = json_encode($message);
		Gateway::sendToUid($email, $json);
		echo $json;
	}
	public function sendChatWordMessage()
	{
		//任何操作首先进行鉴权
		$email = $this->input->post('email');
		if($email != $this->session->email)//鉴权失败
			return ;
		//获取收信方email
		$friendEmail = $this->input->post('friendEmail');
		if($friendEmail == null)
			return ;
		//拒绝空消息
		$content = $this->input->post('content');
		if($content == null)
			return ;
		//session快速确认是否是好友
		if($this->session->chatFriend != $friendEmail)
		{
			session_write_close();
			//数据库慢速确认
			if($this->Friend_model->isFriend($email,$friendEmail) == false)
			{
				return ;
			}
			session_start();
			$this->session->set_userdata('chatFriend', $friendEmail);
			session_write_close();
		}
		session_write_close();
		//转发给对方&自己
		$email_from_color = "000000";
		$time = $this->Common_model->getDate();
		$type = "newChatWordMessage";
		$message['type'] 		= $type;
		$message['email_from'] 	= $email;
		$message['email_from_color'] = $email_from_color;
		$message['email_to'] 	= $friendEmail;
		$message['content'] 	= $content;
		$message['time'] 		= $time;
		$json = json_encode($message);
		//如果对方在线，则直接发送
		if(Gateway::isUidOnline($friendEmail) == true)
			Gateway::sendToUid($friendEmail, $json);
		//不论是否在线，都使未读信息数加1
		//else//若不在线，则向数据库插入未读信息提示
			//$this->Friend_model->setUnreadMessage($friendEmail,$email,"1");
			$this->Friend_model->setUnreadMessageAuto($friendEmail,$email);//未读消息数自增1
		//同时发回自己
		Gateway::sendToUid($email, $json);
		//保存此条聊天记录
		$time = $this->Common_model->getDate();
		$kind = 'word';
		$src  = '';
		$this->Friend_model->saveChatMessage($email,$email_from_color,$friendEmail,$content,$kind,$src,$time);
	}
	public function getChatHistory()
	{
		//任何操作首先进行鉴权
		$email = $this->input->post('email');
		//if($email != $this->session->email)//鉴权失败
		//$message['session_email'] = $_SESSION['email'];
		//echo $_SESSION['email'];
		//if($email != $_SESSION['email'])//鉴权失败
		//	return ;
		//确认是否是好友
		$friendEmail = $this->input->post('friendEmail');
		if($friendEmail == null)
			return ;
		$isFriend = $this->Friend_model->isFriend($email,$friendEmail);
		$message['type'] = 'RE'.'getChatHistory';
		if($isFriend == false)
		{
			$message['status']	= 'fail';
			$message['message'] = 'user is not your friend!';
			$json = json_encode($message);
			Gateway::sendToUid($email, $json);
			echo $json;
			return ;
		}
		//读取七天内的聊天记录
		$time = date('Y-m-d H:i:s', strtotime('-7 days'));
		$result = $this->Friend_model->getChatHistoryAtTime($email,$friendEmail,$time);
		/*
		if($result->current_row == 0)
		{
			
			$message['status']	= 'fail';
			$message['time']	= $time;
			$message['message'] = 'unknow error!';
			$json = json_encode($message);
			Gateway::sendToUid($email, $json);
			echo $json;
			return ;
			
			$message['chatHistory'] = null;
		}
		else*/
		$message['chatHistory'] = $result;
		$message['status'] 	= 'success';
		$message['email'] 	= $email;
		$message['friendEmail'] = $friendEmail;
		
		$json = json_encode($message);
		Gateway::sendToUid($email, $json);
		echo $json;
	}
	//申请添加好友
	public function applicationAddFriend()
	{
		//任何操作首先进行鉴权
		$email = $this->input->post('email');
		if($email != $this->session->email)//鉴权失败
			return ;
		$message['type'] 		= 'RE'.'applicationAddFriend';
		$friendEmail = $this->input->post('friendEmail');
		//不允许添加自己
		if($email == $friendEmail)
		{
			$message['status'] 	= 'fail';
			$message['status_code'] = 501;
			$message['message'] = 'can not add yourself!';
			$json = json_encode($message);
			Gateway::sendToUid($email, $json);
			echo $json;
			return ;
		}
		//账户不存在
		$isEmailExist = $this->User_model->isEmailCover($friendEmail);
		if($isEmailExist == false)
		{
			$message['status'] 	= 'fail';
			$message['status_code'] = 502;
			$message['message'] = 'friend email not exist!';
			$json = json_encode($message);
			Gateway::sendToUid($email, $json);
			echo $json;
			return ;
		}
		//对方已经是你的好友
		$isFriend = $this->Friend_model->isFriend($email,$friendEmail);
		if($isFriend == true)
		{
			$message['status'] 	= 'fail';
			$message['status_code'] = 503;
			$message['message'] = 'friendEmail is already your friend!';
			$json = json_encode($message);
			Gateway::sendToUid($email, $json);
			echo $json;
			return ;
		}
		//好友申请重复发送
		$isSend = $this->Friend_model->isApplicationSend($email,$friendEmail);
		if($isSend == true)
		{
			$message['status'] 	= 'fail';
			$message['status_code'] = 504;
			$message['message'] = 'friendApplication is already sand!';
			$json = json_encode($message);
			Gateway::sendToUid($email, $json);
			echo $json;
			return ;
		}
		$emailUserName	= $this->User_model->getUserNameByEmail($email);
		$emailColor 	= "0000FF";
		$time 			= $this->Common_model->getDate();
		$result 		= $this->Friend_model->addFriendApplication($friendEmail,$email,$emailUserName,$emailColor,$time);
		$message['status'] 		= 'success';//成功发送好友申请
		$message['message'] 	= 'ok! success to send friend application!';
		$message['status_code'] = 200;
		if($result == false)//未知的错误
		{
			$message['status'] 	= 'fail';
			$message['status_code'] = 600;
			$message['message'] = 'unknow error!';
		}
		$json = json_encode($message);
		Gateway::sendToUid($email, $json);
		echo $json;
		$friendMessage['type'] 		= 'newFriendApp';
		$json = json_encode($friendMessage);
		Gateway::sendToUid($friendEmail, $json);
	}
	//删除好友
	public function deleteFriend()
	{
		//任何操作首先进行鉴权
		$email = $this->input->post('email');
		if($email != $this->session->email)//鉴权失败
			return ;
		$message['type']	= 'RE'.'deleteFriend';
		$message['status']	= 'fail';
		$friendEmail = $this->input->post('friendEmail');
		$res_one = $this->Friend_model->deleteFriendByEmail($email,$friendEmail);
		$res_two = $this->Friend_model->deleteFriendByEmail($friendEmail,$email);
		if($res_one != false && $res_two != false)
			$message['status'] = 'success';
		$json = json_encode($message);
		Gateway::sendToUid($email, $json);
	}
	//获取email 的所有好友
	public function getFriendList()
	{
		//任何操作首先进行鉴权
		$email = $this->input->post('email');
		if($email != $this->session->email)//鉴权失败
		{
			$message['my_email'] = $email;
			$message['session_email'] = $this->session->email;
			$message['message'] = 'error:session not find email';
			$json = json_encode($message);
			echo $json;
			return ;
		}	
		$result = $this->Friend_model->getFriendListByEmail($email);
		if($result == false)
		{	
			$message['message'] = 'error:not find friend';
			$json = json_encode($message);
			echo $json;
			return;
		}
		$message['type'] = 'RE'.'getFriendList';
		$online_user = array();
		$offline_user = array();
		foreach ($result as $key => $user)
		{
			$isUidOnline = Gateway::isUidOnline($user['friend_email']);
			if($isUidOnline == true)
			{
				$user['result'] = $isUidOnline;
				$user['isOnline'] = true;
				$online_user[] = $user;
			}
			else
			{
				$user['result'] = $isUidOnline;
				$user['isOnline'] = false;
				$offline_user[] = $user;
			}
		}
		$result = array_merge($online_user,$offline_user);
		$message['data'] = $result;
		$message['status'] = '200';
		$json = json_encode($message);
		Gateway::sendToUid($email, $json);
		echo $json;
	}
	//获取email 的所有未处理的好友申请
	public function getFriendApplication()
	{
		//任何操作首先进行鉴权
		$email = $this->input->post('email');
		if($email != $this->session->email)//鉴权失败
		{
			$message['type'] 		= 'RE'.'getFriendApplication';
			$message['message']		= 'email fail';
			$message['email']		= $email;
			$message['session']		= $this->session->email;
			$json = json_encode($message);
			echo $json;
			return ;
		}
		$result = $this->Friend_model->getFriendApplicationByEmail($email);
		if($result == false)
		{
			$message['type'] 		= 'RE'.'getFriendApplication';
			$message['status']		= '201';
			$message['message']		= 'no friend app';
			$json = json_encode($message);
			echo $json;
			return;
		}
		$message['status']		= '200';
		$message['type'] 		= 'RE'.'getFriendApplication';
		$message['data']		= $result;
		$json = json_encode($message);
		Gateway::sendToUid($email, $json);
		echo $json;
	}
	//处理好友申请回复
	public function friendApplicationReply()
	{
		//任何操作首先进行鉴权
		$email = $this->input->post('email');
		if($email != $this->session->email)//鉴权失败
			return ;
		$listID = $this->input->post('listID');
		$reply = $this->input->post('reply');
		$message['type'] 	= 'RE'.'friendApplicationReply';
		$message['status']	= 'success';
		$message['message']	= 'ok';
		if($reply == 'refuse')//若拒绝添加，则直接删除该条通知
		{
			$result = $this->Friend_model->deleteFriendApplicationByListID($listID);
			if($result == false)
			{
				$message['status']	= 'fail';
				$message['message']	= 'deleteFriendApplicationByListID fail!';
			}
			$json = json_encode($message);
			Gateway::sendToUid($email, $json);
			echo $json;
			return;
		}
		if($reply == 'agree')//若同意添加，则删除该条通知的基础上，还互相添加到对方的好友列表
		{
			//获取好友申请通知
			$notice = $this->Friend_model->getFriendApplicationByListID($listID);
			if($notice == false)
			{
				$message['status']	= 'fail';
				$message['message']	= 'getNoticeByListID fail!';
				$json = json_encode($message);
				Gateway::sendToUid($email, $json);
				echo $json;
				return;
			}
			//互相添加好友
			$candidateEmail = $notice['candidate_email'];
			$candidateUserName =  $this->User_model->getUserNameByEmail($candidateEmail);
			$emailUserName = $this->User_model->getUserNameByEmail($email);
			$this->Friend_model->addFriend($email,$candidateEmail,$candidateUserName);
			$this->Friend_model->addFriend($candidateEmail,$email,$emailUserName);
			//删除此条通知
			$result = $this->Friend_model->deleteFriendApplicationByListID($listID);
			if($result == false)
			{
				$message['status']	= 'fail';
				$message['message']	= 'deleteSystemTextByListID fail!';
				$json = json_encode($message);
				Gateway::sendToUid($email, $json);
				echo $json;
				return;
			}
			//返回结果
			$json = json_encode($message);
			Gateway::sendToUid($email, $json);
			echo $json;
			$friendMessage['type'] = 'newFriendList';
			$json = json_encode($friendMessage);
			Gateway::sendToUid($candidateEmail, $json);
			return;
		}
	}

}
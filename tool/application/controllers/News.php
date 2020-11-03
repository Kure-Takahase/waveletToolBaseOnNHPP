<?php
defined('BASEPATH') OR exit('No direct script access allowed');
require ('Calendar.php');

//加载GatewayClient。关于GatewayClient参见本页面底部介绍
require_once 'GatewayClient/Gateway.php';
// GatewayClient 3.0.0版本开始要使用命名空间
use GatewayClient\Gateway;

class News extends CI_Controller {

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
	    $this->load->model('News_model');//BBS模块
	    Gateway::$registerAddress = $this->config->item('gateway_registerAddress');
	}
	/**
	 * 查询是否有比time更新的评论。
	 * @return [type] [description]
	 */
	public function ifHaveNewComment()
	{
		$json['status'] = '201';//默认为没有新评论
		$TieID = $this->input->post('tieID');
		$time = $this->input->post('time');
		if($time == null || $TieID == null)
		{
			$json['status'] = '500';//参数格式错误
			echo json_encode($json);
			return ;
		}
		$result = $this->News_model->ifHaveNewComment($TieID, $time);
		$json['tieID'] = $TieID;
		if($result == true)
			$json['status'] = '200';//有新评论
		echo json_encode($json);
		return ;
	}
	/**
	 * 查询是否有比time更新的帖子。
	 * @return [type] [description]
	 */
	public function ifHaveNewTie()
	{
		$json['status'] = '201';//默认为没有新帖子
		$time = $this->input->post('time');
		if($time == null)
		{
			$json['status'] = '500';//参数格式错误
			echo json_encode($json);
			return ;
		}
		$result = $this->News_model->ifHaveNewTie($time);
		if($result == true)
			$json['status'] = '200';//有新帖子
		echo json_encode($json);
		return ;
	}
	public function addComment()
	{
		$json['status'] = '200';
		$tieID = $this->input->post('tieID');
		$comment = $this->input->post('comment');
		$userName = $this->input->post('userName');
		$userHead = "../regular/unknow.jpg";
		$email = $this->input->post('email');
		$password = $this->input->post('password');
		$IP = $this->IP_model->getIP();
		$IParea = $this->IP_model->getIPArea($IP);
		$time = $this->Common_model->getDate();
		if($tieID == null || $tieID < 0 || $comment == null)
		{
			echo "大哥，请不要用奇怪的方式访问我！";
			$message = "异常的发评论行为";
			$this->Monitor_model->logIllegalAction($message, $IP, $IParea, $time);
			return;
		}
		if($userName == null)
		{
			$userName = "匿名用户";
		}	
		else
		{
			$res = $this->User_model->isEmailEqualPassword($email,$password);
			if($res != false)
			{
				$userName = $res['userName'];
				$userHead = $res['userHead'];
			}	
			else
				$userName = "匿名用户";
		}
		$json['tieID'] = $tieID;
		$result = $this->News_model->addComment($tieID, $comment, $userName, $userHead, $IP, $IParea, $time);
		if($result == false)
		{
			$json['status'] = '600';//未知的数据库错误
			echo json_encode($json);
			return ;
		}
		echo json_encode($json);
		return ;
	}
	public function getComment()
	{
		$json['status'] = '200';
		$json['count'] = "0";
		$tieID = $this->input->post('tieID');
		$page = $this->input->post('page');
		$ifNeedCount = $this->input->post('ifNeedCount');
		$once = "5";
		//$tieID = "75";
		//$page = "1";
		//$ifNeedCount = "yes";
		$result = $this->News_model->getComment($tieID, $page, $once);
		if($result == false)
		{
			$json['status'] = '201';//未知的数据库错误
			echo json_encode($json);
			return ;
		}
		if($ifNeedCount == "yes")
			$json['count'] = $this->News_model->getCommentCount($tieID);
		$json['tieID'] = $tieID;
		$json['comment'] = $result;
		echo json_encode($json);
		return ;
	}
	public function getTieByID()
	{
		$json['status'] = '200';
		$ID = $this->input->post('ID');
		$result = $this->News_model->getPostByID($ID);
		if($result == false)
		{
			$json['status'] = '600'; //未知的数据库错误
			echo json_encode($json);
			return ;
		}
		$json['data'] = $result;
		echo json_encode($json);
		return ;
	}
	public function getTieGreaterThanID()
	{
		$json['status'] = '200';//有新帖子
		$ID = $this->input->post('ID');
		if($ID == null || $ID < 0)
		{
			echo "大哥，请不要用奇怪的方式访问我！";
			$time = $this->Common_model->getDate();
			$IP = $this->IP_model->getIP();
			$IParea = $this->IP_model->getIPArea($IP);
			$message = "异常的更新首页帖子行为G";
			$this->Monitor_model->logIllegalAction($message, $IP, $IParea, $time);
			return;
		}
		$res = $this->News_model->getPostAndGuaGreaterThanID($ID);
		if($res == null)
		{
			$json['status'] = '201';//没有更新的帖子
			echo json_encode($json);
			return ;
		}
		$json['data'] = $res;
		echo json_encode($json);
		return ;
	}
	public function getTieLessThanID()
	{
		$json['status'] = '200';//有更早的帖子
		$ID = $this->input->post('ID');
		$sum = $this->input->post('sum');
		if($ID == null || $ID < 0 || $sum == null || $sum <= 0)
		{
			echo "大哥，请不要用奇怪的方式访问我！";
			$time = $this->Common_model->getDate();
			$IP = $this->IP_model->getIP();
			$IParea = $this->IP_model->getIPArea($IP);
			$message = "异常的更新首页帖子行为L";
			$this->Monitor_model->logIllegalAction($message, $IP, $IParea, $time);
			return;
		}
		$res = $this->News_model->getPostAndGuaLessThanID($ID,$sum);
		if($res == null)
		{
			$json['status'] = '201';//没有更早的帖子
			echo json_encode($json);
			return ;
		}
		$json['data'] = $res;
		echo json_encode($json);
		return ;
	}
	public function getTieGreaterThanTime()
	{
		$json['status'] = '200';//有新帖子
		$time = $this->input->post('time');
		if($time == null || $time < 0)
		{
			echo "大哥，请不要用奇怪的方式访问我！";
			$time = $this->Common_model->getDate();
			$IP = $this->IP_model->getIP();
			$IParea = $this->IP_model->getIPArea($IP);
			$message = "异常的更新首页帖子行为G";
			$this->Monitor_model->logIllegalAction($message, $IP, $IParea, $time);
			return;
		}
		$res = $this->News_model->getPostAndGuaGreaterThanTime($time);
		if($res == null)
		{
			$json['status'] = '201';//没有更新的帖子
			echo json_encode($json);
			return ;
		}
		$json['data'] = $res;
		echo json_encode($json);
		return ;
	}
	public function getTieLessThanTime()
	{
		$json['status'] = '200';//有更早的帖子
		$time = $this->input->post('time');
		$sum = $this->input->post('sum');
		if($time == null || $time < 0 || $sum == null || $sum <= 0)
		{
			echo "大哥，请不要用奇怪的方式访问我！";
			$time = $this->Common_model->getDate();
			$IP = $this->IP_model->getIP();
			$IParea = $this->IP_model->getIPArea($IP);
			$message = "异常的更新首页帖子行为L";
			$this->Monitor_model->logIllegalAction($message, $IP, $IParea, $time);
			return;
		}
		$res = $this->News_model->getPostAndGuaLessThanTime($time,$sum);
		if($res == null)
		{
			$json['status'] = '201';//没有更早的帖子
			echo json_encode($json);
			return ;
		}
		$json['data'] = $res;
		echo json_encode($json);
		return ;
	}
	public function getNews()
	{
		$json['status'] = '200';
		$sum = $this->input->post('sum');
		if($sum == null || $sum > 100 || $sum <= 0)
		{
			echo "大哥，请不要用奇怪的方式访问我！";
			$time = $this->Common_model->getDate();
			$IP = $this->IP_model->getIP();
			$IParea = $this->IP_model->getIPArea($IP);
			$message = "异常的获取首页帖子行为";
			$this->Monitor_model->logIllegalAction($message, $IP, $IParea, $time);
			return;
		}
		$res = $this->News_model->getLatestPostAndGua($sum);
		if($res == null)
		{
			$json['status'] = '600';//未知的数据库错误
			echo json_encode($json);
			return ;
		}
		$json['data'] = $res;
		echo json_encode($json);
		return ;
	}
	public function post()
	{
		$json['status'] = '200';//成功发布哈有卦贴
		$email = $this->input->post('email');
		$password = $this->input->post('password');
		$userName = "匿名用户";
		$userHead = "unknow.jpg";
		$res = $this->User_model->isEmailEqualPassword($email, $password);
		if($userName != false)
		{
			$userName = $res['userName'];
			$userHead = $res['userHead'];
		}
		if($res['userName'] == "")
		{
			$userName = "匿名用户";
			$userHead = "unknow.jpg";
		}	
		$content = $this->input->post('content');
		$title = $this->input->post('title');
		$time = $this->Common_model->getDate();
		$IP = $this->IP_model->getIP();
		$IParea = $this->IP_model->getIPArea($IP);
		if($content == null || $title == null)
		{
			echo "大哥，请不要用奇怪的方式访问我！";
			$message = "异常的发帖行为";
			$this->Monitor_model->logIllegalAction($message, $IP, $IParea, $time);
			return;
		}
		$tieID = $this->News_model->newPost($title, $content, $userName, $userHead, $IP, $IParea, $time);
		if($tieID == false)
		{
			$json['status'] = '600';//未知的数据库错误
			echo json_encode($json);
			return ;
		}
		$ifGua = $this->input->post('ifGua');
		if($ifGua == "no")
		{
			$this->News_model->setIfGua($tieID, $ifGua);
			$json['status'] = '201';//表示成功发布无卦帖
		}
		else
		{
			//新增卦
			$year = $this->Common_model->getYear();
			$month = $this->Common_model->getMonth();
			$day = $this->Common_model->getDay();
			$calendar = new \Overtrue\ChineseCalendar\Calendar();
			$result = $calendar->solar($year, $month, $day); // 阳历
			$ganzhi_year = $result['ganzhi_year'];
			$ganzhi_month = $result['ganzhi_month'];
			$ganzhi_day = $result['ganzhi_day'];
			$age = $this->input->post('age');
			$sex = $this->input->post('sex');
			$what = $this->input->post('what');
			$nowGua = $this->input->post('nowGua');
			$nowBianGua = $this->input->post('nowBianGua');
			$nowGuaS = $this->input->post('nowGuaS');
			$nowGuaX = $this->input->post('nowGuaX');
			$nowGuaSB = $this->input->post('nowGuaSB');
			$nowGuaXB = $this->input->post('nowGuaXB');
			$nowGuaTotal = $this->input->post('nowGuaTotal');
			$nowGuaTotalB = $this->input->post('nowGuaTotalB');

			$guaID = $this->News_model->newGua($year,$month,$day,$ganzhi_year,$ganzhi_month,$ganzhi_day,$age,$sex,$what,$nowGua,$nowBianGua,$nowGuaS,$nowGuaX,$nowGuaSB,$nowGuaXB,$nowGuaTotal,$nowGuaTotalB,$time,$userName,$IP,$IParea);
			if($guaID == false)
				$json['status'] = '500';
			else
				$this->News_model->setIfGua($tieID, $ifGua, $guaID);
		}
		echo json_encode($json);
		return ;
	}












	public function adminPost()
	{
		$json['status'] = '200';
		$email = $this->input->post('email');
		$password = $this->input->post('password');
		/*
		if($email != "1442827233@jieyou.com" || $password!="q1234567890")
		{
			$json['status'] = '500';
			echo json_encode($json);
			return ;
		}*/
		
		$title = $this->input->post('title');
		$content = $this->input->post('content');
		$userName = $this->input->post('userName');
		$userHead = $this->input->post('userHead');
		$time = $this->input->post('time');
		$IP = $this->IP_model->getIP();
		$IParea = $this->IP_model->getIPArea($IP);

/*
		$title = "title";
		$content = "content";
		$userName = "userName";
		$userHead = "userHead";
		$time = "time";

*/


		$tieID = $this->News_model->newPost($title, $content, $userName, $userHead, $IP, $IParea, $time);
		if($this->User_model->isUserNameCover($userName) == false)//如果用户名不存在
			$this->User_model->register("text@qq.com", $userName, "女", "123456", $IP, $time, $IParea);
		if($tieID == false)
		{
			$json['status'] = '600';//未知的数据库错误
			echo json_encode($json);
			return ;
		}
		$json['tieID'] = $tieID;
		$ifGua = $this->input->post('ifGua');
		if($ifGua == "no")
		{
			$this->News_model->setIfGua($tieID, $ifGua);
			$json['status'] = '201';//表示成功发布无卦帖
		}
		else
		{
			//新增卦
			$year = $this->input->post('year');
			$month = $this->input->post('month');
			$day = $this->input->post('day');
			$json['year'] = $year;
			$json['month'] = $month;
			$json['day'] = $day;
			/*
			echo json_encode($json);
			return ;
			$year = "2018";
			$month = "12";
			$day = "7";
			*/

			$calendar = new \Overtrue\ChineseCalendar\Calendar();
			$result = $calendar->solar($year, $month, $day); // 阳历
			$ganzhi_year = $result['ganzhi_year'];
			$ganzhi_month = $result['ganzhi_month'];
			$ganzhi_day = $result['ganzhi_day'];
			$age = $this->input->post('age');
			$sex = $this->input->post('sex');
			$nowGua = $this->input->post('nowGua');
			$nowBianGua = $this->input->post('nowBianGua');
			$nowGuaS = $this->input->post('nowGuaS');
			$nowGuaX = $this->input->post('nowGuaX');
			$nowGuaSB = $this->input->post('nowGuaSB');
			$nowGuaXB = $this->input->post('nowGuaXB');
			$nowGuaTotal = $this->input->post('nowGuaTotal');
			$nowGuaTotalB = $this->input->post('nowGuaTotalB');
			$what= "0";
			$guaID = $this->News_model->newGua($year,$month,$day,$ganzhi_year,$ganzhi_month,$ganzhi_day,$age,$sex,$what,$nowGua,$nowBianGua,$nowGuaS,$nowGuaX,$nowGuaSB,$nowGuaXB,$nowGuaTotal,$nowGuaTotalB,$time,$userName,$IP,$IParea);
			if($guaID == false)
				$json['status'] = '501';
			else
				$this->News_model->setIfGua($tieID, $ifGua, $guaID);
		}
		echo json_encode($json);
		return ;
	}
	public function adminComment()
	{
		$email = $this->input->post('email');
		$password = $this->input->post('password');
		if($email != "1442827233@jieyou.com" || $password!="q1234567890")
		{
			$json['status'] = '500';
			echo json_encode($json);
			return ;
		}
		$json['status'] = '200';
		$tieID = $this->input->post('tieID');
		$comment = $this->input->post('comment');
		$userName = $this->input->post('userName');
		$userHead = $this->input->post('userHead');
		$IP = $this->IP_model->getIP();
		$IParea = $this->IP_model->getIPArea($IP);
		$time = $this->input->post('time');
		if($this->User_model->isUserNameCover($userName) == false)//如果用户名不存在
			$this->User_model->register("text@qq.com", $userName, "女", "123456", $IP, $time, $IParea);
		$result = $this->News_model->addComment($tieID, $comment, $userName, $userHead, $IP, $IParea, $time);
		if($result == false)
		{
			$json['status'] = '600';//未知的数据库错误
			echo json_encode($json);
			return ;
		}
		echo json_encode($json);
		return ;
	}

}
?>
<?php
class Monitor_model extends CI_Model 
{

	/**
	 * 提供的方法：
	 * 		1.getIP()
	 * 			返回用户IP地址
	 * 		2.getIPArea($IP)
	 * 	 		返回$IP所对应的物理地址
	 * 	 		数据来源为：本地IP库 → 聚合数据(每日500条)
	 */
    public function __construct()
    {
    	parent::__construct();
        $this->load->database();
    }
    public function logVisitAction($IP, $IParea, $time)
    {
        $sql = "INSERT INTO visitlist (IP,IParea,time) VALUES ('".$IP."','".$IParea."','".$time."')";
        return $this->db->query($sql);
    }
    /**
     * 记录一次注册行为(不论是否成功登录)到表registerList
     * @param  string  $email    用户此次注册的邮箱
     * @param  string  $userName 用户此次注册的用户名
     * @param  string  $password 用户此次注册的密码
     * @param  string  $password 用户此次注册的重复密码
     * @param  string  $IP       当前用户IP
     * @param  string  $IParea   当前用户物理位置
     * @param  string  $time     当前时间
     * @return boolean          成功保存返回true 否则返回false
     */
    public function logRegisterAction($email, $userName, $password, $repass, $IP, $IParea, $time)
    {
    	$sql = "INSERT INTO registerlist (email,userName,password,repass,IP,IParea,time) VALUES ('".$email."','".$userName."','".$password."','".$repass."','".$IP."','".$IParea."','".$time."')";
		return $this->db->query($sql);
    }
    /**
     * 记录一次登录行为(不论是否成功登录)到表loginList
     * @param  string  $email    用户此次使用的邮箱
     * @param  string  $password 用户此次使用的密码
     * @param  string  $IP       当前用户IP
     * @param  string  $IParea   当前用户物理位置
     * @param  string  $time     当前时间
     * @return boolean          成功保存返回true 否则返回false
     */
    public function logLoginAction($email, $password, $IP, $IParea, $time)
    {
    	$sql = "INSERT INTO loginlist (email,password,IP,IParea,time) VALUES ('".$email."','".$password."', '".$IP."','".$IParea."','".$time."')";
		return $this->db->query($sql);
    }

    /**
     * 记录一次异常的行为到表error
     * @param  string  $errorMessage 异常信息
     * @param  string  $IP           异常行为者的IP地址
     * @param  string  $IParea       异常行为者的物理地址
     * @param  string  $time         异常行为的时间
     * @return boolean              成功保存返回true 否则返回false
     */
    public function logIllegalAction($errorMessage, $IP, $IParea, $time)
    {
    	$sql = "INSERT INTO error (message,IP,IParea,time) VALUES ('".$errorMessage."', '".$IP."','".$IParea."','".$time."')";
    	return $this->db->query($sql);
    }
}
?>
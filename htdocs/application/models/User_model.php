<?php
class User_model extends CI_Model 
{
    
    public function __construct()
    {
    	parent::__construct();
        $this->load->database();
    }
    public function changeHeadFile()
    {
        $sql = "SELECT * FROM user";
        $result = $this->db->query($sql);//发送给数据库，请求保存
        return $result->result_array();
    }
    public function changeHead()
    {
        $sql = "SELECT * FROM user";
        $result = $this->db->query($sql);//发送给数据库，请求保存
        foreach ($result->result_array() as $key => $value) 
        {
            $sql = "UPDATE user SET head = '".$value['id'].".jpg' WHERE id = '".$value['id']."'";//构造数据库请求
            $this->db->query($sql);//发送给数据库，请求保存
        }
    }
    public function getUserID($email,$password)
    {
        $sql = "SELECT id FROM user WHERE email = '".$email."' and password = '".$password."'";
        $result = $this->db->query($sql);//发送给数据库，请求保存
        if($result->result_array() == null)
            return false;
        return  $result->result_array()[0]['id'];
    }
    //修改email 的密码 为 new_pass
    public function setPassword($email,$new_pass)
    {
        $sql = "UPDATE user SET password = '".$new_pass."' WHERE email = '".$email."'";//构造数据库请求
        return $this->db->query($sql);//发送给数据库，请求保存
    }
    public function updateUserMessage($email,$userName,$sex,$intro)
    {
        $sql = "UPDATE user SET userName = '".$userName."', sex = '".$sex."' ,intro = '".$intro."' WHERE email = '".$email."'";//构造数据库请求
        return $this->db->query($sql);//发送给数据库，请求保存
    }
    //修改email 的用户名 为 newUserName
    public function setUserName($email,$newUserName)
    {
        $sql = "UPDATE user SET userName = '".$newUserName."' WHERE email = '".$email."'";//构造数据库请求
        return $this->db->query($sql);//发送给数据库，请求保存
    }
    /**
     * 根据userName获取头像
     * @param  [type] $userName [description]
     * @return [type]           [description]
     */
    public function getUserHeadByUserName($userName)
    {
    	$this->load->helper('url');
    	$sql = "SELECT head FROM user WHERE userName = '".$userName."'";
    	$result = $this->db->query($sql);//发送给数据库，请求保存
		if($result->result_array() == null)
			return false;
		return base_url('/img/head/').$result->result_array()[0]['head'];
    }
    /**
     * 根据邮箱获取用户信息
     * @param  [type] $email [description]
     * @return [type]        [description]
     */
    public function getUserMessageByEmail($email)
    {
        $sql = "SELECT * FROM user WHERE email = '".$email."'";
        $result = $this->db->query($sql);//发送给数据库，请求保存
        if($result->result_array() == null)
            return false;
        return $result->result_array()[0];
    }
    /**
     * 根据邮箱获取用户名
     * @param  [type] $userName [description]
     * @return [type]           [description]
     */
    public function getUserNameByEmail($email)
    {
    	$sql = "SELECT userName FROM user WHERE email = '".$email."'";
    	$result = $this->db->query($sql);//发送给数据库，请求保存
		if($result->result_array() == null)
			return false;
		return $result->result_array()[0]['userName'];
    }
    /**
     * 根据用户名获取邮箱
     * @param  [type] $userName [description]
     * @return [type]           [description]
     */
    public function getEmailByUserName($userName)
    {
        $sql = "SELECT email FROM user WHERE userName = '".$userName."'";
        $result = $this->db->query($sql);//发送给数据库，请求保存
        if($result->result_array() == null)
            return false;
        return $result->result_array()[0]['email'];
    }
    /**
     * 向表user 插入一条新用户信息
     * @param  string $email    新用户的邮箱
     * @param  string $userName 新用户的用户名
     * @param  string $sex      新用户的性别
     * @param  string $password 新用户的密码
     * @param  string $IP       新用户注册时的IP地址
     * @param  string $time     新用户的注册时间
     * @param  string $IParea   新用户注册时的物理地址
     * @return boolean          成功返回true，失败返回false
     */
    public function register($email, $userName, $sex, $password, $IP, $time, $IParea)
    {
    	$sql = "INSERT INTO user (email, userName,sex,password,registerIP,registerTime,registerArea,intro,head) VALUES ('".$email."', '".$userName."','".$sex."','".$password."','".$IP."','".$time."','".$IParea."','很高兴认识大家~','".$userName.".jpg')";//构造数据库请求
        $res = $this->db->query($sql);//发送给数据库，请求保存
        if($res != false)
        {
            $sql = "SELECT id FROM user WHERE email = '".$email."'";
            $result = $this->db->query($sql);//发送给数据库，请求保存
            if($result->result_array() == null)
                return false;
            $id = $result->result_array()[0]['id'];
            $sql = "UPDATE user SET head = '".$id.".jpg' WHERE email = '".$email."'";//构造数据库请求
            $this->db->query($sql);
            return $id;//发送给数据库，请求保存
        }
        else
            return false;
    }

    /**
     * 查询 $email 和 $password 是否是表user中的用户
     * @param  string  $email    待查询的邮箱
     * @param  string  $password 待查询的密码
     * @return boolean           若该邮箱/密码组合是表user中的用户,则返回userName，否则返回false
     */
    public function isEmailEqualPassword($email,$password)
	{
		$sql = "SELECT userName,head FROM user WHERE email = '".$email."' AND password = '".$password."'";//构造数据库请求
		$result = $this->db->query($sql);//发送给数据库，请求保存
		if($result->result_array() == null)
			return false;
		$res['userName'] = $result->result_array()[0]['userName'];
		$res['userHead'] = $result->result_array()[0]['head'];
 		return $res;
	}
	/**
	 * 查询 表user 中是否存在与 $email email
	 * @param  string  $email 待查询的email
	 * @return boolean        存在相同的email返回true，否则返回false
	 */
	public function isEmailCover($email)
	{
		$sql = "SELECT email FROM user WHERE email = '".$email."'";//构造数据库请求
		$result = $this->db->query($sql);//发送给数据库，请求保存
		if($result->result_array() == null)
			return false;
		return true;
	}
	/**
	 * 查询 表user 中是否存在与 $userName 相同的userName
	 * @param  string  $userName 待查询的用户名
	 * @return boolean           存在相同的userName返回true，否则返回false
	 */
	public function isUserNameCover($userName)
	{
		$sql = "SELECT userName FROM user WHERE userName = '".$userName."'";//构造数据库请求
		$result = $this->db->query($sql);//发送给数据库，请求保存
		if($result->result_array() == null)
			return false;
		return true;
	}
}
?>
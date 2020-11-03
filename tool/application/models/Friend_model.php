<?php
class Friend_model extends CI_Model
{
    public function __construct()
    {
    	parent::__construct();
        $this->load->database();
    }
    //获取 time ~ 当前时间 之间的所有聊天记录
    public function getChatHistoryAtTime($email,$friendEmail,$time)
    {
        $isSuccess = false;
        //获取time以前的email发送给friendEmail的聊天记录
        $sql = "SELECT * FROM user_chat_history WHERE (email_from = '".$email."' and email_to = '".$friendEmail."' and time > '".$time."' ) or (email_from = '".$friendEmail."' and email_to = '".$email."' and time > '".$time."')";
        $result_one = $this->db->query($sql);//发送给数据库，请求保存
        return $result_one->result_array();
        //获取time以前的friendEmail发送给email的聊天记录
        $sql = "SELECT * FROM user_chat_history";
        $result_two = $this->db->query($sql);//发送给数据库，请求保存
        var_dump($result_two);
        var_dump($result_two->result_array());
        
        return $result_two;
        //return array_merge($result_one->result_array(),$result_two->result_array());
    }
    //保存email发送给friendEmail的聊天记录
    public function saveChatMessage($email,$email_from_color,$friendEmail,$content,$kind,$src,$time)
    {
        $sql = "INSERT INTO user_chat_history (email_from,email_from_color, email_to,content,kind,src,time) VALUES ('".$email."','".$email_from_color."' ,'".$friendEmail."','".$content."','".$kind."','".$src."','".$time."')";//构造数据库请求
        return $this->db->query($sql);//发送给数据库，请求保存
    }
    //告诉email有来自friendEmail的未读信息
    public function setUnreadMessage($email,$friendEmail,$status)
    {
        $sql = "UPDATE friend_list SET unread_message = '".$status."' WHERE email = '".$email."' and friend_email = '".$friendEmail."'";//构造数据库请求
        return $this->db->query($sql);//发送给数据库，请求保存
    }
    //未读消息数自增1
    public function setUnreadMessageAuto($email,$friendEmail)
    {
        $sql = "UPDATE friend_list SET unread_message = unread_message + 1 WHERE email = '".$email."' and friend_email = '".$friendEmail."'";//构造数据库请求
        return $this->db->query($sql);//发送给数据库，请求保存
    }
    //email的好友列表中是否有friendEmail
    public function isFriend($email,$friendEmail)
    {
        $sql = "SELECT * FROM friend_list WHERE email = '".$email."' and friend_email = '".$friendEmail."'";
        $result = $this->db->query($sql);//发送给数据库，请求保存
        if($result->result_array() == null)
            return false;
        if(count($result->result_array()) == 1)
            return true;
        return false;
    }
    //修改好友申请者的姓名
    public function setCandidateName($oldUserName,$newUserName)
    {
        $sql = "UPDATE friend_application_list SET candidate_name = '".$newUserName."' WHERE candidate_name = '".$oldUserName."'";//构造数据库请求
        return $this->db->query($sql);//发送给数据库，请求保存
    }
    //修改好友的姓名
    public function setFriendName($oldUserName,$newUserName)
    {
        $sql = "UPDATE friend_list SET friend_name = '".$newUserName."' WHERE friend_name = '".$oldUserName."'";//构造数据库请求
        return $this->db->query($sql);//发送给数据库，请求保存
    }
    //添加candidateEmail 为 email 的好友
    public function addFriend($email,$candidateEmail,$candidateUserName)
    {
        /*
        //获取好友的颜色
        $sql = "SELECT color FROM user_status WHERE email = '".$candidateEmail."'";
        $result = $this->db->query($sql);//发送给数据库，请求保存
        if($result->result_array() == null)
            return false;
        $friend_color = $result->result_array()[0]['color']; 
        */
        //添加好友
        $sql = "INSERT INTO friend_list (email, friend_email,friend_name,friend_color) VALUES ('".$email."', '".$candidateEmail."','".$candidateUserName."','0000FF')";//构造数据库请求
        return $this->db->query($sql);//发送给数据库，请求保存
    }
    //获取email的好友列表
    public function getFriendListByEmail($email)
    {
        $sql = "SELECT * FROM friend_list WHERE email = '".$email."'";
        $result = $this->db->query($sql);//发送给数据库，请求保存
        if($result->result_array() == null)
            return false;
        return $result->result_array();
    }
    //获取userName的所有 好友申请 请求
    public function getFriendApplicationByEmail($email)
    {
    	$sql = "SELECT * FROM friend_application_list WHERE email = '".$email."'";
        $result = $this->db->query($sql);//发送给数据库，请求保存
        if($result->result_array() == null)
            return false;
        return $result->result_array();
    }
    //根据ListID删除一条好友申请
    public function deleteFriendApplicationByListID($ListID)
    {
        $sql = "DELETE FROM friend_application_list WHERE id = '".$ListID."'";//构造数据库请求
        return $this->db->query($sql);//发送给数据库，请求保存
    }
    //根据删除一位好友
    public function deleteFriendByEmail($email,$friendEmail)
    {
        $sql = "DELETE FROM friend_list WHERE email = '".$email."' and friend_email = '".$friendEmail."'";//构造数据库请求
        return $this->db->query($sql);//发送给数据库，请求保存
    }
    //根据ListID获取一条好友申请
    public function getFriendApplicationByListID($ListID)
    {
        $sql = "SELECT * FROM friend_application_list WHERE id = '".$ListID."'";
        $result = $this->db->query($sql);//发送给数据库，请求保存
        if($result->result_array() == null)
            return false;
        return $result->result_array()[0];
    }
    //email是否已经向friendEmail发出了好友申请
    public function isApplicationSend($email,$friendEmail)
    {
        $sql = "SELECT * FROM friend_application_list WHERE email = '".$friendEmail."' and candidate_email = '".$email."'";
        $result = $this->db->query($sql);//发送给数据库，请求保存
        if($result->result_array() == null)
            return false;
        if(count($result->result_array()) >= 1)
            return true;
        return false;
    }
    //userName想添加friendUserName为好友
    public function addFriendApplication($friendEmail,$email,$emailUserName,$emailColor,$time)
    {
        $sql = "INSERT INTO friend_application_list (email,candidate_email,candidate_name,candidate_color,time) VALUES ('".$friendEmail."', '".$email."','".$emailUserName."','".$emailColor."','".$time."')";//构造数据库请求
        return $this->db->query($sql);//发送给数据库，请求保存
    }
}
?>
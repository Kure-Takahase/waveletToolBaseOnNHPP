<?php
class GamePublicChat_model extends CI_Model 
{
    public function __construct()
    {
    	parent::__construct();
        $this->load->database();
    }
    public function isMapID($mapID)
    {
    	$sql = "SELECT * FROM map_list WHERE id = '".$mapID."'";//构造数据库请求
		$result = $this->db->query($sql);//发送给数据库，请求保存
		if($result->result_array() == null)
			return false;
		return true;
    }
    public function getMapStatus($mapID)
    {
    	$sql = "SELECT * FROM map_list WHERE id = '".$mapID."'";//构造数据库请求
		$result = $this->db->query($sql);//发送给数据库，请求保存
		if($result->result_array() == null)
			return false;
		$map_status = $result->result_array()[0];
		$map_status['map_src'] = "https://".$_SERVER['SERVER_NAME'].'/limit/dreamSchool/img/map/'.$map_status['map_src'];
		return $map_status;
    }
    public function getMapFriendList($mapID)
    {
    	$sql = "SELECT * FROM map_friend_list WHERE map_id = '".$mapID."'";//构造数据库请求
		$result = $this->db->query($sql);//发送给数据库，请求保存
		if($result->result_array() == null)
			return false;
		return $result->result_array();
    }
    public function getChatHistoryAtSum($mapID)
    {
    	$sql = "SELECT * from (SELECT * from map_chat_history WHERE map_id = '".$mapID."') as newTable ORDER BY time desc LIMIT 20";
    	//$sql = "SELECT * FROM map_chat_history WHERE map_id = '".$mapID."' limit 100";//构造数据库请求
		$result = $this->db->query($sql);//发送给数据库，请求保存
		if($result->result_array() == null)
			return false;
		return $result->result_array();
    }
    public function saveChatMessage($array_message)
    {
    	$sql = "INSERT INTO map_chat_history (message_from, message_to,content,kind,src,time,map_id,color_one,color_two) VALUES ('".$array_message['message_from']."', '".$array_message['message_to']."','".$array_message['content']."','".$array_message['kind']."','".$array_message['src']."','".$array_message['time']."','".$array_message['map_id']."','".$array_message['color_one']."','".$array_message['color_two']."')";//构造数据库请求
        return $this->db->query($sql);//发送给数据库，请求保存
    }
    
}
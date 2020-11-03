<?php
class UserStatus_model extends CI_Model 
{
    
    public function __construct()
    {
    	parent::__construct();
        $this->load->database();
    }
    public function createUserStatus($userStatus)
    {
    	$originalAction	= $userStatus['originalAction'];
		$originalMaxHP	= $userStatus['originalMaxHP'];
		$originalDefense= $userStatus['originalDefense'];
		$originalAttack	= $userStatus['originalAttack'];
		$originalDodge	= $userStatus['originalDodge'];
		$originalHit	= $userStatus['originalHit'] ;
		$color 			= $userStatus['color'];
		$email 			= $userStatus['email'];
    	$sql = "INSERT INTO user_status (email,color,nowHP,nowAction,originalMaxHP,originalAction,originalDefense,originalAttack,originalDodge,originalHit) VALUES ('".$email."', '".$color."','".$originalMaxHP."','".$originalAction."','".$originalMaxHP."','".$originalAction."','".$originalDefense."','".$originalAttack."','".$originalDodge."','".$originalHit."')";//构造数据库请求
		return $this->db->query($sql);//发送给数据库，请求保存
    }
    public function useItem($email,$itemID)
    {
		//获取自己背包内itemID的信息
		$result = $this->getUserOwnGoodsByEmailAndItemID($email,$itemID);
		if($result == false || $result['kind'] != 'common')
			return false;
		//更新sum
		$newSum = $result['sum'] - 1;
		if($newSum > 0)//还有库存，故sum减1即可
			$sql = "UPDATE user_own_item SET sum = ".$newSum." WHERE email = '".$email."' and item_id = '".$itemID."'";
		if($newSum == 0) //从背包删除物品（但本次可以继续
			$sql = "DELETE FROM user_own_item WHERE email = '".$email."' and item_id = '".$itemID."'";
		if($newSum < 0)
		{
			$sql = "DELETE FROM user_own_item WHERE email = '".$email."' and item_id = '".$itemID."'";
			$this->db->query($sql);
			return false;
		}
		$this->db->query($sql);
		//更新userStatus
		$userStatus = $this->getUserStatusByEmail($email);
		if($userStatus == false)
			return false;
		$userStatus['nowHP'] 	+= $result['addHP'];
		$userStatus['nowAction']+= $result['addAction'];
		if($userStatus['nowHP'] > $userStatus['originalMaxHP'] + $userStatus['accouterMaxHP'])
			$userStatus['nowHP'] = $userStatus['originalMaxHP'] + $userStatus['accouterMaxHP'];
		if($userStatus['nowAction'] > $userStatus['originalAction'] + $userStatus['accouterAction'])
			$userStatus['nowAction'] = $userStatus['originalAction'] + $userStatus['accouterAction'];
		$result = $this->setUserStatusByEmail($email,$userStatus);
		if($result == false)
			return false;
		return true;
    }
    public function ifHaveItem($email,$itemID)
    {
    	$sql = "SELECT * FROM user_own_item WHERE email = '".$email."' and item_id = '".$itemID."'";
		$result = $this->db->query($sql);//发送给数据库，请求保存
		if($result->result_array() == null)
			return false;
		if(count($result->result_array()) == 0)
			return false;
		return true;
    }
    public function setEquipment($email,$itemID)
    {
    	$sql = "SELECT * FROM item_list WHERE id = '".$itemID."'";
		$result = $this->db->query($sql);//发送给数据库，请求保存
		if($result->result_array() == null)
			return false;
		$result = $result->result_array()[0];
		$equipmentType = $result['kind'];
		switch ($equipmentType) 
		{
			case 'head':
			$sql = "UPDATE user_status SET equip_head_id = '".$result['id']."',equip_head_name = '".$result['equipmentName']."',equip_head_src = '".$result['src']."',equip_head_color = '".$result['color']."'  WHERE email = '".$email."'";
				break;
			case 'body':
			$sql = "UPDATE user_status SET equip_body_id = '".$result['id']."',equip_body_name = '".$result['equipmentName']."',equip_body_src = '".$result['src']."',equip_body_color = '".$result['color']."'  WHERE email = '".$email."'";
				break;
			case 'foot':
			$sql = "UPDATE user_status SET equip_foot_id = '".$result['id']."',equip_foot_name = '".$result['equipmentName']."',equip_foot_src = '".$result['src']."',equip_foot_color = '".$result['color']."'  WHERE email = '".$email."'";
				break;
			case 'weapon':
			$sql = "UPDATE user_status SET equip_weapon_id = '".$result['id']."',equip_weapon_name = '".$result['equipmentName']."',equip_weapon_src = '".$result['src']."',equip_weapon_color = '".$result['color']."'  WHERE email = '".$email."'";
				break;
			default:
				return false;
		}
		return $this->db->query($sql);//发送给数据库，请求保存
    }
    public function setUserStatusByEmail($email,$userStatus)
    {
        $sql = "UPDATE user_status SET color = '".$userStatus['color']."',nowHP = '".$userStatus['nowHP']."',nowAction = '".$userStatus['nowAction']."',originalMaxHP = '".$userStatus['originalMaxHP']."',accouterMaxHP = '".$userStatus['accouterMaxHP']."',originalAction = '".$userStatus['originalAction']."',accouterAction = '".$userStatus['accouterAction']."',originalAttack = '".$userStatus['originalAttack']."',accouterAttack = '".$userStatus['accouterAttack']."',originalDefense = '".$userStatus['originalDefense']."',accouterDefense = '".$userStatus['accouterDefense']."',originalHit = '".$userStatus['originalHit']."',accouterHit = '".$userStatus['accouterHit']."',originalDodge = '".$userStatus['originalDodge']."',accouterDodge = '".$userStatus['accouterDodge']."',equip_head_id = '".$userStatus['equip_head_id']."',equip_body_id = '".$userStatus['equip_body_id']."',equip_foot_id = '".$userStatus['equip_foot_id']."',equip_weapon_id = '".$userStatus['equip_weapon_id']."',equip_head_name = '".$userStatus['equip_head_name']."',equip_head_src = '".$userStatus['equip_head_src']."',equip_head_color = '".$userStatus['equip_head_color']."',equip_body_name = '".$userStatus['equip_body_name']."',equip_body_src = '".$userStatus['equip_body_src']."',equip_body_color = '".$userStatus['equip_body_color']."',equip_foot_name = '".$userStatus['equip_foot_name']."',equip_foot_src = '".$userStatus['equip_foot_src']."',equip_foot_color = '".$userStatus['equip_foot_color']."',equip_weapon_name = '".$userStatus['equip_weapon_name']."',equip_weapon_src = '".$userStatus['equip_weapon_src']."',equip_weapon_color = '".$userStatus['equip_weapon_color']."' WHERE email = '".$email."'";//构造数据库请求
        return $this->db->query($sql);//发送给数据库，请求保存
    }
    public function unloadEquipment($email,$equipmentType)
    {
    	switch ($equipmentType)
    	{
    		case 'head':
    			$sql = "UPDATE user_status SET equip_head_id = '0' WHERE email = '".$email."'";//构造数据库请求
    			break;
    		case 'body':
    			$sql = "UPDATE user_status SET equip_body_id = '0' WHERE email = '".$email."'";//构造数据库请求
    			break;
    		case 'foot':
    			$sql = "UPDATE user_status SET equip_foot_id = '0' WHERE email = '".$email."'";//构造数据库请求
    			break;
    		case 'weapon':
    			$sql = "UPDATE user_status SET equip_weapon_id = '0' WHERE email = '".$email."'";//构造数据库请求
    			break;
    		default:
    			return false;
    	}
        return $this->db->query($sql);//发送给数据库，请求保存
    }
    public function getColorByEmail($email)
	{
		$sql = "SELECT color FROM user_status WHERE email = '".$email."'";
    	$result = $this->db->query($sql);//发送给数据库，请求保存
		if($result->result_array() == null)
			return false;
		return $result->result_array()[0]['color'];
	}
	public function getUserStatusByEmail($email)
	{
		$sql = "SELECT * FROM user_status WHERE email = '".$email."'";
		$result = $this->db->query($sql);//发送给数据库，请求保存
		if($result->result_array() == null)
			return false;
		return $result->result_array()[0];
	}
	public function getUserOwnGoodsByEmail($email)
	{
		$sql = "SELECT * FROM user_own_item WHERE email = '".$email."'";
		$result = $this->db->query($sql);//发送给数据库，请求保存
		if($result->result_array() == null)
			return false;
		return $result->result_array();
	}
	public function getUserOwnGoodsByEmailAndItemID($email,$itemID)
	{
		$sql = "SELECT * FROM user_own_item WHERE email = '".$email."' and item_id = '".$itemID."'";
		$result = $this->db->query($sql);//发送给数据库，请求保存
		if($result->result_array() == null)
			return false;
		return $result->result_array()[0];
	}
	public function getItemStatusByID($itemID)
	{
		$sql = "SELECT * FROM item_list WHERE id = '".$itemID."'";
		$result = $this->db->query($sql);//发送给数据库，请求保存
		if($result->result_array() == null)
			return false;
		return $result->result_array()[0];
	}
}
?>
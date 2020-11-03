<?php
class Shop_model extends CI_Model
{
    public function __construct()
    {
    	parent::__construct();
        $this->load->database();
    }
    public function getGoods($kindID, $page, $once)
	{
		$start = ($page - 1) * $page;
        $sql = "SELECT * from (SELECT * from goods WHERE kindID = '".$kindID."') as newTable ORDER BY time desc LIMIT ".$start.",".$once;
    	$result = $this->db->query($sql)-> result_array();
    	if($result == null)
    		return false;
        foreach ($result as $key => $value) 
        {
            $result[$key]['goodsPic'] = $value['goodsPic'];
        }
    	return $result;
	}
    public function addOrder($name,$userName,$phone,$address,$order,$money,$IP,$IParea,$time)
    {
        $sql = "INSERT INTO orderlist (name,userName,phone,address,orderContent,totalMoney,IP,IParea,time,status,mailNumber,mailCompany) VALUES ('".$name."','".$userName."','".$phone."','".$address."','".$order."','".$money."','".$IP."','".$IParea."','".$time."','未付款','无','无')";
        if($this->db->query($sql) == false)
            return false;
        $sql = "SELECT id from orderlist WHERE userName = '".$userName."' and time = '".$time."'";
        $result = $this->db->query($sql)->result_array();
        if($result == null)
            return false;
        return $result[0]['id'];
    }
    public function getOrder($userName)
    {
        $sql = "SELECT * from orderlist WHERE userName = '".$userName."'";
        $result = $this->db->query($sql)->result_array();
        if($result == null)
            return false;
        return $result;
    }
    public function setOrderStatus($orderID,$status)
    {
        $sql = "UPDATE orderlist SET status = '".$status."' WHERE id = '".$orderID."'";
        return $this->db->query($sql);
    }
    public function getOrderByID($orderID)
    {
        $sql = "SELECT * from orderlist WHERE id = '".$orderID."'";
        $result = $this->db->query($sql)->result_array();
        if($result == null)
            return false;
        return $result[0];
    }
}
?>
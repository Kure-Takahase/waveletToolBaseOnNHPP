<?php
class Pay_model extends CI_Model 
{
    public function __construct()
    {
    	parent::__construct();
        $this->load->database();
    }
    public function setOrderPayFinishTime($orderId,$nowTime)
    {
        $sql = "UPDATE orderlist SET payFinishTime = '".$nowTime."' WHERE id = '".$orderId."'";
        return $this->db->query($sql);
    }
    public function getHistoryBestPay()
    {
        $sql = "SELECT userName,money FROM orderlist WHERE status = '1' or status = '2' order by money desc limit 5";
        $result = $this->db->query($sql);
        if($result == null)
            return false;
        return $result->result_array();
    }
    public function getOrderByStatus($status)
    {
    	$sql = "SELECT * from orderlist WHERE status = '".$status."'";
        $result = $this->db->query($sql);
        if($result == null)
            return false;
        return $result;
    }
    //closeTime 为关闭时间。单位分钟
    public function addOrder($userName = 'unknow',$closeTime,$money,$IP,$IParea,$createTime)
    {
        $sql = "INSERT INTO orderlist (userName,closeTime,money,IP,IParea,createTime,status) VALUES ('".$userName."','".$closeTime."','".$money."','".$IP."','".$IParea."','".$createTime."','0')";
        if($this->db->query($sql) == false)
            return false;
        $sql = "SELECT id from orderlist WHERE userName = '".$userName."' and createTime = '".$createTime."'";
        $result = $this->db->query($sql)->result_array();
        if($result == null)
            return false;
        return $result[0]['id'];
    }
    public function setOrderStatus($orderID,$status)
    {
        $sql = "UPDATE orderlist SET status = '".$status."' WHERE id = '".$orderID."'";
        return $this->db->query($sql);
    }
}
?>
<?php
class Notice_model extends CI_Model 
{
    public function __construct()
    {
    	parent::__construct();
        $this->load->database();
    }
    public function getNotice()
    {
    	$sql = "SELECT * FROM notice_list";
        $result = $this->db->query($sql);//发送给数据库，请求保存
        if($result->result_array() == null)
            return false;
        return $result->result_array();
    }
}
?>
<?php
class MessageBox_model extends CI_Model 
{
    public function __construct()
    {
    	parent::__construct();
        $this->load->database();
    }
    /**
     * 向tieID的帖子中发布一个新评论
     * @param string $tieID    帖子ID
     * @param string $comment  评论内容
     * @param string $userName 评论人
     * @param string $IP       发布评论时的地址
     * @param string $IParea   地址的物理区域
     * @param string $time     发布时间
     * @return array 		   成功返回true,失败返回false
     */
    public function addComment($tieID, $comment, $userName, $userHead, $IP, $IParea, $time)
    {
    	$sql = "INSERT INTO message_box_comment (tieID, comment, userName, head, IP, IParea, time) VALUES ('".$tieID."', '".$comment."','".$userName."','".$userHead."','".$IP."','".$IParea."','".$time."')";
		$res = $this->db->query($sql);//增加新评论
		if($res == false)
			return false;
        $sql = "UPDATE message_box_tie SET time = '".$time."' WHERE id = '".$tieID."'";
        $res = $this->db->query($sql);
        if($res == false)
            return false;
        return true;
    }
    /**
     * 查询tieID的评论数量
     * @param  [type] $TieID [description]
     * @return string        评论数量
     */
    public function getCommentCount($TieID)
    {
        $sql = "SELECT count(*) from message_box_comment WHERE tieID = '".$TieID."'";
        $result = $this->db->query($sql)->result_array()[0]['count(*)'];
        return $result;
    }
    /**
     * 获取tieID 的第 page 页评论。每页有sum条
     * @param  string $TieID 帖子ID
     * @param  string $page  需要该页回复
     * @param  string $sum   定义每页回复的数量
     * @return array         评论集。查询失败返回false 
     */
    public function getComment($TieID, $page, $once)
    {
    	$start = ($page - 1) * $once ;
        $sql = "SELECT * from (SELECT * from message_box_comment WHERE tieID = '".$TieID."') as newTable ORDER BY time desc LIMIT ".$start.",".$once;
    	$result = $this->db->query($sql)-> result_array();
    	if($result == null)
    		return false;
        /*
        foreach ($result as $key => $value) 
        {
            $result[$key]['head'] = base_url('jpcnBBS/img/head/').$value['head'];
        }
        */
    	return $result;
    }
    public function getPostAndGuaGreaterThanID($ID)
    {
    	$sql = "SELECT * from (SELECT * from message_box_tie WHERE id > '".$ID."') as newTable ORDER BY time desc";
    	$result = $this->db->query($sql)->result_array();
    	foreach ($result as $key => $arr) 
    	{
    		if($arr['ifgua'] == 'yes')
    		{
    			$sql = "SELECT * FROM gua WHERE id = '".$arr['guaID']."'";
    			$res = $this->db->query($sql)->result_array()[0];
    			$result[$key]['gua'] = $res;
    		}
    	}
    	return $result;
    }
    public function getPostAndGuaLessThanID($ID, $sum)
    {
    	$sql = "SELECT * from (SELECT * from message_box_tie WHERE id < '".$ID."') as newTable ORDER BY time desc LIMIT ".$sum."";
    	$result = $this->db->query($sql)->result_array();
    	foreach ($result as $key => $arr)
    	{
    		if($arr['ifgua'] == 'yes')
    		{
    			$sql = "SELECT * FROM gua WHERE id = '".$arr['guaID']."'";
    			$res = $this->db->query($sql)->result_array()[0];
    			$result[$key]['gua'] = $res;
    		}
    	}
    	return $result;
    }

    public function getPostAndGuaGreaterThanTime($time)
    {
        $sql = "SELECT * from (SELECT * from message_box_tie WHERE time > '".$time."') as newTable ORDER BY time desc";
        $result = $this->db->query($sql)->result_array();
        foreach ($result as $key => $arr) 
        {
            if($arr['ifgua'] == 'yes')
            {
                $sql = "SELECT * FROM gua WHERE id = '".$arr['guaID']."'";
                $res = $this->db->query($sql)->result_array()[0];
                $result[$key]['gua'] = $res;
            }
        }
        return $result;
    }
    public function getPostAndGuaLessThanTime($time, $sum ,$email)
    {
        $sql = "SELECT * from (SELECT * from message_box_tie WHERE time < '".$time."') as newTable where hostEmail = '".$email."' or email = '".$email."' ORDER BY time desc LIMIT ".$sum."";
        $result = $this->db->query($sql)->result_array();
        
        return $result;
    }
    /**
     * 向表 gua 中添加一个新的卦。成功返回gua的ID，失败返回false
     * @param  string $year         新卦的阳历年
     * @param  string $month        新卦的阳历月
     * @param  string $day          新卦的阳历日
     * @param  string $age          起卦人的年龄
     * @param  string $sex          起卦人的性别
     * @param  string $what         起卦人的测项
     * @param  string $nowGua       新卦的主卦整卦
     * @param  string $nowBianGua   新卦的变卦整卦
     * @param  string $nowGuaS      新卦的主卦上卦
     * @param  string $nowGuaX      新卦的主卦下卦
     * @param  string $nowGuaSB     新卦的变卦上卦
     * @param  string $nowGuaXB     新卦的变卦下卦
     * @param  string $nowGuaTotal  新卦的主卦爻
     * @param  string $nowGuaTotalB 新卦的变卦爻
     * @param  string $time         起卦时间
     * @param  string $userName     起卦人用户名
     * @param  string $IP           起卦人IP
     * @param  string $IParea       起卦人IP地址
     * @return string               新卦的ID
     */
    public function newGua($year,$month,$day,$ganzhi_year,$ganzhi_month,$ganzhi_day,$age,$sex,$what,$nowGua,$nowBianGua,$nowGuaS,$nowGuaX,$nowGuaSB,$nowGuaXB,$nowGuaTotal,$nowGuaTotalB,$time,$userName,$IP,$IParea)
    {
    	$sql = "INSERT INTO gua (year, month, day, ganzhi_year, ganzhi_month, ganzhi_day, age, sex, what, nowGua, nowBianGua, nowGuaS, nowGuaX, nowGuaSB, nowGuaXB, nowGuaTotal, nowGuaTotalB,time,userName,IP,IParea) VALUES ('".$year."','".$month."','".$day."','".$ganzhi_year."','".$ganzhi_month."','".$ganzhi_day."','".$age."','".$sex."','".$what."','".$nowGua."','".$nowBianGua."','".$nowGuaS."','".$nowGuaX."','".$nowGuaSB."','".$nowGuaXB."','".$nowGuaTotal."','".$nowGuaTotalB."','".$time."','".$userName."','".$IP."','".$IParea."')";
		$res = $this->db->query($sql);//增加新帖子
		if($res == false)
			return false;
		$sql = "SELECT id FROM gua WHERE userName = '".$userName."' AND time = '".$time."'";
		$result = $this->db->query($sql);//获取新帖子的ID
		if($result->result_array() == null)
			return false;
		return $result->result_array()[0]['id'];
    }
    /**
     * 将表tie中id为 $id 的帖子的ifGua 字段设为 $ifGua，同时自动设置guaID
     * @param string $id    帖子ID
     * @param string $ifGua 设定的ifGua的值
     * @param string $guaID 若ifGua 为 非no，则设置此值
     */
    public function setIfGua($id,$ifGua,$guaID = null)
    {
    	if($ifGua == "no")
    	{
    		$sql = "UPDATE message_box_tie SET ifgua = '".$ifGua."' WHERE id = '".$id."'";
    		return $this->db->query($sql);
    	}
    	else
    	{
    		$sql = "UPDATE message_box_tie SET ifgua = '".$ifGua."', guaID = '".$guaID."'  WHERE id = '".$id."'";
    		return $this->db->query($sql);
    	}
    }
    /**
     * 向表tie 插入一条新的帖子。
     * @param  string $title   新帖子的标题
     * @param  string $content 新帖子的内容
     * @param  string $user    发帖人的用户名
     * @param  string $time    发帖时间
     * @return string          成功返回新帖子的id，失败返回false
     */
    public function newPost($title, $content, $user, $userHead, $IP, $IParea, $time,$hostEmail,$email)
    {
    	$sql = "INSERT INTO message_box_tie (title, content,user, head, IP,IParea,time,createTime,hostEmail,email) VALUES ('".$title."', '".$content."','".$user."','".$userHead."','".$IP."','".$IParea."','".$time."','".$time."','".$hostEmail."','".$email."')";
		$res = $this->db->query($sql);//增加新帖子
		if($res == false)
			return false;
		$sql = "SELECT id FROM message_box_tie WHERE title = '".$title."' AND time = '".$time."'";
		$result = $this->db->query($sql);//获取新帖子的ID
		if($result->result_array() == null)
			return false;
		return $result->result_array()[0]['id'];
    }
    public function ifHaveNewComment($TieID, $time)
    {
        $sql = "SELECT count(*) from (SELECT * from message_box_comment WHERE tieID = '".$TieID."') as newTable WHERE time > '".$time."'";
        $result = $this->db->query($sql)->result_array()[0]['count(*)'];
        if($result == "0")
            return false;
        return true;
    }
    public function ifHaveNewTie($time)
    {
        $sql = "SELECT count(*) from message_box_tie WHERE time > '".$time."'";
        $result = $this->db->query($sql)->result_array()[0]['count(*)'];
        if($result == "0")
            return false;
        return true;
    }
    /**
     * 从表tie 中获取前 $sum 条帖子。默认为 10条。若帖子含有卦，则同时输出卦。
     * @param  integer $sum 返回帖子的数量
     * @return array        帖子集
     */
    public function getLatestPostAndGua($sum,$email)
    {
    	$sql = "SELECT * from message_box_tie WHERE hostEmail = '".$email."' or email = '".$email."'  ORDER BY time desc LIMIT ".$sum."";
    	$result = $this->db->query($sql)->result_array();
    	return $result;
    }
    /**
     * 从表tie 中获取前 $sum 条帖子。默认为 10条
     * @param  integer $sum 返回帖子的数量
     * @return array        帖子集
     */
    public function getLatestPost($sum = 10)
    {
    	$sql = "SELECT * from message_box_tie where iftop != '1' ORDER BY time desc LIMIT ".$sum."";
    	$result = $this->db->query($sql);
    	return $result->result_array();
    }
     /**
     * 从表tie 中获取前 $sum 条置顶标记的帖子。默认为 10条
     * @param  integer $sum 返回帖子的数量
     * @return array        帖子集
     */
    public function getLatestPostWhereTop($sum = 10)
    {
        $sql = "SELECT * from message_box_tie where iftop = '1' ORDER BY time desc LIMIT ".$sum."";
        $result = $this->db->query($sql);
        return $result->result_array();
    }
    /**
     * 从表tie 中获取id 为 $id 的帖子的内容
     * @param  string $id 帖子ID
     * @return array      内容数组
     */
    public function getPostByID($id)
    {
    	$sql = "SELECT * from message_box_tie WHERE id = ".$id."";
    	$result = $this->db->query($sql)->result_array();
    	if($result == null)
    		return false;
    	$result[0]['head'] = base_url('/img/head/').$result[0]['head'];
    	if($result[0]['ifgua'] == "yes")
    	{
    		$sql = "SELECT * FROM gua WHERE id = '".$result[0]['guaID']."'";
			$res = $this->db->query($sql)->result_array()[0];
			$result[0]['gua'] = $res;
    	}
    	return $result[0];
    }




}
?>
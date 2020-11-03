<?php
class IP_model extends CI_Model 
{
    public function __construct()
    {
    	parent::__construct();
        $this->load->database();
    }
    /**
     * 返回当前访问者的IP地址
     * @return string 访问者的IP地址
     */
    public function getIP()
    {
    	if(isset($_SERVER['HTTP_X_FORWARDED_FOR']) == true)
    		return explode(',',$_SERVER['HTTP_X_FORWARDED_FOR'])[0];
    	else
    		return $this->input->ip_address();
    }
    /**
     * 根据IP地址返回对应的物理地址。
     * 首先根据本地IP地址库查询。若不存在则向聚合数据查询(每日500条)
     * @param  string $IP 待查询的IP地址
     * @return string     该IP地址对应的物理地址
     */
    public function getIPArea($IP)
	{
		//先从自己的IP库查找对应的物理地址
		$res = $this->getLocalDataBaseIP($IP);
		if($res != null)
			return $res;
		//从ipip免费库查找
		$url='http://freeapi.ipip.net/'.$IP;
		$html = file_get_contents($url);
		if($html != false)
		{
			$arr = json_decode($html,true);
			$result['area'] = $arr[0].$arr[1].$arr[2].$arr[3];
			$result['location'] = $arr[4];
		}
		else
		{
			//从聚合数据免费库查找
			$url = "http://apis.juhe.cn/ip/ip2addr";
			$params = array(
			    "ip" => $IP,//需要查询的IP地址或域名
			    "key" => "fe5e6607f19488781fb40b346c6b17d0",//应用APPKEY(应用详细页查询)
			);
			$paramstring = http_build_query($params);
			$content = $this->juheCurl($url, $paramstring);
			$result = json_decode($content, true);
			if($result != false)
				$result = $result['result'];
		}
		if($result != false)
		{
			// $result['result']['area'] = "地名";
			// $result['result']['location'] = "运营商名";
			$location = $result['location'] == null ? "未知" : $result['location'];
			$IParea = $result['area'] == null ? "未知地区" : $result['area'];
			$sql = "INSERT INTO iplist (IP,IParea,location) VALUES ('".$IP."', '".$IParea."','".$location."')";//构造数据库请求
			$this->db->query($sql);//将数据库内不存在的IP地址保存。以便下次查询时直接调出,避免调用API接口
			return $IParea;
		}
		else
		{
		    return null;
		}
	}
	public function getAreaByIPIP($IP)
	{

	}
	public function getLocalDataBaseIP($IP)
	{
		$sql = "SELECT IParea FROM iplist WHERE IP = '".$IP."'";//构造数据库请求
		$result = $this->db->query($sql);//查找自己IP库中是否存在这个IP地址
		if($result->result_array() == null)
			return null;
		return $result->result_array()[0]['IParea'];
	}
	/**
	 * 请求接口返回内容
	 * @param  string $url [请求的URL地址]
	 * @param  string $params [请求的参数]
	 * @param  int $ipost [是否采用POST形式]
	 * @return  string
	 */
	function juheCurl($url, $params = false, $ispost = 0)
	{
		ob_start();
	    $httpInfo = array();
	    $ch = curl_init();

	    curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);
	    curl_setopt($ch, CURLOPT_USERAGENT, 'JuheData');
	    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 60);
	    curl_setopt($ch, CURLOPT_TIMEOUT, 60);
	    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
	    if ($ispost) {
	        curl_setopt($ch, CURLOPT_POST, true);
	        curl_setopt($ch, CURLOPT_POSTFIELDS, $params);
	        curl_setopt($ch, CURLOPT_URL, $url);
	    } else {
	        if ($params) {
	            curl_setopt($ch, CURLOPT_URL, $url.'?'.$params);
	        } else {
	            curl_setopt($ch, CURLOPT_URL, $url);
	        }
	    }
	    $response = curl_exec($ch);
	    if ($response === FALSE) {
	        //echo "cURL Error: " . curl_error($ch);
	        return false;
	    }
	    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
	    $httpInfo = array_merge($httpInfo, curl_getinfo($ch));
	    curl_close($ch);
	    return $response;
	} 
}
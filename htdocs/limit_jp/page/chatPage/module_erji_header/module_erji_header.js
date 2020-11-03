function module_erji_header() 
{
	this.test = function() 
	{
		console.log("hello,module_erji_header!");
	}
	this.friendUserName;
	this.setFriendName = function (userName)
	{
		friendUserName = userName;
		$('#chat_page_header .layui-row .goto_center .header_userName').html(userName);
	}
	this.getFriendName = function () 
	{
		return friendUserName;
	}
	this.setFriendOnlineStatus = function (onlineStatus)
	{
		if(onlineStatus == true)
		{
			$("#chat_page_master_online").removeClass('user_status_offline');
			$("#chat_page_master_online").addClass('user_status_online');
		}
		else
		{
			$("#chat_page_master_online").removeClass('user_status_online');
			$("#chat_page_master_online").addClass('user_status_offline');
		}
	}
}
function chat_page_header()//chat_page_header别名的构造函数
{
	$('#chat_page_header .layui-row .goto_left .return_span').on('click',function() 
	{
		LimitControl.removePage("chatPage","right");
	})
	$('#chat_page_header .layui-row .goto_center .header_userName').on('click',function() 
	{
		//LimitControl.removeModule("body","right");
		LimitControl.removePage("chatPage","bottom");
	})
}
function destruct_chat_page_header()//chat_page_header别名的析构函数
{

}
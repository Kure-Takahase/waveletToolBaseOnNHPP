function module_friend_list() 
{
	this.reflashFriend = function() 
	{
		$(".frined_list_friend_page").remove();
		loadFriendApp();
		loadFriendList();
	}
	this.removeFriend = function()
	{
		$(".frined_list_friend_page").remove();
	}
	this.onlineCount;
	this.friendCount;
	this.setOnlineCount = function(count) 
	{
		onlineCount = count;
	}
	this.getOnlineCount = function() 
	{
		return onlineCount;
	}
	this.setFriendCount = function(count) 
	{
		friendCount = count;
	}
	this.getFriendCount = function() 
	{
		return friendCount;
	}
	this.showFriendTotalZero = function () 
	{
		$("#friend_h2").html("我的好友&#8194;(0/0)");
	}

}
function friend_list() 
{
	//loadFriendApp();
	$("#add_button").on('click',function()
	{
		LimitControl.loadPage('addFriendPage','none');
	})
	ws_friend_list();
}
function destruct_friend_list() 
{
	
}
function loadFriendList() 
{
	console.log("loadFriendList ok");
	var url = LimitControl.hostName() + 'Friend/getFriendList';
	var data = 
	{
		email:$.cookie('yourEmail')
	}
	function success_loadFriendList(data)
	{
		if(data == "")
			return ;
		//console.log(data);
		data = JSON.parse( data );
		
		if(data['status'] == '200')
		{
			var online_count ;
			online_count = 0;
			for(var i = 0; i < data['data'].length; i++)
			{
				addFriendList(data['data'][i]);
				if(data['data'][i]['isOnline'] == true)
					online_count ++;
			}
			LimitControl.moduleObject("index","friend_list").setOnlineCount(online_count);
			LimitControl.moduleObject("index","friend_list").setFriendCount(data['data'].length);
			$("#friend_h2").html("我的好友&#8194;("+ online_count +"/"+ data['data'].length +")");
		}
	}
	LimitControl.sendAjax(url,data,success_loadFriendList);
}
function ws_friend_list() 
{
	console.log("ws 已监听");
	ws.addEventListener('message',function (evt) 
	{
		var received_msg = evt.data;
        data = JSON.parse(received_msg);
        if(data.type == 'newChatWordMessage')
        {
        	userEmail = data.email_from;
        	//增加未读信息提示
        	$("span[friend_unread_email='"+userEmail+"']").addClass('layui-badge');
        	if($("span[friend_unread_email='"+userEmail+"']").html() == "")
        		unread_message = 1;
        	else
        		unread_message = parseInt( $("span[friend_unread_email='"+userEmail+"']").html() ) + 1;
        	$("span[friend_unread_email='"+userEmail+"']").html(unread_message);
        }
        else if(data.type == 'newFriendApp')
        {
        	$("#friend_list_new_friend_app").show();
        	//更新好友页
			LimitControl.moduleObject("index","friend_list").reflashFriend();
        }
        else if(data.type == 'newFriendList')
        {
        	//更新好友页
			LimitControl.moduleObject("index","friend_list").reflashFriend();
        }
        else if(data.type == 'RElogin')
        {
        	console.log("RElogin 已截获");
        	$.cookie('yourEmail', data.email, { expires: 7 });
        	//更新好友页
			LimitControl.moduleObject("index","friend_list").reflashFriend();
        }
        else if(data.type == 'friendOnlineStatus')
        {
        	if(data.isOnline == '1')
			{
				$("span[friend_email='"+data.friendEmail+"']").removeClass("user_status_offline");
				$("span[friend_email='"+data.friendEmail+"']").addClass("user_status_online");
			}
			if(data.isOnline == '0')
			{
				$("span[friend_email='"+data.friendEmail+"']").removeClass("user_status_online");
				$("span[friend_email='"+data.friendEmail+"']").addClass("user_status_offline");
			}
			//更新好友页
			LimitControl.moduleObject("index","friend_list").reflashFriend();
        }
	})
	
	//
}
function addFriendList(friend) 
{
	//console.log(friend);
	var HTML = "";
	HTML += "<div class='layui-col-xs12 user_list frined_list_friend_page' onclick='gotoChat(event,this);' email='"+friend['friend_email']+"' username='"+friend['friend_name']+"'>";
		HTML += "<img src='"+LimitControl.staticHost()+'img/head/'+friend['friend_user_id']+".jpg' class='user_head_img'>";
		HTML += "<h2 class='user_name_h2 goto_line'>"+friend['friend_name']+"</h2>";
		
		if(friend['unread_message'] != '0')
		{
			HTML += "<span class='layui-badge unread_message_span' friend_unread_email='"+friend['friend_email']+"'>";
			HTML += friend['unread_message'];	
			HTML += "</span>";
		}
		else
		{
			HTML += "<span class='unread_message_span' friend_unread_email='"+friend['friend_email']+"'>";
			HTML += "</span>";
		}
		
		HTML += "<span friend_email='"+friend['friend_email']+"' class='layui-icon user_status_span ";
		if(friend['isOnline'] == true)
			HTML += "user_status_online";
		if(friend['isOnline'] == false)
			HTML += "user_status_offline";
		HTML += "' layim-event='status' lay-type='show'></span>";
	HTML += "</div>";
	$("#friend_row_div").append(HTML);
}
function loadFriendApp() 
{
	var url = LimitControl.hostName() + 'Friend/getFriendApplication';
	var data = 
	{
		email:$.cookie('yourEmail')
	}
	function success_loadFriendApp(data)
	{
		data = JSON.parse( data );
		//console.log(data);
		if(data['status'] == '200')
		{
			for(var i = 0; i < data['data'].length; i++)
			{
				addFriendAppList(data['data'][i]);
			}
		}
	}
	LimitControl.sendAjax(url,data,success_loadFriendApp);
}
function addFriendAppList(friendApp)
{
	var HTML = "";
	HTML += "<div class='layui-col-xs12 message_list frined_list_friend_page'>";
		HTML += "<img src='"+LimitControl.staticHost()+'img/head/'+friendApp['candidate_name']+".jpg' class='message_head_img'>";
		HTML += "<div class='main_message_div'>";
			HTML += "<h4 class='user_name_h4 goto_line'>"+friendApp['candidate_name']+"</h4>";
			HTML += "<h4 class='add_message_front'>申请添加您为好友</h4>";
		HTML += "</div>";
		HTML += "<button class='layui-btn layui-btn-radius layui-btn-primary layui-btn layui-btn-sm friend_button' onclick='refuseFriendApp("+friendApp['id']+")'>拒绝</button>";
		HTML += "<button class='layui-btn layui-btn-radius layui-btn layui-btn-sm friend_button' onclick='agreeFriendApp("+friendApp['id']+")'>同意</button>";
	HTML += "</div>";
	$("#friend_list_row_div").append(HTML);
}
function agreeFriendApp(listID) 
{
	$("#friend_list_new_friend_app").hide();
	var url = LimitControl.hostName() + 'Friend/friendApplicationReply';
	var data = 
	{
		email:$.cookie('yourEmail'),
		listID:listID,
		reply:'agree'
	}
	function success_agreeFriendApp(data)
	{
		data = JSON.parse( data );
		console.log(data);
		if(data['status'] == 'success')
		{
			layer.msg('已同意！', 
			{
        		time: 1000 //1s后自动关闭
      		});
      		//更新好友页
			LimitControl.moduleObject("index","friend_list").reflashFriend();
		}
	}
	function fail_agreeFriendApp(e) 
	{
		console.log(e.responseText);
	}
	LimitControl.sendAjax(url,data,success_agreeFriendApp,fail_agreeFriendApp);
}
function refuseFriendApp(listID) 
{
	$("#friend_list_new_friend_app").hide();
	var url = LimitControl.hostName() + 'Friend/friendApplicationReply';
	var data = 
	{
		email:$.cookie('yourEmail'),
		listID:listID,
		reply:'refuse'
	}
	function success_refuseFriendApp(data)
	{
		data = JSON.parse( data );
		console.log(data);
		if(data['status'] == 'success')
		{
			layer.msg('已拒绝！', 
			{
        		time: 1000 //1s后自动关闭
      		});
      		//更新好友页
			LimitControl.moduleObject("index","friend_list").reflashFriend();
		}
	}
	LimitControl.sendAjax(url,data,success_refuseFriendApp);
}
function gotoChat(event,elm)
{
	var userEmail = elm.getAttribute("email");
	var userName = elm.getAttribute("username");

	LimitControl.loadPage("chatPage");
	LimitControl.moduleObject("chatPage","chat_page").setFriendEmail(userEmail);
	LimitControl.moduleObject("chatPage","chat_page_header").setFriendName(userName);
	if($("span[friend_email='"+userEmail+"']").hasClass("user_status_online") == true)
		LimitControl.moduleObject("chatPage","chat_page_header").setFriendOnlineStatus(true);
	else
		LimitControl.moduleObject("chatPage","chat_page_header").setFriendOnlineStatus(false);
	LimitControl.moduleObject("chatPage","chat_page").startChatWithFriend();
	LimitControl.moduleObject("chatPage","chat_page").loadChatHistory();
	//取消留言未读提示
	$("span[friend_unread_email='"+userEmail+"']").removeClass('layui-badge');
	$("span[friend_unread_email='"+userEmail+"']").html("");
}
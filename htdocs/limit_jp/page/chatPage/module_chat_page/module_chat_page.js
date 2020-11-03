function module_chat_page() 
{
	this.friendemail;
	this.setFriendEmail = function (email)
	{
		friendemail = email;
	}
	this.getFriendEmail = function() 
	{
		return friendemail;
	}
	this.loadChatHistory = function ()
	{
		var url = LimitControl.hostName() + 'Friend/getChatHistory';
	    var data = 
	    {
	    	email : $.cookie('yourEmail'),
	    	friendEmail: LimitControl.moduleObject("chatPage","chat_page").getFriendEmail(),
	    }
	    function success_loadChatHistory(data) 
	    {
	    	if(data == "")
	    		return ;
	    	console.log(data);
	    	data = JSON.parse( data );
	    	console.log(data);
	    	if(data['chatHistory'] == null)
	    		return ;
	    	console.log("chatHistory ok");
			for(var i=0;i<data['chatHistory'].length;i++)
			{
				addChatHistory(data['chatHistory'][i]);
			}
			chat_page_goto_bottom();
	    }
	    function fail_loadChatHistory(e) 
	    {
	    	console.log(e.responseText);
	    }
	    LimitControl.sendAjax(url,data,success_loadChatHistory,fail_loadChatHistory);
	}
	this.startChatWithFriend = function ()
	{
		var url = LimitControl.hostName() + 'Friend/startChatWithFriend';
		var data = 
	    {
	    	email : $.cookie('yourEmail'),
	    	friendEmail: LimitControl.moduleObject("chatPage","chat_page").getFriendEmail(),
	    }
	    LimitControl.sendAjax(url,data,function () {},function (e) {console.log(e.responseText)});
	}
}
function chat_page() 
{
	ws_chat_page();
	$("#chat_page_send_vip_question_div").on('click',function() 
	{
		$("#chat_page_vip_question_textarea").val("");
	    $("#chat_page_vip_question_textarea_div").show();
		$("#chat_page_vip_question_shade_div").show();
		$("#chat_page_vip_question_textarea").hide();
		$("#chat_page_vip_question_textarea_div").css("height","35px");
		$("#chat_page_vip_question_textarea_div").animate({"height":"222px"}, 150, function(argument) {
		  $("#chat_page_vip_question_textarea").show();
		  $("#chat_page_vip_question_textarea").focus();
		});
	})
	$("#chat_page_vip_question_shade_div").on('click',function() 
	{
		$("#chat_page_vip_question_textarea").hide();
        $("#chat_page_vip_question_shade_div").hide();
        $("#chat_page_vip_question_textarea_div").animate({"height":"35px"}, 100, function(argument) {
            $("#chat_page_vip_question_textarea_div").hide();
        });
	})
	$("#chat_page_vip_question_cancel").on("click",function() 
    {
        $("#chat_page_vip_question_textarea").hide();
        $("#chat_page_vip_question_shade_div").hide();
        $("#chat_page_vip_question_textarea_div").animate({"height":"35px"}, 100, function(argument) {
            $("#chat_page_vip_question_textarea_div").hide();
        });
    })
}
function destruct_chat_page() 
{
	console.log("已移除监听器!");
	ws.removeEventListener('message',addNewChatWordMessage);
}
function chat_page_goto_bottom() 
{
	//元素的内边距+边框+外边距的高
    var outerHeight = $("#chat_page_public_chat").outerHeight(true);
    var height = $(window).height();
    var move = outerHeight - height;
    console.log(outerHeight);
    console.log(height);
    console.log(move);
    $(".chat_page_public_chat_div").scrollTop(move);
}
function ws_chat_page() 
{
	ws.addEventListener('message',addNewChatWordMessage);
}
function addNewChatWordMessage(evt) 
{
	var received_msg = evt.data;
    data = JSON.parse(received_msg);
    if(data.type == 'newChatWordMessage')
    {
    	addChatHistory(data);
    	chat_page_goto_bottom();
    }
}
function sendChatWordMessage() 
{
	if($('#chat_page_vip_question_textarea').val() == null)
    {
        layer.msg('消息不能为空！', {
            time: 1500, //1s后自动关闭
        });
        return;
    }
    var url = LimitControl.hostName() + 'Friend/sendChatWordMessage';
    var data = 
    {
    	email : $.cookie('yourEmail'),
    	friendEmail: LimitControl.moduleObject("chatPage","chat_page").getFriendEmail(),
    	content : $('#chat_page_vip_question_textarea').val()
    }
    function success_send_chat_word_message(data) 
    {
    	console.log(data);
    }
    function fail_send_chat_word_message(e) 
    {
    	console.log(e.responseText);
    }
    LimitControl.sendAjax(url,data,success_send_chat_word_message,fail_send_chat_word_message);
    $("#chat_page_vip_question_textarea").hide();
    $("#chat_page_vip_question_shade_div").hide();
    $("#chat_page_vip_question_textarea_div").animate({"height":"35px"}, 100, function(argument) {
        $("#chat_page_vip_question_textarea_div").hide();
    });
}
function addChatHistory(chatMessage) 
{
	var friendEmail = LimitControl.moduleObject("chatPage","chat_page").getFriendEmail();
	var myName = $.cookie('yourUserName');
	var friendName = LimitControl.moduleObject("chatPage","chat_page_header").getFriendName();
	var HTML = "";
	HTML += "<div class='layui-col-xs12 chat_page_chat_message'>";
		HTML += "<div class='chat_page_chat_message_div'>";
			if(chatMessage['email_from'] == friendEmail)
			{
				HTML += "<h4 class='chat_page_chat_name_h4 goto_line chat_page_he_chatmessage'>";
				HTML += friendName;
				HTML += "</h4>";
				HTML += "<h4 class='chat_page_time_h4 chat_page_he_chatmessage'>"+chatMessage['time']+"</h4>";
			}
			else
			{
				HTML += "<h4 class='chat_page_chat_name_h4 goto_line chat_page_my_chatmessage'>";
				HTML += myName;
				HTML += "</h4>";
				HTML += "<h4 class='chat_page_time_h4 chat_page_my_chatmessage'>"+chatMessage['time']+"</h4>";
			}
			HTML += "<h4 class='chat_page_chat_message_h4'>"+LimitControl.moduleObject("index","index_header").CNtoJP(chatMessage['content'])+"</h4>";
		HTML += "</div>";
	HTML += "</div>";
	$("#chat_page_public_chat").append(HTML);
}
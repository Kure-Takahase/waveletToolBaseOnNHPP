function module_message_box_list() 
{
	this.is_loading_message = false;
}
function message_box_list() 
{
	loadMessageBox();
}
function destruct_message_box_list() 
{
	
}

function loadMessageBox() 
{
	var url = LimitControl.hostName()+"MessageBox/getMessage";
	var data = 
	{
		sum:10,
		email:$.cookie('yourEmail')
	}
	function success_loadMessage(data) 
	{
		data = JSON.parse( data );
		console.log(data);
		if(data['status'] == '200')
		{
			oldest_news_time = data['data'][ data['data'].length - 1 ]['createTime'];
			for (var i = 0; i < data['data'].length ; i++) 
			{
				addMessageList( data['data'][i] );
			}
		}
		autoLoadMessageBox();
	}
	function fail_loadMessage(e) 
	{
		console.log(e.responseText);
	}
	LimitControl.sendAjax(url,data,success_loadMessage,fail_loadMessage);
}
function autoLoadMessageBox() 
{
	$("#message_box_list .message_box_list_div").scroll(function () 
	{
		if(LimitControl.moduleObject("hostPage","message_box_list").is_loading_message == true)
        		return;
        var page = $("#message_box_list .message_box_list_div");
        //bot是底部距离的高度
        var bot = 300;
        //可视区域的高度
        var page_height = page.height();
        //已经拉上去的高度
        var page_scrollTop = page.scrollTop();
        //整个元素的高度
        var page_scrollHeight = page[0].scrollHeight;
        if ((page_height + page_scrollTop ) >= ( page_scrollHeight - bot ) ) 
        {
            LimitControl.moduleObject("hostPage","message_box_list").is_loading_message = true;
            function loadNews(data)
            {
            	data = JSON.parse( data );
            	if(data['status'] == '200')
            	{
            		for(var i= 0 ; i < data['data'].length ; i++)
					{
						addMessageList( data['data'][i] );
					}
					LimitControl.moduleObject("hostPage","message_box_list").is_loading_message = false;
					oldest_news_time = data['data'][ data['data'].length - 1 ]['time'];
            	}
            	if(data['status'] == '201')
            	{
					layer.msg('已经到底啦！', {
			        	time: 1000, //1.5s后自动关闭
			      	});
            	}
            }
            function fail_loadNews(e) 
            {
            	console.log(e.responseText);
            }
            url  = LimitControl.hostName()+"MessageBox/getTieLessThanTime";
            data = 
            {
				time:oldest_news_time,
				sum:'5',
				email:$.cookie('yourEmail')
			};
            LimitControl.sendAjax(url,data,loadNews,fail_loadNews);
        }
    });
}
function showMailContent(id) 
{
	LimitControl.loadPage('mailContent');
	LimitControl.moduleObject('mailContent','mail_content').loadContent(id);
}
function addMessageList(message) 
{
	var HTML = "";
	HTML += "<div class='layui-row message_box_list_row_div' onclick='showMailContent("+message['id']+")'>";
		HTML += "<div class='layui-col-xs2 message_box_list_img_div'>";
			HTML += "<img class='message_box_list_head_img' src='"+LimitControl.staticHost()+'img/head/'+message['head']+"'>";
		HTML += "</div>";
		HTML += "<div class='layui-col-xs10'>";
			HTML += "<h2 class='message_box_list_name'>"+ message['user'] +"</h2>";
			HTML += "<p class='message_box_list_time'>"+ message['createTime'].substring(5,10) +"</p>";
			HTML += "<p class='message_box_list_title'>"+ LimitControl.moduleObject("index","index_header").CNtoJP(message['title']) +"</p>";
			HTML += "<p class='message_box_list_content'>"+ LimitControl.moduleObject("index","index_header").CNtoJP(message['content'])+"</p>";
		HTML += "</div>";
	HTML += "</div>";

	$("#message_box_list .message_box_list_div").append(HTML);
}
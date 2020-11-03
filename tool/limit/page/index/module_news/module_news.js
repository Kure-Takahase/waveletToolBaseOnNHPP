function module_news()
{
	this.is_loading_news = false;
}
function news_page() 
{
	$("#news_page").css("width","100%");
	$("#news_page").css("overflow","auto");
	var height = $(window).height() - 60 - 45;
	$("#news_page").css("height",height);
	loadNews();
}
function destruct_news_page() 
{
	 
}
function loadNews()
{
	//console.log(LimitControl.hostName()+"News/getNews");
	$.ajax
	({
		url: LimitControl.hostName()+"News/getNews",
		type:"post",
		dataType:"json",
		data:
		{
			sum:'10'
		},
		success:function(data)
		{
			for(var i=data['data'].length - 1; i >=0 ; i--)
			{
				addNews("#news_page .notice_main_content",data['data'][i]);
			}
			oldest_news_time = data['data'][ data['data'].length - 1 ]['time'];
			//新闻自动加载
			$("#news_page").scroll(function () 
			{
				if(LimitControl.moduleObject("index","news_page").is_loading_news == true)
		        		return;
		        var page = $("#news_page");
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
		            LimitControl.moduleObject("index","news_page").is_loading_news = true;
		            function loadNews(data)
		            {
		            	data = JSON.parse( data );
		            	if(data['status'] == '200')
		            	{
		            		for(var i= 0 ; i < data['data'].length ; i++)
							{
								addNews("#news_page .notice_main_content",data['data'][i],true);
							}
							LimitControl.moduleObject("index","news_page").is_loading_news = false;
							oldest_news_time = data['data'][ data['data'].length - 1 ]['time'];
		            	}
		            	if(data['status'] == '201')
		            	{
							layer.msg('已经到底啦！', {
					        	time: 1000, //1.5s后自动关闭
					      	});
		            	}
		            }
		            url  = LimitControl.hostName()+"News/getTieLessThanTime";
		            data = 
		            {
						time:oldest_news_time,
						sum:'5'
					};
		            LimitControl.sendAjax(url,data,loadNews);
		        }
		    });
		},
		error:function(e)
		{
			console.log(e.responseText);
			layer.msg('失败！服务器错误！', {
	        	time: 1500, //1.5s后自动关闭
	      	});
		}
	});
}
function showNewsEr(newsID) 
{
	LimitControl.loadPage("news_erji");
	LimitControl.moduleObject("news_erji",'news_page_erji').loadNews(newsID);
	LimitControl.moduleObject("news_erji",'news_page_erji').loadComment(newsID);
}
function addNews(parentElementID,newsData,isTail)
{
	isTail = isTail || false;
	var newsHTML = "";
	
	newsHTML += "<div class='layui-col-md12 remander_col' onclick='showNewsEr("+newsData.id+");'>";
		newsHTML += "<div class='title remander_title'>";
			newsHTML += "<!--     可选      -->";
			if(newsData.ifnew == '1')
				newsHTML += "<span class='layui-badge img_new'>NEW</span>";
			if(newsData.iftop == '1')
				newsHTML += "<span class='layui-badge layui-bg-orange img_new'>置顶</span>";
			newsHTML += "<span class='remander_title'>"+ newsData.title +"</span>";
		newsHTML += "</div>";
		newsHTML += "<hr>";
		newsHTML += "<p class='the_content'>"+ newsData.content +"</p>";
		newsHTML += "<hr>";
		newsHTML += "<span class='span_icon'>";
			newsHTML += "<img class='img_icon' src='$staticImgURL/time2.png'>";
		newsHTML += "</span>";
		newsHTML += "<span class='up_time'>"+ newsData.time +"</span>";
    newsHTML += "</div>";

	newsHTML = LimitControl.staticImgURLtoReal(newsHTML);
	if(isTail == false)
		$(parentElementID).prepend(newsHTML);
	else
		$(parentElementID).append(newsHTML);
}
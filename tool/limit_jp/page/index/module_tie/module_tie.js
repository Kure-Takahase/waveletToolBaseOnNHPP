function module_tie()
{
	this.is_loading_Tie = false;
	this.reLoadTie = function () 
	{
		loadTie();
	}
}
function tie_page() 
{
	$("#tie_page").css("width","100%");
	$("#tie_page").css("overflow","auto");
	var height = $(window).height() - 60 - 45;
	$("#tie_page").css("height",height);
	loadTie();
}
function destruct_tie_page() 
{
	 
}
function loadTie()
{
	//console.log(LimitControl.hostName()+"Tie/getTie");
	$.ajax
	({
		url: LimitControl.hostName()+"Tie/getTie",
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
				addTie("#tie_page .notice_main_content",data['data'][i]);
			}
			oldest_Tie_time = data['data'][ data['data'].length - 1 ]['time'];
			//新闻自动加载
			$("#tie_page").scroll(function () 
			{
				if(LimitControl.moduleObject("index","tie_page").is_loading_Tie == true)
		        		return;
		        var page = $("#tie_page");
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
		            LimitControl.moduleObject("index","tie_page").is_loading_Tie = true;
		            function loadTie(data)
		            {
		            	data = JSON.parse( data );
		            	if(data['status'] == '200')
		            	{
		            		for(var i= 0 ; i < data['data'].length ; i++)
							{
								addTie("#tie_page .notice_main_content",data['data'][i],true);
							}
							LimitControl.moduleObject("index","tie_page").is_loading_Tie = false;
							oldest_Tie_time = data['data'][ data['data'].length - 1 ]['time'];
		            	}
		            	if(data['status'] == '201')
		            	{
							layer.msg('已经到底啦！', {
					        	time: 1000, //1.5s后自动关闭
					      	});
		            	}
		            }
		            url  = LimitControl.hostName()+"Tie/getTieLessThanTime";
		            data = 
		            {
						time:oldest_Tie_time,
						sum:'5'
					};
		            LimitControl.sendAjax(url,data,loadTie);
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
function showTieEr(TieID) 
{
	LimitControl.loadPage("tie_erji");
	LimitControl.moduleObject("tie_erji",'tie_page_erji').loadtie(TieID);
	LimitControl.moduleObject("tie_erji",'tie_page_erji').loadComment(TieID);
}
function addTie(parentElementID,TieData,isTail)
{
	isTail = isTail || false;
	var TieHTML = "";
	
	TieHTML += "<div class='layui-col-md12 remander_col' onclick='showTieEr("+TieData.id+");'>";
		TieHTML += "<div class='title remander_title'>";
			TieHTML += "<!--     可选      -->";
			if(TieData.ifnew == '1')
				TieHTML += "<span class='layui-badge img_new'>NEW</span>";
			if(TieData.iftop == '1')
				TieHTML += "<span class='layui-badge layui-bg-orange img_new'>置顶</span>";
			TieHTML += "<span class='remander_title'>"+ LimitControl.moduleObject("index","index_header").CNtoJP(TieData.title) +"</span>";
		TieHTML += "</div>";
		TieHTML += "<hr>";
		TieHTML += "<p class='the_content'>"+ LimitControl.moduleObject("index","index_header").CNtoJP(TieData.content) +"</p>";
		TieHTML += "<hr>";
		TieHTML += "<span class='span_icon'>";
			TieHTML += "<img class='img_icon' src='$staticImgURL/time2.png'>";
		TieHTML += "</span>";
		TieHTML += "<span class='up_time'>"+ TieData.time +"</span>";
    TieHTML += "</div>";

	TieHTML = LimitControl.staticImgURLtoReal(TieHTML);
	if(isTail == false)
		$(parentElementID).prepend(TieHTML);
	else
		$(parentElementID).append(TieHTML);
}
function module_tie_erji()
{
	this.is_loading_comment = false;
	this.nowPage = 1;
	this.tieID = 1;
	this.totalCommentSum = 0;
	this.nowCommentSum = 0;
	this.loadtie = function(tieID)
	{
		LimitControl.moduleObject("tie_erji","tie_page_erji").tieID = tieID;
		var url = LimitControl.hostName()+'tie/getTieByID';
		var data = 
		{
			ID:tieID
		};
		function loadContent(data)
		{
			data = JSON.parse( data );
			if(data['status'] == '200')
			{
				$("#erji_title").html(LimitControl.moduleObject("index","index_header").CNtoJP(data['data']['title']));
				$("#erji_content_p").html(LimitControl.moduleObject("index","index_header").CNtoJP(data['data']['content']));
				$("#erji_user_time").html(data['data']['createTime']);
				$("#erji_user_name").html(data['data']['user']);
				//var src = LimitControl.staticHost() + 'img/head/' +data['data']['head'];
				var src = data['data']['head'];
				$('#erji_user_head').attr("src", src);
			}
			console.log(data['status']);
			if(data['status'] == '201')
			{
				console.log("201");
				$("#comment_loading_img").hide();
				$("#comment_noComment_img").show();
			}
		}
		LimitControl.sendAjax(url,data,loadContent);
	};
	this.loadComment = function(tieID) 
	{
		LimitControl.moduleObject("tie_erji","tie_page_erji").tieID = tieID;
		LimitControl.moduleObject("tie_erji","tie_page_erji").nowPage = 1;
		LimitControl.moduleObject("tie_erji","tie_page_erji").is_loading_comment = false;
		var url = LimitControl.hostName()+'tie/getComment';
		var data = 
		{
			tieID:tieID,
			page:1,
			ifNeedCount:'yes'
		};
		function loadTheComment(data)
		{
			data = JSON.parse( data );
			console.log(data);
			if(data['status'] == '200')
			{
				if(data['tieID'] != LimitControl.moduleObject("tie_erji","tie_page_erji").tieID)
				{
					return ;
				}
				$("#comment_noComment_img").hide();
				LimitControl.moduleObject("tie_erji","tie_page_erji").totalCommentSum = data['count'];
				LimitControl.moduleObject("tie_erji","tie_page_erji").nowCommentSum = data['comment'].length;
				console.log("nowCommentSum ok");
				$("#comment_sum_p").html(data['count']);
				$("#comment_loading_img").hide();
				if(data['count'] == 0)
					$("#comment_noComment_img").show();
				$('.comment_div').remove();
				for (var i = 0; i < data['comment'].length; i++) 
				{
					addErJiComment(data['comment'][i]);
				}
				//加入自动加载
				autoLoadComment();
			}
			if(data['status'] == '201')
			{
				console.log("201");
				$("#comment_loading_img").hide();
				$("#comment_noComment_img").show();
			}
		}
		LimitControl.sendAjax(url,data,loadTheComment);
	}
}
function tie_page_erji() 
{
	LimitControl.moduleObject("tie_erji","tie_page_erji").is_loading_comment = false;
	LimitControl.moduleObject("tie_erji","tie_page_erji").nowPage = 1;
}
function destruct_tie_page_erji() 
{
	//LimitControl.removeModule("tie_page_erji");
}
function sendErjiComment() 
{
	$("#tie_page_erji").css("overflow","auto");
	if($('#comment_textarea').val() == "")
		return;
	var url = LimitControl.hostName()+'tie/addComment';
	var data = 
	{
		email:$.cookie('yourEmail'),
        password:$.cookie('yourPassword'),
        userName:$.cookie('yourUserName'),
        comment:$('#comment_textarea').val(),
        tieID:LimitControl.moduleObject("tie_erji","tie_page_erji").tieID
	};
	function successSendComment(data)
	{
		hideCommentShade();
		$("#tie_page_erji").scrollTop(0);
		data = JSON.parse( data );
		//console.log(data);
		if(data['status'] == '200')
		{
			layer.msg('评论成功!', 
			{
        		time: 1000, //1s后自动关闭
      		});
			var tieID = LimitControl.moduleObject("tie_erji","tie_page_erji").tieID;
			//重新载入评论
			LimitControl.moduleObject("tie_erji","tie_page_erji").loadComment(tieID);
		}
	}
	function failSendComment(data) 
	{
		layer.msg('评论失败!', 
		{
    		time: 1000, //1s后自动关闭
  		});
	}
	LimitControl.sendAjax(url,data,successSendComment,failSendComment);
}
function autoLoadComment(tieID) 
{
	//console.log("autoLoadComment OK");
	$("#erji_main").scroll(function () 
	{
		//console.log("scroll OK");
		if(LimitControl.moduleObject("tie_erji","tie_page_erji").is_loading_comment == true)
        		return;
        var page = $("#erji_main");
        //bot是底部距离的高度
        var bot = 100;
        //可视区域的高度
        var page_height = page.height();
        //已经拉上去的高度
        var page_scrollTop = page.scrollTop();
        //整个元素的高度
        var page_scrollHeight = page[0].scrollHeight;
        //元素的内边距+边框+外边距的高
        var page_outerHeight = page.outerHeight();
        //console.log(page_height+" "+page_scrollTop+" "+page_scrollHeight);
        if ((page_height + page_scrollTop ) >= ( page_scrollHeight - bot ) )
        {
        	if(LimitControl.moduleObject("tie_erji","tie_page_erji").nowCommentSum >= LimitControl.moduleObject("tie_erji","tie_page_erji").totalCommentSum)
        	{
        		if((page_outerHeight + page_scrollTop ) == ( page_scrollHeight))
        		{
					layer.msg('已经到底了!', 
					{
		        		time: 1000, //1s后自动关闭
		      		});
        		}
        		return ;
        	}
        	//console.log("auto load comment!");
            LimitControl.moduleObject("tie_erji","tie_page_erji").is_loading_comment = true;
            url  = LimitControl.hostName()+"tie/getComment";
            data = 
            {
				tieID:LimitControl.moduleObject("tie_erji","tie_page_erji").tieID,
				page:LimitControl.moduleObject("tie_erji","tie_page_erji").nowPage + 1,
				isNeedCount:'no'
			};
			function loadNewComment(data)
            {
            	data = JSON.parse( data );
            	//console.log(data);
            	if(data['status'] == '200')
				{
					LimitControl.moduleObject("tie_erji","tie_page_erji").nowCommentSum += data['comment'].length;
		        	for (var i = 0; i < data['comment'].length; i++) 
					{
						addErJiComment(data['comment'][i]);
					}
				}
				LimitControl.moduleObject("tie_erji","tie_page_erji").is_loading_comment = false;
				LimitControl.moduleObject("tie_erji","tie_page_erji").nowPage += 1;
            }
            LimitControl.sendAjax(url,data,loadNewComment);
        }
    });
}
function showCommentShade() 
{
	$("#comment_textarea").val("");
	$("#textarea_div").css("z-index","100");
	$("#textarea_div").show();
	$("#textarea_shade_div").show();
	$("#comment_textarea").hide();
	$("#textarea_div").css("height","35px");
	$("#textarea_div").animate({"height":"222px"}, 150, function(argument) {
			$("#comment_textarea").show();
			$("#comment_textarea").focus();
	});
	$("#tie_page_erji").css("overflow","hidden");
}
function hideCommentShade() 
{
	$("#comment_textarea").hide();
	$("#textarea_shade_div").hide();
	$("#textarea_div").animate({"height":"35px"}, 100, function(argument) {
			$("#textarea_div").hide();
	});
	$("#tie_page_erji").css("overflow","auto");
}
function addErJiComment(comment)
{
	console.log("comment ok");
	var tieHTML = "";
	tieHTML += "<div class='layui-col-xs12 comment_div'>";
		tieHTML += "<div class='comment_head_div goto_line'>";
			tieHTML += "<img class='comment_head_img' src='"+comment['head']+"' alt=''>";
		tieHTML += "</div>";
		tieHTML += "<div class='layui-row comment_main_div goto_line'>";
			tieHTML += "<div class='layui-col-xs12'>";
				tieHTML += "<div class='comment_name_div'>"+comment['userName'];
				tieHTML += "</div>";
			tieHTML += "</div>";
			tieHTML += "<div class='layui-col-xs12'>";
				tieHTML += "<div class='comment_content_div'>"+LimitControl.moduleObject("index","index_header").CNtoJP(comment['comment']);
				tieHTML += "</div>";
			tieHTML += "</div>";
			tieHTML += "<!--";
			tieHTML += "<div class='layui-col-xs12'>";
				tieHTML += "<div class='comment_comment_div'>";
				//评论的评论暂时不使用
				tieHTML += "</div>";
			tieHTML += "</div>";
			tieHTML += "-->";
			tieHTML += "<div class='layui-col-xs12'>";
				tieHTML += "<div class='comment_other_div'>";
					tieHTML += "<p>"+comment['time']+"</p>";
				tieHTML += "</div>";
			tieHTML += "</div>";
		tieHTML += "</div>";
    tieHTML += "</div>";
    tieHTML = LimitControl.staticImgURLtoReal(tieHTML);
	$("#comment_div_row").append(tieHTML);
	
}
function module_mail_content() 
{
	this.is_loading_comment = false;
	this.nowPage = 1;
	this.tieID = 1;
	this.totalCommentSum = 0;
	this.nowCommentSum = 0;
	this.loadContent = function (newsID) 
	{
		loadMailContent(newsID);
		loadMailComment(newsID);
	}
	this.loadComment = function (newsID) 
	{
		$('.comment_div').remove();
		loadMailComment(newsID);
	}
}
function mail_content() 
{
	layui.use('form', function(){
	  var form = layui.form;
	  //监听提交
	  form.on('submit(mail_content)', function(data)
	  {
	  	if(data.field['desc'] == "")
	  	{
	  		layer.msg('回复不能为空!', 
			{
        		time: 1000, //1s后自动关闭
      		});
	  		return false;
	  	}
	    sendComment(data.field['desc']);
	    return false;
	  });
	  form.render();
	});
}
function destruct_mail_content() 
{
	
}
function sendComment(comment) 
{
	var url = LimitControl.hostName() + "MessageBox/addComment";
	var data = 
	{
		email:$.cookie('yourEmail'),
        password:$.cookie('yourPassword'),
        userName:$.cookie('yourUserName'),
        comment:comment,
        tieID:LimitControl.moduleObject("mailContent","mail_content").tieID
	}
	function success_sendComment(data) 
	{
		console.log(data);
		layer.msg('回复成功!', 
		{
    		time: 1000, //1s后自动关闭
  		});
  		var tieID = LimitControl.moduleObject("mailContent","mail_content").tieID;
		//重新载入评论
		LimitControl.moduleObject("mailContent","mail_content").loadComment(tieID);
	}
	LimitControl.sendAjax(url,data,success_sendComment);
}
function loadMailContent(newsID) 
{
	var url = LimitControl.hostName() + "MessageBox/getTieByID";
	var data = 
	{
		ID:newsID
	}
	function success_loadMailContent(data)
	{
		data = JSON.parse( data );
		console.log(data);
		if(data['status'] == '200')
		{
			$("#mail_content_title").html(LimitControl.moduleObject("index","index_header").CNtoJP(data['data']['title']));
			$("#mail_content_content_p").html(LimitControl.moduleObject("index","index_header").CNtoJP(data['data']['content']));
			$("#mail_content_user_time").html(data['data']['createTime']);
			$("#mail_content_user_name").html(data['data']['user']);
			//var src = LimitControl.staticHost() + 'img/head/' +data['data']['head'];
			var src = data['data']['head'];
			$('#mail_content_user_head').attr("src", src);
		}
	}
	function fail_loadMailContent(e)
	{
		console.log(e.responseText);
	}
	LimitControl.sendAjax(url,data,success_loadMailContent,fail_loadMailContent);
}
function loadMailComment(newsID) 
{
	LimitControl.moduleObject("mailContent","mail_content").tieID = newsID;
	LimitControl.moduleObject("mailContent","mail_content").nowPage = 1;
	LimitControl.moduleObject("mailContent","mail_content").is_loading_comment = false;
	var url = LimitControl.hostName()+'MessageBox/getComment';
	var data = 
	{
		tieID:newsID,
		page:1,
		ifNeedCount:'yes'
	};
	function loadTheComment(data)
	{
		data = JSON.parse( data );
		//console.log(data);
		if(data['status'] == '200')
		{
			if(data['tieID'] != LimitControl.moduleObject("mailContent","mail_content").tieID)
				return ;
			LimitControl.moduleObject("mailContent","mail_content").totalCommentSum = data['count'];
			LimitControl.moduleObject("mailContent","mail_content").nowCommentSum = data['comment'].length;
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
			//autoLoadComment();
		}
	}
	LimitControl.sendAjax(url,data,loadTheComment);
}
function addErJiComment(comment)
{
	//console.log("comment ok");
	var tieHTML = "";
	tieHTML += "<div class='layui-col-xs12 comment_div'>";
		tieHTML += "<div class='comment_head_div goto_line'>";
			tieHTML += "<img class='comment_head_img' src='$staticImgURL/head/"+comment['head']+"' alt=''>";
		tieHTML += "</div>";
		tieHTML += "<div class='layui-row comment_main_div goto_line'>";
			tieHTML += "<div class='layui-col-xs12'>";
				tieHTML += "<div class='comment_name_div'>"+comment['userName'];
				tieHTML += "</div>";
			tieHTML += "</div>";
			tieHTML += "<div class='layui-col-xs12'>";
				tieHTML += "<div class='comment_content_div'>"+ LimitControl.moduleObject("index","index_header").CNtoJP(comment['comment']);
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
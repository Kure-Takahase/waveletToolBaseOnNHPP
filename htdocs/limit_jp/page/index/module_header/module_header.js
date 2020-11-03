function module_header() 
{
	this.test = function() 
	{
		console.log("hello,module_header!");
	}
	this.CNtoJP = function (word) 
	{
		console.log("CNtoJP ok！！！");
		var result_word = "";
		//请求HTML代码块
		$.ajax
		({
		 	url:LimitControl.hostName() + 'Common/CNtoJP',
		 	type:"post",
		 	async: false,
		 	dataType:"json",
			data:{
				word:word
			},
		 	success:function(result)
		 	{
		 		result_word = result['result'];
	  		}
		});
		console.log(result_word);
		return result_word;
	}
}
//构造函数
function index_header()
{
	console.log("CNtoJP ok");
	var result = LimitControl.moduleObject("index","index_header").CNtoJP("你好");
	console.log(result);
	$("#img_write").on('click',function () 
	{
		LimitControl.loadPage("postNewTie",'none');
	})
	$('.liuqiong_shop_login_button').on('click',function() 
	{
		LimitControl.loadPage("login");
		//LimitControl.loadModule("login","login","loginPage","module_login","right");
	})
	$('.liuqiong_shop_register_button').on('click',function() 
	{
		LimitControl.loadPage("register");
		//LimitControl.loadModule("register","register","registerPage","module_register","right");
	})
	$('.loginOut').on('click',function()
	{
		header_loginOut();
		$(".user_login_div").hide();
		$(".login_button_div").show();
		$(".register_button_div").show();
		$(".layui-nav-bar").hide();
		$.cookie('yourUserName', "null");
		$.cookie('yourEmail', "null");
		$.cookie('yourPassword', "null");
		LimitControl.moduleObject("index","friend_list").removeFriend();
		layer.msg('已登出', {
	        time: 1500, //1.5s后自动关闭
	    });
	});
	$(".user_name_div").on('click',function() 
	{
		$("#header_MyPage").removeClass("layui-this");
		$("#header_HostPage").removeClass("layui-this");
	});
	$('#header_MyPage').on('click',function() 
	{
		LimitControl.loadPage("userPage","right");
	});
	$('#header_HostPage').on('click',function() 
	{
		LimitControl.loadPage("hostPage","right");
	});
	loginByCookies();
}
//析构函数
function destruct_index_header() 
{
	
}
function header_loginOut() 
{
	var url = LimitControl.hostName() + 'User/loginOut';
	var data = 
	{
		email : $.cookie('yourEmail'),
		client_id : $.cookie('client_id')
	}
	LimitControl.sendAjax(url,data);
}
//检查cookies信息，并尝试登录
function loginByCookies() 
{
	//console.log($.cookie('yourEmail')+" "+$.cookie('yourPassword'));
	if($.cookie('yourEmail') != "null" &&$.cookie('yourEmail') != undefined)
	{
		ws.addEventListener('message',function (evt) 
		{
			var received_msg = evt.data;
	        data = JSON.parse(received_msg);
	        if(data.type == 'init')
	        {
	        	$.cookie('client_id', data.client_id);
	        	var url = LimitControl.hostName() + 'User/loginOut';
				var data = 
				{
					email : $.cookie('yourEmail'),
					client_id : $.cookie('client_id')
				}
				function success_logout() 
				{
					cookies_login($.cookie('yourEmail'), $.cookie('yourPassword'), cookiesLoginSuccess, cookiesLoginFail, "no");
				}
				LimitControl.sendAjax(url,data,success_logout);
	        }
		})
	}
	else
	{
		cookiesLoginFail()
	}
}
//通过cookies登录成功时的回调函数
function cookiesLoginSuccess(data)
{
	cookiesLoginSuccessScreen(data['userName']);
	
}
//通过cookies登录失败时的回调函数
function cookiesLoginFail()
{
	
}
//主页界面变更为已登录
function cookiesLoginSuccessScreen(userName)
{
	$(".user_name_p").html(userName);
	$(".user_login_div").show();
	$(".user_login_div").css("display","inline-block");
	$(".login_button_div").hide();
	$(".register_button_div").hide();
}
//登录ajax请求
function cookies_login(email, password, callback_success, callback_fail, ifMsg = "yes") 
{

	//console.log(LimitControl.hostName()+"User/login");
	$.ajax
	({
		url: LimitControl.hostName()+"User/login",
		type:"post",
		dataType:"text",
		data:
		{
			client_id:$.cookie('client_id'),
			email:email,
			password:password,
		},
		success:
		function(data)
		{
			//console.log("cookies_login:");
			//console.log(data);
			if(data == [])
				return ;
			console.log
		    data = JSON.parse( data );
		    console.log(data);
			if(data['status'] == '200')
			{

				if(ifMsg == "yes")
				{
					layer.msg('登录成功！', 
					{
		        		time: 1000, //1s后自动关闭
		      		});
				}
		      	$.cookie('yourUserName', data['userName'], { expires: 7 });
		      	$.cookie('yourUserHead', data['userHead'], { expires: 7 });
		      	//执行回调
		      	callback_success(data);
			}
			if(data['status'] == '500')
			{
				callback_fail();
				if(ifMsg == "yes")
				{
					layer.msg('邮箱/密码不正确！', 
					{
		        		time: 1500, //1.5s后自动关闭
		      		});
				}
			}
			if(data['status'] == '600')
			{
				callback_fail();
				if(ifMsg == "yes")
				{
					layer.msg('数据库错误！', 
					{
		        		time: 1500, //1.5s后自动关闭
		      		});
				}
			}
		},
		error:function(e)
		{
			callback_fail();
			if(ifMsg == "yes")
			{
				layer.msg('失败！服务器出现未知的错误！', 
				{
	        		time: 1500, //1.5s后自动关闭
	      		});
			}
		}
	});
}
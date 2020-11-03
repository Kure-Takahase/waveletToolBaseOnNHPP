layui.use('form', function()
{
	var form = layui.form;
});
function module_login()
{
	this.test = function() 
	{
		console.log("hello,module_login!");
	}
}
//构造函数
function loginPage()
{
	//加载二级标题栏
	//LimitControl.loadModule("loginPage","login_header","module_erji_header","none","head");
	//登录
	layui.use('form', function()
	{
		var form = layui.form;
		form.on('submit(LAY-user-login-submit)', function(data)
		{
			if($("#loginPage .LAY-user-login-password_login").val() == "" || $("#loginPage .LAY-user-login-password_login").val() == undefined)
			{
				layer.msg('请输入密码!', 
				{
	        		time: 1000, //1s后自动关闭
	      		});
				return false;
			}
			$("#loginPage .LAY-user-login-password_login").val("");
			//记录下来用户输入的用户名和密码。之后每次用户有关的操作都要用这个进行验证
			$.cookie('yourEmail', data.field['email'], { expires: 7 });
			$.cookie('yourPassword', data.field['password'], { expires: 7 });
			jieyou_login(data.field['email'], data.field['password'], loginPageSuccess);
			return false;
		});
	})
}
//析构函数
function destruct_loginPage()
{

}
//通过登录页成功登录时的回调函数
function loginPageSuccess(data)
{
	//关闭登录页
	LimitControl.removePage("login","right");
	//主页界面变更为已登录
	loginSuccessScreen(data['userName']);
}
//主页界面变更为已登录
function loginSuccessScreen(userName)
{
	$(".user_name_p").html(userName);
	$(".user_login_div").show();
	$(".user_login_div").css("display","inline-block");
	$(".login_button_div").hide();
	$(".register_button_div").hide();
	//更新好友页
	//LimitControl.moduleObject("index","friend_list").reflashFriend();
}
//登录ajax请求
function jieyou_login(email, password, callback, ifMsg = "yes") 
{
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
			if(data == "")
				return ;
			data = JSON.parse( data );
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
		      	callback(data);
			}
			if(data['status'] == '500')
			{
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

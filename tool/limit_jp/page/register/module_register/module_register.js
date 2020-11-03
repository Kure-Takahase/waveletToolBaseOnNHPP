layui.use('form', function()
{
	var form = layui.form;
});
function module_register() 
{
	this.test = function() 
	{
		console.log("hello,module_register!");
	}
}
function registerPage() 
{
	//加载二级标题栏
	//LimitControl.loadModule("registerPage","register_header","module_erji_header","none","head");
	//注册
	layui.use('form', function()
	{
		var form = layui.form;
		form.on('submit(LAY-user-reg-submit)', function(data)
		{
			if(data.field['password'] != data.field['repass'])
			{
				layer.msg('密码与确认密码不一致!', {
		        time: 1500, //1s后自动关闭
		      	});
		      	return false;
			}
		  	if(data.field['nickname'].replace(/[\u0391-\uFFE5]/g,"aa").length > 12)
			{
				layer.msg('用户名过长！请不要超过6个汉字', {
		        time: 1500, //1s后自动关闭
		      	});
		      	return false;
			}
			if(data.field['nickname'].replace(/[\u0391-\uFFE5]/g,"aa").length < 2)
			{
				layer.msg('用户名过短！请在1个汉字以上', {
		        time: 1500, //1s后自动关闭
		      	});
		      	return false;
			}
			var regNumber = /\d+/; //验证0-9的任意数字最少出现1次。
			var regString = /[a-zA-Z]+/; //验证大小写26个字母任意字母最少出现1次。
			if(!regNumber.test(data.field['password']) || !regString.test(data.field['password']))
			{
				layer.msg('密码中至少包含数字和英文字母！', {
		        time: 1500, //1s后自动关闭
		      	});
		      	return false;
			}
			$.cookie('yourEmail', data.field['email'], { expires: 7 });
			$.cookie('yourPassword', data.field['password'], { expires: 7 });
			jieyou_register(data.field['email'], data.field['nickname'], data.field['password'], data.field['repass'], data.field['password'].length, registerSuccessScreen);
			return false;
		});
	});
}
function destruct_registerPage() 
{
	//LimitControl.removeModule("registerPage");
}
function registerSuccessScreen(data)
{
	LimitControl.removePage("register","right");
	$(".user_name_p").html(data['userName']);
	$(".user_login_div").show();
	$(".login_button_div").hide();
	$(".register_button_div").hide();
}
function jieyou_register(email,nickname,password,repass,passwordLength,callback_Success,ifMsg = "yes") 
{
	$.ajax
	({
		url: LimitControl.hostName()+"User/register",
		type:"post",
		dataType:"text",
		data:
		{
			client_id:$.cookie('client_id'),
			email:email,
			userName:nickname,
			password:password,
			repass:repass,
			passwordLength:passwordLength
		},
		success:function(data)
		{
			console.log(data);
			data = JSON.parse( data );
			if(data['status'] == '200')
			{
				if(ifMsg == "yes")
				{
					layer.msg('注册成功！', {
		        		time: 1000, //1s后自动关闭
		      		});
				}
		      	$.cookie('yourUserName', data['userName'], { expires: 7 });
				$.cookie('yourUserHead', "unknow.jpg", { expires: 7 });
		      	//切换界面,自动登录
		      	callback_Success(data);
		      	//registerSuccessScreen($.cookie('yourUserName'));
		      	
			}
			if(data['status'] == '500')
			{
				if(ifMsg == "yes")
				{
					layer.msg('该邮箱已被使用！', {
			        	time: 1500, //1.5s后自动关闭
			      	});
				}
			}
			if(data['status'] == '501')
			{
				if(ifMsg == "yes")
				{
					layer.msg('该用户名已被使用！', {
			        	time: 1500, //1.5s后自动关闭
			      	});
				}
			}
			if(data['status'] == '502')
			{
				if(ifMsg == "yes")
				{
					layer.msg('两次密码不一致！', {
			        	time: 1500, //1.5s后自动关闭
			      	});
				}
			}
			if(data['status'] == '503')
			{
				if(ifMsg == "yes")
				{
					layer.msg('密码长度过短！密码长度需8位以上！', {
			        	time: 1500, //1.5s后自动关闭
			      	});
				}
			}
			if(data['status'] == '504')
			{
				if(ifMsg == "yes")
				{
					layer.msg('密码长度过长！密码长度需16位以下！', {
			        	time: 1500, //1.5s后自动关闭
			      	});
				}
			}
			if(data['status'] == '600')
			{
				if(ifMsg == "yes")
				{
					layer.msg('数据库错误！', {
			        	time: 1500, //1.5s后自动关闭
			      	});
				}
			}
		},
		error:function(e)
		{
			console.log(e);
			if(ifMsg == "yes")
			{
				layer.msg('失败！服务器出现未知的错误！', {
		        	time: 1500, //1.5s后自动关闭
		      	});
			}
		}
	});
}
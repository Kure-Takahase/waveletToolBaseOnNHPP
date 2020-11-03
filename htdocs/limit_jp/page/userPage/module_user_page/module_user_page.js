function module_user_page() 
{
	
}
function my_page() 
{
	//加载用户信息
	loadUserMessage();
	layui.use('form', function(){
	  var form = layui.form;
	  //监听提交
	  form.on('submit(userPage)', function(data){
	    //layer.msg(JSON.stringify(data.field['field));
	    //console.log($("#email_p_user_page").html()+" "+data.field['title']+" "+data.field['desc']+" "+data.field['sex']+" "+data.field['ifPassword']+" "+data.field['password']+" "+data.field['new_password']);
	    if(data.field['ifPassword'] == 1 && data.field['new_password'] != data.field['new_password_repeat'])
	    {
	    	layer.msg('两次密码输入不一致！', {
		        time: 1000, //1s后自动关闭
		    });
	    	return false;
	    }
	    setUserMessage($("#email_p_user_page").html(),data.field['title'],data.field['desc'],data.field['sex'],data.field['ifPassword'],data.field['password'],data.field['new_password']);
	    return false;
	  });
	  form.render();
	});
	$("#changePassword_button").on('click',function() 
	{
		$("#ifPassword_userPage").val(1);
		showChangePassword();
	})
	$("#notChangePassword_button").on('click',function() 
	{
		$("#ifPassword_userPage").val(0);
		hideChangePassword();
	})
	//上传头像
	layui.use('upload', function(){
	  var upload = layui.upload;
	  //执行实例
	  var uploadInst = upload.render({
	    elem: '#upload_head_user_page_button' //绑定元素
	    ,url: LimitControl.hostName()+'User/uploadHead/'+ $.cookie('yourUserName')//上传接口
	    ,auto: false //选择文件后不自动上传
  		,bindAction: '#save_user_page_button' //指向一个按钮触发上传
  		,choose: function(obj){
	      //预读本地文件示例，不支持ie8
	      obj.preview(function(index, file, result){
	      	$("#upload_head_user_page_img").attr("src", result);
	        //$('#demo2').append('<img src="'+ result +'" alt="'+ file.name +'" class="layui-upload-img">')
	      });
	    }
	    ,done: function(res){
	    	//console.log(res);
	    	/*
	    	layer.msg('成功上传头像！', {
		        time: 1500, //1.5s后自动关闭
		    });
		    */
	      //上传完毕回调
	    }
	    ,error: function(e){
	    	layer.msg('上传头像失败！', {
		        time: 1500, //1.5s后自动关闭
		    });
	    	//console.log("upload error");
	      //请求异常回调
	    }
	  });
	});
}
function destruct_my_page() 
{
	
}
function setUserMessage(email,userName,intro,sex,isPassword,old_pass,new_pass)
{
	var url = LimitControl.hostName() + 'User/updateUserMessage';
	var data = 
	{
		email:email,
		userName:userName,
		intro:intro,
		sex:sex,
		isPassword:isPassword,
		old_pass:old_pass,
		new_pass:new_pass
	}
	function success_setUserMessage(data) 
	{
		data = JSON.parse( data );
		//console.log(data);
		//正常
		if(data['status'] == '200')
		{
			layer.msg('修改成功！', {
		        time: 1000, //1.5s后自动关闭
		    });
		}
		//用户名已存在
		if(data['status'] == '501')
		{
			layer.msg('用户名已存在！', {
		        time: 1000, //1.5s后自动关闭
		    });
		}
		//数据库错误
		if(data['status'] == '502')
		{
			layer.msg('数据库错误！', {
		        time: 1000, //1.5s后自动关闭
		    });
		}
		//修改密码认证失败
		if(data['status'] == '503')
		{
			layer.msg('旧密码错误！', {
		        time: 1000, //1.5s后自动关闭
		    });
		}
		//认证失败
		if(data['status'] == '600')
		{
			layer.msg('认证失败！', {
		        time: 1000, //1.5s后自动关闭
		    });
		}
	}
	function fail_setUserMessage(e) 
	{
		//console.log(e.responseText);
	}
	LimitControl.sendAjax(url,data,success_setUserMessage,fail_setUserMessage);
}
function loadUserMessage() 
{
	//console.log($.cookie('yourEmail'));
	var url = LimitControl.hostName() + 'User/getUserMessage';
	var data = 
	{
		email:$.cookie('yourEmail'),
		password:$.cookie('yourPassword')
	}
	function success_getUserMessage(data)
	{
		data = JSON.parse( data );
		//console.log(data);
		$("#upload_head_user_page_img").attr("src", LimitControl.staticHost() + 'img/head/' +data['userMessage']['head']);
		$("#email_p_user_page").html(data['userMessage']['email']);
		$("#userName_input_user_page").val(data['userMessage']['userName']);
		if(data['userMessage']['sex'] == 0)
		{
			$("#sex_radio_user_page_woman").prop("checked",true);
            $("#sex_radio_user_page_man").prop("checked",false);
		}
		if(data['userMessage']['sex'] == 1)
		{
			$("#sex_radio_user_page_man").prop("checked",true);
            $("#sex_radio_user_page_woman").prop("checked",false);
		}
		$("#intro_textarea_user_page").val(data['userMessage']['intro']);
	}
	LimitControl.sendAjax(url,data,success_getUserMessage);
}
function showChangePassword() 
{
	$(".changePassword_div").hide();
	$(".changePassword").show();
	$("#password_input_user_page").val('');
	$("#new_password_input_user_page").val('');
	$("#new_password_repeat_input_user_page").val('');
}
function hideChangePassword()
{
	$("#password_input_user_page").val('1');
	$("#new_password_input_user_page").val('1');
	$("#new_password_repeat_input_user_page").val('1');
	$(".changePassword_div").show();
	$(".changePassword").hide();
}

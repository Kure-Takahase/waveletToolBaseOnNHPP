function module_volunteer_apply() 
{
	this.hostEmail;
	this.setHostEmail = function (email) 
	{
		hostEmail = email;
	}
	this.getHostEmail = function ()
	{
		return hostEmail;
	}
}
function volunteer_apply() 
{
	layui.use('form', function()
	{
		var form = layui.form;
		//监听提交
		form.on('submit(volunteer_apply_page)', function(data)
		{
			//layer.msg(JSON.stringify(data.field));
			post_volunteer_apply(data);
			//helloworld();
			return false;
		});
		form.render();
	});
}
function destruct_volunteer_apply() 
{
	
}
/*
function helloworld() 
{
	layer.msg("helloworld");
	var url = LimitControl.hostName() + 'MessageBox/post';
    var data = 
    {
    	email : $.cookie('yourEmail'),
    	password:$.cookie('yourPassword'),
    	hostEmail : hostEmail,
    	content : data.field['content'],
    	title : data.field['title']
    }
}
*/
function post_volunteer_apply(data) 
{
	///layer.msg("helloworld");
	var url = LimitControl.hostName() + 'MessageBox/post';
	LimitControl.moduleObject("postVolunteerApply","volunteer_apply").getHostEmail()
    var data_arr = 
    {
    	email : $.cookie('yourEmail'),
    	password:$.cookie('yourPassword'),
    	hostEmail : LimitControl.moduleObject("postVolunteerApply","volunteer_apply").getHostEmail(),
    	content : data.field['content'],
    	title : data.field['title']
    }
    //layer.msg("1234567");
    function success_volunteer_apply(data) 
    {
    	/*
    	layer.msg('success_volunteer_apply ok', 
		{
    		time: 1000 //1s后自动关闭
  		});
  		*/
    	if(data == "")
			return ;
		data = JSON.parse( data );
		console.log(data);
		if(data['status'] == '200')
		{
			layer.msg('已发送申请！', 
			{
        		time: 1000 //1s后自动关闭
      		});
			LimitControl.removePage('postVolunteerApply');
		}
		if(data['status'] == 'fail')
		{
			layer.msg(data['message'], 
			{
        		time: 1000 //1s后自动关闭
      		});
		}
    }
    function fail_volunteer_apply(e)
    {
    	layer.msg('失败!', 
		{
    		time: 1000 //1s后自动关闭
  		});
    	console.log(e.responseText);
    }
    //layer.msg("1234567");
   /* layer.msg('sendAjax ok', 
	{
		time: 1000 //1s后自动关闭
		});
    layer.msg(url);*/
    LimitControl.sendAjax(url,data_arr,success_volunteer_apply,fail_volunteer_apply);
}

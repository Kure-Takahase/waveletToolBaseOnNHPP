function module_add_friend() 
{
	
}
function add_friend() 
{
	layui.use('form', function()
	{
	  var form = layui.form;
	  //监听提交
	  form.on('submit(add_friend_page)', function(data){
	    var userEmail = data.field['title'];
	    var url = LimitControl.hostName() + 'Friend/applicationAddFriend';
	    var data = 
	    {
	    	email : $.cookie('yourEmail'),
	    	friendEmail : userEmail
	    }
	    function success_add_friend(data) 
	    {
	    	if(data == "")
				return ;
			data = JSON.parse( data );
			console.log(data);
			if(data['status'] == 'success')
			{
				layer.msg('已发送好友申请！', 
				{
	        		time: 1000 //1s后自动关闭
	      		});
				LimitControl.removePage('addFriendPage');
			}
			if(data['status'] == 'fail')
			{
				layer.msg(data['message'], 
				{
	        		time: 1000 //1s后自动关闭
	      		});
			}
	    }
	    function fail_add_friend(e) 
	    {
	    	console.log(e.responseText);
	    }
	    LimitControl.sendAjax(url,data,success_add_friend,fail_add_friend);
	    return false;
	  });
	  form.render();
	});
}
function destruct_add_friend() 
{
	
}
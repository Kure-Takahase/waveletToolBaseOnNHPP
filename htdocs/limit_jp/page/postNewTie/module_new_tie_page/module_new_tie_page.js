function module_new_tie_page() 
{
	
}
function new_tie_apply() 
{
	layui.use('form', function()
	{
		var form = layui.form;
		//监听提交
		form.on('submit(new_tie_page)', function(data)
		{
			//layer.msg(JSON.stringify(data.field));
			post_new_tie_apply(data);
			//helloworld();
			return false;
		});
		form.render();
	});
}
function destruct_new_tie_apply() 
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
function post_new_tie_apply(data) 
{
	///layer.msg("helloworld");
	var url = LimitControl.hostName() + 'Tie/post';
    var data_arr = 
    {
    	email : $.cookie('yourEmail'),
    	password:$.cookie('yourPassword'),
    	content : data.field['content'],
    	title : data.field['title']
    }
    //layer.msg("1234567");
    function success_new_tie_apply(data) 
    {
    	/*
    	layer.msg('success_new_tie_apply ok', 
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
			layer.msg('已发布新帖子！', 
			{
        		time: 1000 //1s后自动关闭
      		});
			LimitControl.removePage('postNewTie');
			LimitControl.moduleObject("index","tie_page").reLoadTie();
		}
		if(data['status'] == 'fail')
		{
			layer.msg(data['message'], 
			{
        		time: 1000 //1s后自动关闭
      		});
		}
    }
    function fail_new_tie_apply(e)
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
    LimitControl.sendAjax(url,data_arr,success_new_tie_apply,fail_new_tie_apply);
}

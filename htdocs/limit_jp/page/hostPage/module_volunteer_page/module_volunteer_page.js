function module_volunteer_page() 
{
	
}
function volunteer_page() 
{
	layui.use('form', function(){
	  var form = layui.form;
	  //监听提交
	  form.on('submit(userPage)', function(data){
	    layer.msg(JSON.stringify(data.field));
	    return false;
	  });
	  form.render();
	});
}
function destruct_volunteer_page() 
{
	
}
function module_erji_header() 
{
	this.test = function() 
	{
		console.log("hello,module_erji_header!");
	}
}
function host_page_header()//host_page_header别名的构造函数
{
	$('#host_page_header .layui-row .goto_left .return_span').on('click',function() 
	{
		LimitControl.removePage("hostPage","right");
	})
	$('#host_page_header .layui-row .goto_center .img_logo').on('click',function() 
	{
		//LimitControl.removeModule("body","right");
		LimitControl.removePage("hostPage","bottom");
	})
}
function destruct_host_page_header()//host_page_header别名的析构函数
{
	
}
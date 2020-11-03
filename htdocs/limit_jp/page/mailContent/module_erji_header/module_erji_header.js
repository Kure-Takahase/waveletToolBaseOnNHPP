function module_erji_header() 
{
	this.test = function() 
	{
		console.log("hello,module_erji_header!");
	}
}
function mailContent_header()//mailContent_header别名的构造函数
{
	$('#mailContent_header .layui-row .goto_left .return_span').on('click',function() 
	{
		LimitControl.removePage("mailContent","right");
	})
	$('#mailContent_header .layui-row .goto_center .img_logo').on('click',function() 
	{
		//LimitControl.removeModule("body","right");
		LimitControl.removePage("mailContent","bottom");
	})
}
function destruct_mailContent_header()//mailContent_header别名的析构函数
{
	
}
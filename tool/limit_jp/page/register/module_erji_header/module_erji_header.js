function module_erji_header() 
{
	this.test = function() 
	{
		console.log("hello,module_erji_header!");
	}
}
function register_header()//register_header别名的构造函数
{
	$('#register_header .layui-row .goto_left .return_span').on('click',function() 
	{
		LimitControl.removePage("register","right");
	})
	$('#register_header .layui-row .goto_center .img_logo').on('click',function() 
	{
		//LimitControl.removeModule("body","right");
		LimitControl.removePage("register","bottom");
	})
}
function destruct_register_header()//register_header别名的析构函数
{

}
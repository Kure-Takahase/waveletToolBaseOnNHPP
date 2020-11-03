function module_erji_header() 
{
	this.test = function() 
	{
		console.log("hello,module_erji_header!");
	}
}
function login_header()//login_header别名的构造函数
{
	$('#login_header .layui-row .goto_left .return_span').on('click',function() 
	{
		LimitControl.removePage("login","right");
	})
	$('#login_header .layui-row .goto_center .img_logo').on('click',function() 
	{
		//LimitControl.removeModule("body","right");
		LimitControl.removePage("login","bottom");
	})
}
function destruct_login_header()//login_header别名的析构函数
{

}
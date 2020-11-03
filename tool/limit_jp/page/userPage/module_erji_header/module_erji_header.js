function module_erji_header() 
{
	this.test = function() 
	{
		console.log("hello,module_erji_header!");
	}
}
function my_page_header()//my_page_header别名的构造函数
{
	$('#my_page_header .layui-row .goto_left .return_span').on('click',function() 
	{
		LimitControl.removePage("userPage","right");
	})
	$('#my_page_header .layui-row .goto_center .img_logo').on('click',function() 
	{
		LimitControl.removePage("userPage","bottom");
	})
}
function destruct_my_page_header()//login_header别名的析构函数
{

}
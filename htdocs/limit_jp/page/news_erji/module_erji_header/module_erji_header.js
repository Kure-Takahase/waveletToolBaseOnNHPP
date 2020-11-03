function module_erji_header() 
{
	this.test = function() 
	{
		console.log("hello,module_erji_header!");
	}
}
function news_erji_header()
{
	$('#news_erji_header .layui-row .goto_left .return_span').on('click',function() 
	{
		//LimitControl.removeModule("body","right");
		LimitControl.removePage("news_erji","right");
	})
	$('#news_erji_header .layui-row .goto_center .img_logo').on('click',function() 
	{
		//LimitControl.removeModule("body","right");
		LimitControl.removePage("news_erji","bottom");
	})
}
function destruct_news_erji_header()//register_header别名的析构函数
{

}
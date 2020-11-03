function module_erji_header() 
{
	this.test = function() 
	{
		console.log("hello,module_erji_header!");
	}
}
function tie_erji_header()
{
	$('#tie_erji_header .layui-row .goto_left .return_span').on('click',function() 
	{
		//LimitControl.removeModule("body","right");
		LimitControl.removePage("tie_erji","right");
	})
	$('#tie_erji_header .layui-row .goto_center .img_logo').on('click',function() 
	{
		//LimitControl.removeModule("body","right");
		LimitControl.removePage("tie_erji","bottom");
	})
}
function destruct_tie_erji_header()//register_header别名的析构函数
{

}
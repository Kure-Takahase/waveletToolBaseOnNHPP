function init()
{
	//加载二级标题栏
	LimitControl.loadModule("hostPage","hostPage","host_page_header","module_erji_header");
	//加载侧边导航栏
	LimitControl.loadModule("hostPage","hostPage","host_nav","module_host_side_nav");
	//加载初始页面
	LimitControl.loadModule("hostPage","hostPage","volunteer_page","module_volunteer_page");
}
function pre_init() 
{
	
}
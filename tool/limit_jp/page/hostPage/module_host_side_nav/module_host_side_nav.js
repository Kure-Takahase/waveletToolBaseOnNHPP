function module_host_side_nav() 
{
    this.nowModule;
    this.getNowModule = function () 
    {
    	return nowModule;
    }
    this.setNowModule = function (Module) 
    {
    	nowModule = Module;
    }
}
function host_nav() 
{
	LimitControl.moduleObject("hostPage","host_nav").setNowModule('volunteer_page');
	//console.log("host_nav ok");
	$(".host_side_nav").on('click',function(){
		$("#host_side_nav_volunteer").removeClass("nav_is_checked");
	})
	//志愿者按钮
	$("#host_side_nav_volunteer").on('click',function()
	{
		nowModule = LimitControl.moduleObject("hostPage","host_nav").getNowModule();
		//console.log("nowModule:"+nowModule);
		if(nowModule == 'volunteer_page')
			return ;
		//移除上一页面
		LimitControl.removeModule("hostPage",nowModule);
		//加载当前页面
		LimitControl.loadModule("hostPage","hostPage","volunteer_page","module_volunteer_page");
		//设置当前页面
		LimitControl.moduleObject("hostPage","host_nav").setNowModule('volunteer_page');
	})
	//Host按钮
	$("#host_side_nav_host").on('click',function()
	{
		nowModule = LimitControl.moduleObject("hostPage","host_nav").getNowModule();
		//console.log("nowModule:"+nowModule);
		if(nowModule == 'host_page')
			return ;
		//移除上一页面
		LimitControl.removeModule("hostPage",nowModule);
		//加载当前页面
		LimitControl.loadModule("hostPage","hostPage","host_page","module_host_page");
		//设置当前页面
		LimitControl.moduleObject("hostPage","host_nav").setNowModule('host_page');
	})
	//站内信按钮
	$("#host_side_nav_message_box").on('click',function()
	{
		nowModule = LimitControl.moduleObject("hostPage","host_nav").getNowModule();
		//console.log("nowModule:"+nowModule);
		if(nowModule == 'message_box_list')
			return ;
		//移除上一页面
		LimitControl.removeModule("hostPage",nowModule);
		//加载当前页面
		LimitControl.loadModule("hostPage","hostPage","message_box_list","module_message_box_list");
		//设置当前页面
		LimitControl.moduleObject("hostPage","host_nav").setNowModule('message_box_list');
	})
}
function destruct_host_nav()
{
	
}
//初始化函数执行
function init()
{
    //console.log("index.js ok!");
	//载入模块
	LimitControl.loadModule("index","index","index_tab","module_tab");
	LimitControl.loadModule("index","index","index_header","module_header");

	console.log("1");
	LimitControl.loadModule("index","jpcnBBS_news","news_page","module_news");
	console.log("2");
	LimitControl.loadModule("index","jpcnBBS_bbs","tie_page","module_tie");
	console.log("3");
	LimitControl.loadModule("index","liuqiong_my","friend_list","module_friend_list");
	console.log("4");
	LimitControl.loadModule("index","liuqiong_cart","volunteer","module_volunteer");
	console.log("5");
}
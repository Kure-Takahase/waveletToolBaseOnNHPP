/**
 * LimitControl 2.0
 * 模块约定 与 注意事项
 * 1.模块最外层应只有一个DIV
 * 2.模块最外层必须设置id名为 "$aliasName$"
 * 3.模块最外层DIV初始建议设置为不显示(display:none)。以免在动画载入时出现闪烁
 * 4.模块css文件应放在css文件夹内。js文件应放在js文件夹内。HTML代码段放在html文件夹内
 * 5.路径默认为: 网站根目录/module/...
 * 6.不要对最外层div设置z-index属性
 * 0.以下函数请勿修改。框架基础函数
 *
 * 方法列表:
 * 1.加载模块		loadModule() 		
 * 2.移除模块		removeModule()
 * 3.设置模块动画速度	setAnimateTime()
 */
var LimitControl = new LimitControl();

function LimitControl()
{
	var hostName 	= "http://"+window.location.host+"/";
	var staticHost 	= "http://"+window.location.host+"/";
	var stack 		= new Array(500);//保存所有页面的所有模块别名
	var stackName 	= new Array(500);//保存所有页面的所有模块名
	var stackParent = new Array(500);//保存所有页面的所有模块parent
	var moduleObject= new Array(500);//保存所有页面的所有模块JS对象
	var animateTime = 700;
	var isAnimate 	= false;
	var projectName = null;
	var moduleTotal = 0;
	var pageTotal 	= 0;
	this.loadPage = function( pageName, dirt)
	{
		$('body').css("pointer-events","none");
		isAnimate = true;
		dirt = dirt || 'right';
		pageTotal ++;
		$('body').prepend( "<div id='" + pageName + "' style='width:100%;height:100%;position:absolute;z-index:"+ pageTotal +";'></div>" );
		var jsURL = LimitControl.staticHost() + 'page/' + pageName + '/' + 'init.js';
		loadPageJs(jsURL,pageName);
		if(dirt != 'none')
			moduleAnimate(pageName, 'in', dirt, animateTime, function(){$('body').css("pointer-events","auto");isAnimate = false;})
		else
			isAnimate = false;
		if(isAnimate == false)
			$('body').css("pointer-events","auto");
	}
	this.loadModule = function( pageName, parent, aliasName, moduleName, dirt , insertDirt )
	{
		$('body').css("pointer-events","none");
		if( pageName == null || moduleName == null || aliasName == null )
		{
			if(isAnimate == false)
				$('body').css("pointer-events","auto");
			return false;
		}
		//aliasName  	= pageName + moduleName + aliasName;
		//parent 		= pageName + moduleName + parent;
		dirt = dirt || "none";
		insertDirt 	= insertDirt || "tail";
		//如果pageName作用域未定义，则创建该pageName作用域
		if(stack.hasOwnProperty( pageName ) == false)
		{
			stack[ pageName ] = new Array();
			moduleObject[ pageName ] = new Array();
			stackName[ pageName ] = new Array();
			stackParent[ pageName ] = new Array();
		}
		//若该模块已被加载，则退出。避免重复加载
		if($.inArray( aliasName, stack[ pageName ] ) != -1)
		{
			//console.log("该模块已被加载");
			if(isAnimate == false)
				$('body').css("pointer-events","auto");
			return false;
		}

		stackName[ pageName ][ aliasName ]	 = moduleName;
		stackParent[ pageName ][ aliasName ] = parent;
		var lastModule = stack[pageName].length;
		moduleTotal += 1;
		moduleObject[pageName][aliasName] = loadModule(pageName, parent, aliasName, moduleName, dirt, moduleTotal, animateTime, insertDirt, staticHost);
		//console.log(aliasName);
		//console.log(moduleObject[pageName][aliasName]);
		//执行模块构造函数
		window[aliasName]();
		stack[pageName][ lastModule ]  = aliasName;
		if(isAnimate == false)
			$('body').css("pointer-events","auto");
		//console.log($('body').css("pointer-events"));
		return moduleObject[pageName][aliasName];
	}
	this.removePage = function( pageName, dirt = "none", aliasName = "all", time = 700 ) 
	{
		pageTotal --;
		dirt = dirt || "none";
		time = time || 700;
		moduleTotal -= 1;
		var moduleNames = stackName[pageName];
		var aliasNames = stack[pageName];
		if(dirt != "none")
		{
			$('body').css("pointer-events","none");
			moduleAnimate(pageName,"out",dirt,animateTime,function () 
			{
				$('body').css("pointer-events","auto");
				deletePage(pageName,moduleNames,aliasNames);
			});
		}
		else
		{
			deletePage(pageName,moduleNames,aliasNames);
		}
	}
	this.removeModule = function(pageName,aliasName, dirt = "none", time = 700)
	{
		//console.log(pageName+" "+aliasName);
		var parent = stackParent[ pageName ][ aliasName ];
		//console.log(parent);
		moduleTotal -= 1;
		if(dirt != "none")
		{
			$('body').css("pointer-events","none");
			moduleAnimate(aliasName,"out",dirt,animateTime,function () 
			{
				$('body').css("pointer-events","auto");
				var index = stack[pageName].indexOf(aliasName);
				if (index > -1)
				    stack[pageName].splice(index, 1);
				deleteModule(aliasName);
			});
		}
		else
		{
			var index = stack[pageName].indexOf(aliasName);
			if (index > -1)
				   stack[pageName].splice(index, 1);
			deleteModule(aliasName);
		}
	}
	this.setAnimateTime = function(time) 
	{
		animateTime = time;
	}
	this.setStaticHost = function(host) 
	{
		staticHost = host;
	}
	this.staticHost = function(host) 
	{
		return staticHost;
	}
	this.setHostName = function(host)
	{
		hostName = host;
	}
	this.hostName = function(host) 
	{
		return hostName;
	}
	this.setProjectName = function(name) 
	{
		projectName = name;
	}
	this.projectName = function(name) 
	{
		return projectName;
	}
	this.moduleObject = function(pageName,aliasName) 
	{
		//console.log(moduleObject[pageName]);
		return moduleObject[pageName][aliasName];
	}
	this.staticImgURLtoReal = function(str)//将str字符串内的pre子串替换为after
	{
		var obj_res;
		while(true)
 		{
 			obj_res = str.replace("$staticImgURL/",LimitControl.staticHost() +"img/");
	 		if(obj_res == str)
	 			break;
	 		str = obj_res;
 		}
 		return str;
	}
	this.sendAjax = function(url,data,success_callBack,fail_callBack) 
	{
		$.ajax
		({
			url: url,
			type:"post",
			dataType:"text",
			data:data,
			
			success:function(data)
			{
				success_callBack(data);
			},
			error:function(e)
			{
				fail_callBack(e);
			}
		});
	}
	this.clearArr = function(pageName)
	{
		stack[ pageName ] = [];
		moduleObject[ pageName ] = [];
		stackName[ pageName ] = [];
	}
	this.setIsAnimate = function(Animate) 
	{
		isAnimate = Animate;
	}
	this.getIsAnimate = function() 
	{
		return isAnimate ;
	}

}
/**
 * 模块移除函数。
 * 
 */
function deletePage(pageName,moduleNames,aliasNames)
{
	$("#"+pageName).remove();
	LimitControl.clearArr(pageName);
	var cssURL;
	for(var key in moduleNames)
	{
		cssURL = LimitControl.staticHost() + "page/" + pageName + "/" + moduleNames[key] + "/" + moduleNames[key] + ".css";
		removejscssfile(cssURL,"css");
	}
	for(var key in aliasNames)
	{
		//执行析构函数
		window["destruct_"+aliasNames[key]]();
	}
}
function deleteModule(aliasName)
{
	//执行析构函数
	window["destruct_"+aliasName]();
	$("#"+aliasName).remove();
}
function removejscssfile(filename,filetype)
{
	var targetelement=(filetype=="js")? "script" :(filetype=="css")? "link" : "none"
	var targetattr=(filetype=="js")?"src" : (filetype=="css")? "href" :"none"
	var allsuspects=document.getElementsByTagName(targetelement)
	for (var i=allsuspects.length; i>=0;i--)
	{
		if (allsuspects[i] &&allsuspects[i].getAttribute(targetattr)!=null && allsuspects[i].getAttribute(targetattr).indexOf(filename)!=-1)
			allsuspects[i].parentNode.removeChild(allsuspects[i])
	}
}
/**
 * 模块加载函数。
 * 所有的模块的HTML代码块都从viewModule控制器请求获取
 * parent 参数表示放入加载的模块的元素
 * dirt   参数表示模块的展现方式。可选值：left,right,top,bottom,none
 */
function loadModule(pageName,parent,aliasName,moduleName,dirt,now,animateTime,insertDirt,staticHost)
{
	var moduleObject = null;
	var cssURL = LimitControl.staticHost() + "page/" + pageName + "/" + moduleName + "/" + moduleName + ".css";
	var htmlURL = LimitControl.staticHost() + "page/" + pageName + "/" + moduleName + "/" + moduleName + ".html";
	var jsURL = LimitControl.staticHost() + "page/" + pageName + "/" + moduleName + "/" + moduleName + ".js";
	//载入css
	$("<link>")
	.attr({ rel: "stylesheet",
	type: "text/css",
	href:cssURL,
	}).appendTo("head");
	//载入别名块
	if(insertDirt == "tail")
		$('#'+parent).append( "<div id='" + aliasName + "' style='width:100%;height:100%;'></div>" );
	else if(insertDirt == "head")
		$('#'+parent).prepend( "<div id='" + aliasName + "' style='width:100%;height:100%;'></div>" );
	//请求HTML代码块
	$.ajax
	({
	 	url:htmlURL,
	 	type:"get",
	 	async: false,
		data:{
			moduleName:moduleName,
			aliasName:aliasName
		},
	 	success:function(result)
	 	{
	 		var res = result;
	 		var obj_res;
	 		//res = res.replace("$aliasName$",aliasName);
	 		while(true)
	 		{
	 			obj_res = res.replace("$staticImgURL/",LimitControl.staticHost() +"img/");
		 		if(obj_res == res)
		 			break;
		 		res = obj_res;
	 		}
	 		//载入HTML代码块
	 		$("#"+aliasName).append(res);
			//载入js
			moduleObject = loadModuleJs(staticHost,jsURL,aliasName,now,animateTime,dirt,moduleName);
  		}
	});
	return moduleObject;
}
function loadPageJs(jsURL,moduleObjectName) 
{
	//console.log(jsURL);
	$.ajax
	({
		url:jsURL,
		type:"get",
		dataType: "script",
		async: false,
		success:function()
		{
			//console.log(moduleObjectName);
			window['init']();
			//console.log("loadPageJs finish");
	  	}
	});
}
function loadModuleJs(staticHost,jsURL,aliasName,now,animateTime,dirt,moduleObjectName) 
{
	//console.log(jsURL);
	var moduleObject = null;
	$.ajax
	({
		url:jsURL,
		type:"get",
		dataType: "script",
		async: false,
		success:function()
		{
			//console.log("success ok."+aliasName+" "+moduleObjectName);
			var Module = $("#"+aliasName);
			Module.css("z-index",now);
			Module.show();
			if(dirt != "none")
			{
				LimitControl.setIsAnimate(true);
				//var position = Module.css("position");
				function returnPos()
				{
					LimitControl.setIsAnimate(false);
					$('body').css("pointer-events","auto");
					//console.log($('body').css("pointer-events"));
				}
				moduleAnimate(aliasName,"in","right",animateTime,returnPos);
			}
			moduleObject = new window[moduleObjectName]();
	  	},
  		error:function(e)
  		{
  			//console.log(e.responseText);
  		}
	});
	//console.log(moduleObject);
	return moduleObject;
}
function moduleAnimate(aliasName, finalPosition, dirt, time, callBack) 
{
	var Module = $("#"+aliasName);
	Module.css("position","absolute");
	if(finalPosition == "in")
	{
		if(dirt == "right")
		{
			Module.css("left","100%");
			Module.animate({left:"0%"}, time, callBack);
		}
		else if(dirt == "left")
		{
			Module.css("right","100%");
			Module.animate({right:"0%"}, time, callBack);
		}
		else if(dirt == "top")
		{
			Module.css("bottom","100%");
			Module.animate({bottom:"0%"}, time, callBack);
		}
		else if(dirt == "bottom")
		{
			Module.css("top","100%");
			Module.animate({top:"0%"}, time, callBack);
		}
	}
	else if(finalPosition == "out")
	{
		if(dirt == "right")
		{
			Module.animate({left:"100%"}, time, callBack);
		}
		else if(dirt == "left")
		{
			Module.animate({right:"100%"}, time, callBack);
		}
		else if(dirt == "top")
		{
			Module.animate({bottom:"100%"}, time, callBack);
		}
		else if(dirt == "bottom")
		{
			Module.animate({top:"100%"}, time, callBack);
		}
	}
}
<html style="overflow: hidden;">
<head>
	<meta charset="UTF-8">
	<title><?php echo $title; ?></title>
	<link rel="shortcut icon" href="<?php echo base_url('/img/'.$shortcutIcon);?>" />
	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
	<!-- 载入layui CSS -->
	<link rel="stylesheet" href="<?php echo base_url('/core/layui/css/layui.css');?>"  media="all">
</head>

<body id="body" style="position:relative; overflow: hidden;">
</body>

<!-- 载入layui JS -->
<script src="<?php echo base_url('/core/layui/layui.js');?>"></script>
<!-- 载入jquery -->
<script src="https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
<!-- 载入jquery cookie -->
<script src="https://cdn.bootcss.com/jquery-cookie/1.4.1/jquery.cookie.min.js"></script>
<!-- 载入md5插件 -->
<script src="<?php echo base_url('/core/')."md5.js";?>"></script>
<!-- 载入LimitControl控制模块 -->
<script src="<?php echo base_url('/core/')."LimitControl.js";?>"></script>
<!-- 模块组入口 -->
<script>
	//载入layer模块
	layui.use('layer', function(){});
    layui.use('element', function(){});
	//加载websocket
	var ws;
	WebSocketTest(<?php echo $isWebSocket;?>);
	//设置网站域名
	LimitControl.setHostName("<?php echo $host_url;?>");
	//设置Limit框架目录路径
	LimitControl.setStaticHost("<?php echo $CDN_url;?>");
	//设置模块出现速度
	LimitControl.setAnimateTime(<?php echo $animateTime;?>);
	//加载入口代码
	LimitControl.loadPage("<?php echo $index_page;?>","none");
	
    function WebSocketTest(isWebSocket)
    {
    	if(isWebSocket != true)
    		return ;
        if ("WebSocket" in window)
        {
            // 打开一个 web socket
            ws = new WebSocket("<?php echo $ws_url;?>");
            //ws = new WebSocket("ws://dreamSchool.wujingchi.com:8282");
            ws.onopen = function() 
            {
                console.log("open websocket success!");
            };

            ws.onmessage = function (evt) 
            {
                var received_msg = evt.data;
                data = JSON.parse(received_msg);
                if(data.type == 'init')
                    $.cookie('client_id', data.client_id);  
                //console.log("from websocket:");
                //console.log(data);
            };

            ws.onclose = function()
            {
                console.log("websocket onclose");
            };
        }
        else
        {
        	// 浏览器不支持 WebSocket
            layer.msg('因您的浏览器版本过低或设备原因，将无法使用好友功能！请升级至最新浏览器(推荐Chrome)', {
                time: 3000, //3s后自动关闭
            });
        }
    }
</script>
</html>
<!DOCTYPE HTML>
<html>
    <head>
        <meta charset="utf-8">
        <title>websocket测试</title>
        <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>
        <script src="https://cdn.bootcss.com/jquery-cookie/1.4.1/jquery.cookie.min.js"></script>
        <script type="text/javascript">
            var ws;
            function WebSocketTest()
            {
                if ("WebSocket" in window)
                {
                    // 打开一个 web socket
                    ws_url = document.getElementById("ws_url").value;
                    ws = new WebSocket(ws_url);
                    //ws = new WebSocket("ws://dreamSchool.wujingchi.com:8282");
                    ws.onopen = function() 
                    {
                        console.log("open websocket success!");
                    };

                    ws.onmessage = function (evt) 
                    {
                        var received_msg = evt.data;
                        var h3= document.getElementById("my_div");
                        h3.innerHTML = received_msg;
                        data = JSON.parse(received_msg);
                        if(data.type == 'init')
                            $.cookie('client_id', data.client_id);
                        console.log("from websocket:");
                        console.log(data);

                        
                    };

                    ws.onclose = function()
                    {
                        console.log("websocket onclose");
                    };
                }
                else
                {
                // 浏览器不支持 WebSocket
                    alert("您的浏览器不支持 WebSocket!");
                }
            }
            //WebSocketTest();
            function login()
            {
                var url = 'https://jpcnbbs.wujingchi.com/index.php/User/login';
                //var url = 'https://jpcnbbs.wujingchi.com/index.php/Test/websocketTest';
                var inputValue  = document.getElementById("email").value;
                var password    = document.getElementById("password").value;
                var data = {
                    "email"     : inputValue,
                    "password"  : password,
                    'client_id' : $.cookie('client_id')
                };
                send(url,data);
            }
            function who()
            {
                //var url = 'https://jpcnbbs.wujingchi.com/index.php/Test/ajaxTest';
                var url = 'https://jpcnbbs.wujingchi.com/index.php/Common/who';
                send(url);
            }
            function custom()
            {
            	var url 		= document.getElementById("ajax_url").value;
                var controller  = document.getElementById("controller").value;
                var action      = document.getElementById("action").value;
                var json        = document.getElementById("json").value;
                var data        = JSON.parse(json);
                var url = url +controller+'/'+action;
                send(url,data);
            }
            function send(URL,dataArray = null)
            {
                console.log(dataArray);
                $.ajax
                ({
                    withCredentials:true,
                    dataType: "json",
                    url:URL,
                    type:"post",
                    data:dataArray,
                    success:function(result)
                    {
                        if(result != "")
                        {
                        	//var obj = result.parseJSON();
                        	console.log(result);
                        }    

                    },
                    error:function (error)
                    {
                        console.log(error.responseText);
                        var h3= document.getElementById("ajax_div");
                        h3.innerHTML = error.responseText;
                    }
                });
            }
        </script>
        
    </head>
    <body>
    <input type="text" placeholder="输入ws地址" value="wss://jpcnbbs.wujingchi.com:8484" id="ws_url">
    <button id="button" onclick="WebSocketTest();">连接ws</button><br>
    <input type="text" placeholder="输入你的email" value="2453219525@qq.com" id="email" >
    <input type="text" placeholder="输入你的password" value="q1234567" id="password" >
    <button id="button" onclick="login();">登录</button>
    <button id="button" onclick="who();">向服务器询问我是谁</button><br><br>
    <input type="text" placeholder="输入ajax_url" value="https://jpcnbbs.wujingchi.com/index.php/" id="ajax_url" >
    <input type="text" placeholder="输入控制器名" id="controller" >
    <input type="text" placeholder="输入方法名" id="action" >
    <input type="text" placeholder="输入json" id="json" ><br><br>
    <button id="button" onclick="custom();">自定义发送</button>
    <div id="my_div"></div>
    <div id="ajax_div"></div>
    </body>
</html>
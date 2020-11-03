function updateUni()
{
	var timestamp = (new Date()).valueOf();
	$.cookie('uniqueNum', timestamp);
	console.log("标识码已重置")
	$("#taskName").val("")
	$("#upfile_name1").html("")
	$("#upfile_name2").html("")
	$("#upfile_name3").html("")
	$("#upfile_name4").html("")
	//重置已上传的代码文件数组
	fileArr = new Array();
	var jsonStr = JSON.stringify(fileArr);
	$.cookie('fileArr', jsonStr);
}
function index_tab()
{
	$.cookie('last_num',0)

	var myDate = new Date();
	//获取当前年
	var year = myDate.getFullYear();
	//获取当前月
	var month = myDate.getMonth() + 1;
	$.cookie('date', year.toString()+'_'+month.toString());
	//创建标识码
	var timestamp = (new Date()).valueOf();
	$.cookie('uniqueNum', timestamp);
	layui.use('element', function(){
		var element = layui.element;
		//…
	});
	//创建已上传的代码文件数组
	//cookie可写性证明
	fileArr = new Array();
	fileArr.push('hello')
	var jsonStr = JSON.stringify(fileArr);
	$.cookie('fileArr', jsonStr);
	console.log($.cookie('fileArr'))

	fileArr = new Array();
	var jsonStr = JSON.stringify(fileArr);
	$.cookie('fileArr', jsonStr);



	layui.use('form', function(){
		var form = layui.form;
		//监听提交
		form.on('submit(formDemo)', function(data){
			taskName = data.field.taskName;
			if(taskName.length > 15)
			{
				layer.msg('任务名必须小于15个字符!',{time:2000});
				return false;
			}
			console.log(taskName);
			taskCodeFile = $("#upfile_name1").text();
			dataFile = $("#upfile_name2").text();
			paraFile = $("#upfile_name3").text();
			/*
			if(taskCodeFile == "")
			{
				layer.msg('必须上传任务代码!',{time:2000});
				return false;
			}
			if(dataFile == "")
			{
				layer.msg('必须上传数据文件!',{time:2000});
				return false;
			}
			if(paraFile == "")
			{
				layer.msg('必须上传参数文件!',{time:2000});
				return false;
			}
			*/
			other = $.cookie('fileArr');
			//发送ajax,请求添加任务
			url = LimitControl.hostName() + 'PythonDistributedComputing/addTask' //上传接口
			data = {
				taskName:taskName,					//任务名
				taskCodeFile:taskCodeFile,			//任务代码
				dataFile:dataFile,					//数据文件
				paraFile:paraFile,					//参数文件
				otherCodeFile:other,//依赖文件
				uniqueNum:function() {				//标识码
					return $.cookie('uniqueNum');
				},
				date:function() {					//年月编号	
					return $.cookie('date');
				},
			}
			success_callBack = function(data) 
			{
				console.log(data)
				layer.msg('任务添加成功!',{time:2000});
				//重置页面
				updateUni();
			}
			fail_callBack = function(data) 
			{
				layer.msg('任务添加失败...',{time:2000});
			}
			LimitControl.sendAjax(url,data,success_callBack,fail_callBack)

			//layer.msg(JSON.stringify(data.field));
			//var data1 = form.val("formTest");
			//console.log(data1);
			return false;
		});
	});
	layui.use('upload', function(){
		var upload = layui.upload;

		//执行实例
		//上传任务代码及其依赖文件
		var uploadInst = upload.render({
			elem: '#test1' //绑定元素
			,auto: true //选择文件后自动上传
			,accept:'py'
			,data:{
				date:function(){			//年月编号
    							return $.cookie('date');
  							}, 			
				uniqueNum : function(){
    							return $.cookie('uniqueNum');
  							}
			}
			,url: LimitControl.hostName() + 'PythonDistributedComputing/fileUpload' //上传接口
			,done: function(res){
				//res = JSON.parse( res )
				//console.log(res);
				$("#upfile_name1").html("")
				$("#upfile_name1").html(res.filename)
				layer.msg('任务代码已上传!',{time:2000}); 
			}
			,error: function(){
				console.log("no");
			  //请求异常回调
			}
		});
	});
	layui.use('upload', function(){
		var upload = layui.upload;

		//执行实例
		//上传任务代码及其依赖文件
		var uploadInst = upload.render({
			elem: '#test4' //绑定元素
			,auto: true //选择文件后自动上传
			,accept:'py'
			,multiple: true //允许多文件上传
			,data:{
				date:function(){			//年月编号
    							return $.cookie('date');
  							}, 			
				uniqueNum : function(){
    							return $.cookie('uniqueNum');
  							}
			}
			,url: LimitControl.hostName() + 'PythonDistributedComputing/fileUpload' //上传接口
			,allDone: function(obj){ //当文件全部被提交后，才触发
				layer.msg('已上传所有选择的文件!',{time:2000}); 
			}
			,done: function(res){
				console.log(res);
				jsonStr = $.cookie('fileArr')
				fileArr = JSON.parse( jsonStr );
				//避免重复上传文件时，多次显示同一个文件名
				var index =  fileArr.indexOf(res.filename);
				if(index == -1)
				{
					fileArr.push(res.filename)
					var jsonStr = JSON.stringify(fileArr);
					$.cookie('fileArr', jsonStr);
					console.log($.cookie('fileArr'))
					var val = $("#upfile_name4").text()
					$("#upfile_name4").html(val+res.filename+" ")
				}
			}
			,error: function(){
				console.log("no");
			  //请求异常回调
			}
		});
	});
	layui.use('upload', function(){
		var upload = layui.upload;

		//执行实例
		//上传任务代码及其依赖文件
		var uploadInst = upload.render({
			elem: '#test2' //绑定元素
			,auto: true //选择文件后自动上传
			,accept:'file'
			,exts:'txt|xlsx|xls'
			,acceptMime : 'text/plain,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
			,data:{
				date:function(){			//年月编号
    							return $.cookie('date');
  							}, 			
				uniqueNum : function(){
    							return $.cookie('uniqueNum');
  							}
			}
			,url: LimitControl.hostName() + 'PythonDistributedComputing/fileUpload' //上传接口
			,done: function(res){
				//res = JSON.parse( res )
				console.log(res);
				$("#upfile_name2").html("")
				$("#upfile_name2").html(res.filename)
				layer.msg('文件已上传!',{time:2000}); 
			}
			,error: function(){
				console.log("no");
			  //请求异常回调
			}
		});
	});
	layui.use('upload', function(){
		var upload = layui.upload;

		//执行实例
		//上传任务代码及其依赖文件
		var uploadInst = upload.render({
			elem: '#test3' //绑定元素
			,auto: true //选择文件后自动上传
			,accept:'file'
			,exts:'txt|xlsx|xls'
			,acceptMime : 'text/plain,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
			,data:{
				date:function(){			//年月编号
    							return $.cookie('date');
  							}, 			
				uniqueNum : function(){
    							return $.cookie('uniqueNum');
  							}
			}
			,url: LimitControl.hostName() + 'PythonDistributedComputing/fileUpload' //上传接口
			,done: function(res){
				console.log(res);
				var val = $("#upfile_name3").text()
				//console.log(val);
				$("#upfile_name3").html("")
				$("#upfile_name3").html(res.filename)
				layer.msg('文件已上传!',{time:2000}); 
			}
			,error: function(){
				console.log("no");
			  //请求异常回调
			}
		});
	});

	layui.use('code', function(){
  		
		layui.code({
			height:'450px',
			about:false
		});
	});
	/*
	layui.use('table', function(){
		var table = layui.table;
		//转换静态表格
		table.init('parse-table-demo', {
			count:3
			,height: 312 //设置高度
			,limit: 10 //注意：请务必确保 limit 参数（默认：10）是与你服务端限定的数据条数一致
			//支持所有基础参数
			,page: true //开启分页
		}); 
	  	/*
		//第一个实例
		table.render({
			elem: '#demo'
			,height: 312
			,url: LimitControl.hostName()+'PythonDistributedComputing/getTaskList' //数据接口
			,page: true //开启分页
			,cols: [[ //表头
			
				{field: 'id', title: '文件名', width:250, fixed: 'left'}
				,{field: 'status', title: '状态', width:80}
				,{field: 'complete', title: '已完成', width:100}
				,{field: 'time', title: '剩余时间' } 
				,{field: 'active', title: '操作', width: 64}
			
			/*
			{field: 'id', title: 'ID', width:80, sort: true, fixed: 'left'}
	      ,{field: 'username', title: '用户名', width:80}
	      ,{field: 'sex', title: '性别', width:80, sort: true}
	      ,{field: 'city', title: '城市', width:80} 
	      ,{field: 'sign', title: '签名', width: 177}
	      ,{field: 'experience', title: '积分', width: 80, sort: true}
	      ,{field: 'score', title: '评分', width: 80, sort: true}
	      ,{field: 'classify', title: '职业', width: 80}
	      ,{field: 'wealth', title: '财富', width: 135, sort: true}
	      
			]]
		});
	});*/

}
function showMasterOutput()
{
	//发送ajax,请求添加任务
	url = LimitControl.hostName() + 'PythonDistributedComputing/getOutput' //上传接口
	data = {
		last_num:$.cookie('last_num')
	}
	success_callBack = function(data) 
	{
		//console.log(data)
		res = JSON.parse( data )
		//$("#control-view").html(res[0][1])
		if(res.length > 0)
		{
			console.log('有新的输出')
			console.log(data)
			for(j = 0,len=res.length; j < len; j++) 
			{
				console.log("开始添加"+res[j][1])
				$(".layui-code-ol").append('<li>'+res[j][1]+'</li>');
				//$("#control-view").append('\n'+res[j][1]);
			}
			$.cookie('last_num',res[res.length-1][0])
			last_num = $.cookie('last_num')
			console.log("添加完成,移动滚动条")
			$(".layui-code-ol").scrollTop(last_num*20);
		}
		else
			console.log("没有新的输出")
		setTimeout(function () {showMasterOutput();},1000);
	}
	fail_callBack = function(data) 
	{

	}
	LimitControl.sendAjax(url,data,success_callBack,fail_callBack)
}

function checkMasterLive() 
{
	//发送ajax,请求添加任务
	url = LimitControl.hostName() + 'PythonDistributedComputing/isMasterLive' //上传接口
	data = {
		
	}
	success_callBack = function(data) 
	{
		console.log(data)

		if(data == 'pong')
		{
			$("#master_status").html('运行中<i class="layui-icon layui-icon-circle-dot" style="margin-left: 3px; font-size: 12px; color: #5FB878;"></i>')
			//$("#master_active").html('无')
			showMasterOutput()
			$("#stop_server").show()
			$("#start_server").hide()
		}
	}
	fail_callBack = function(data) 
	{

	}
	LimitControl.sendAjax(url,data,success_callBack,fail_callBack)
}
function start_server(status) 
{
	//发送ajax,请求添加任务
	url = LimitControl.hostName() + 'PythonDistributedComputing/startServer' //上传接口
	data = {
		status:status
	}
	success_callBack = function(data) 
	{
		checkMasterLive()
	}
	fail_callBack = function(data) 
	{

	}
	LimitControl.sendAjax(url,data,success_callBack,fail_callBack)
}
function loadExcelSaveTable() 
{
	//发送ajax,请求添加任务
	url = LimitControl.hostName() + 'PythonDistributedComputing/getExcelSaveFilesList' //上传接口
	data = {
		
	}
	success_callBack = function(data) 
	{
		console.log(location.host)
		try 
		{
            res = JSON.parse( data )
			length = res.length
			for (var i = 0; i < length; i++) 
			{
				html = ''
				html += '<tr>'
				html += '<td>'+(i+1)+'</td>'
				html += '<td>'+res[i]+'</td>'
				html += '<td><a href="https://'+location.host+'/Server/excel_save/'+res[i]+'" download="'+res[i]+'" ><button type="button" class="layui-btn layui-btn-xs layui-btn-radius">下载</button></a></td>'
				html += '</tr>'
				$("#excel_save_tbody").append(html)
			}
        }
        catch(e) 
        {
            console.log(e);
            return false;
        }
        layui.use('table', function(){
			var table = layui.table;
			//转换静态表格
			table.init('parse-table-demo', {
				count:res.length
				,height: 312 //设置高度
				,limit: 10 //注意：请务必确保 limit 参数（默认：10）是与你服务端限定的数据条数一致
				//支持所有基础参数
				,page: true //开启分页
			});
		});


	}
	fail_callBack = function(data) 
	{

	}
	LimitControl.sendAjax(url,data,success_callBack,fail_callBack)

}
console.log(document.cookie.length)
index_tab()
checkMasterLive()
loadExcelSaveTable()
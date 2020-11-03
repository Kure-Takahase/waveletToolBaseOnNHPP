function module_tab()
{

}

function index_tab() 
{
	layui.use('element', function(){
		var element = layui.element;
	  
	  //…
	});
	layui.use('form', function(){
	  var form = layui.form;
	  //监听提交
	  form.on('submit(formDemo)', function(data){

	    //layer.msg(JSON.stringify(data.field));
	    //var data1 = form.val("formTest");
	    //console.log(data1);
	    return false;
	  });
	});
	layui.use('upload', function(){
	  var upload = layui.upload;
	   
	  //执行实例
	  var uploadInst = upload.render({
	    elem: '#test1' //绑定元素
	    ,exts:'txt'
	    ,auto: false //选择文件后不自动上传
  		,bindAction: '#testListAction' //指向一个按钮触发上传
	    ,url: LimitControl.hostName() + 'Wavelet/upload' //上传接口
	    ,done: function(res){
	    	console.log(res);
	    	var data1 = layui.form.val("formTest");
	    	console.log(data1);
	    	var url = LimitControl.hostName() + 'Wavelet/execute';
	    	console.log("mode:"+data1.mode);
			var data_arr =
			{
				dataTransform 				: data1.dataTransform,
				thresholdRule 				: data1.thresholdRule,
				thresholdMethod 			: data1.thresholdMethod,
				filename 					: res.filename,
				mode 						: data1.mode
			}
			console.log(data_arr);
			function success_Wavelet_execute(data) 
			{
				str = jQuery.parseJSON(data)['output'][0];
				console.log(str);
				$("#res a").remove();
				$("#res").append("<a id='tem' href='"+str+"'>結果をダウンロード</a>");
			}
			function fail_Wavelet_execute(e) 
			{
				console.log(e.responseText);
			}


	    	LimitControl.sendAjax(url,data_arr,success_Wavelet_execute,fail_Wavelet_execute);
	        //上传完毕回调
	    }
	    ,error: function(){
	    	console.log("no");
	      //请求异常回调
	    }
	  });
	});
}

function destruct__index_tab()
{

}

index_tab()
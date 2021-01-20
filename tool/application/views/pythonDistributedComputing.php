<html>
<head>
	<meta charset="UTF-8">
	<title><?php echo $title; ?></title>
	<link rel="shortcut icon" href="<?php echo base_url('/limit/img/'.$shortcutIcon);?>" />
	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
	<!-- 载入layui CSS -->
	<link rel="stylesheet" href="<?php echo base_url('/limit/core/layui/css/layui.css');?>"  media="all">
	<link rel="stylesheet" href="<?php echo base_url('/limit/css/'.$pageName.'.css');?>"  media="all">
</head>

<body id="body" style="position:relative;">
	<ul class="layui-nav nav-fixed" lay-filter="">
		<li class="layui-nav-item"><a href="<?php echo site_url('welcome\index\waveletShrinkageEstimationTool');?>">小波收缩工具</a></li>
		<li class="layui-nav-item layui-this"><a href="<?php echo site_url('welcome\index\pythonDistributedComputing');?>">Python分布式计算平台</a></li>
	</ul>

	<div class="layout">
		<div class=" layadmin-user-login-header pythonDistributedComputingTitle">
			<h2>Python分布式计算平台</h2>
			<p>作者：Wu JingChi</p>
		</div>


		<fieldset class="layui-elem-field layui-field-title" style="margin-top: 30px;">
			<legend>添加任务</legend>
		</fieldset>
		<!-- 登录页 -->
		<div class="login_shade_div">
			<!-- 登录内容 -->

			<div class="layadmin-user-login layadmin-user-display-show" id="LAY-user-login" style="display: none;">
				<div class="layadmin-user-login-main">
					<div class="layadmin-user-login-box layadmin-user-login-body layui-form" lay-filter="formTest">
						<div class="layui-container">
							<div class="layui-row">
								<div class="layui-col-xs6">
									<br><br><br>
									<div class="layui-form-item">
										<label class="layui-form-label">任务名:<span style="color:red">*</span></label>
										<div class="layui-input-block">
											<input id="taskName" type="text" name="taskName" lay-verify="required" autocomplete="off" placeholder="请输入任务名称" class="layui-input">
										</div>
									</div>
									<br>
									<div class="layui-form-item">
										<div class="layui-input-block" id="res">
										<button id="testListAction" class="layui-btn" lay-submit lay-filter="formDemo" >添加任务</button>
										<button type="reset"  lay-filter="formReset" onclick="updateUni();"  class="layui-btn layui-btn-primary">重置</button>
										</div>
									</div>
								</div>
								<div class="layui-col-xs6">
									<div class="layui-form-item">
										<div>
											<label class="layui-form-label file_upload">任务代码:<span style="color:red">*</span></label>
											<button type="button" class="layui-btn file_upload" id="test1">
												<i class="layui-icon">&#xe67c;</i>上传
											</button>
										</div>
										<span id="upfile_name1" class="layui-inline layui-upload-choose file_upload upfile_name"></span>
									</div>
									<div class="layui-form-item">
										<div>
											<label class="layui-form-label file_upload">任务代码的依赖项:</label>
											<button type="button" class="layui-btn file_upload" id="test4">
												<i class="layui-icon">&#xe67c;</i>上传
											</button>
										</div>
										<span id="upfile_name4" class="layui-inline layui-upload-choose file_upload upfile_name"></span>
									</div>
									<div class="layui-form-item">
										<div>
											<label class="layui-form-label file_upload">数据文件:<span style="color:red">*</span></label>
											<button type="button" class="layui-btn file_upload" id="test2">
												<i class="layui-icon">&#xe67c;</i>上传
											</button>
										</div>
										<span id="upfile_name2" class="layui-inline layui-upload-choose file_upload upfile_name"></span>
									</div>
									<div class="layui-form-item">
										<div>
											<label class="layui-form-label file_upload">参数文件:<span style="color:red">*</span></label>
											<button type="button" class="layui-btn file_upload" id="test3">
												<i class="layui-icon">&#xe67c;</i>上传
											</button>
										</div>
										<span id="upfile_name3" class="layui-inline layui-upload-choose file_upload upfile_name"></span>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>


		<fieldset class="layui-elem-field layui-field-title" style="margin-top: 30px;">
			<legend>控制面板</legend>
		</fieldset>
		<div class="layui-row">
			<div class="layui-col-xs6" style="padding: 0px 3%;">
				
				<table class="layui-table server-status"  lay-skin="line">
					<colgroup>
						<col width="100">
						<col >
						<col width="80">
					</colgroup>
					<thead>
						<tr>
						<th>服务器</th>
						<th>状态</th>
						<th>操作</th>
						</tr> 
					</thead>
					<tbody>
						<tr>
							<td>Master</td>
							<td id="master_status">离线<i class="layui-icon layui-icon-circle-dot" style="margin-left: 3px; font-size: 12px; color: #d2d2d2;"></i></td>
							<td id="master_active"><button id="start_server" onclick="start_server(1);" type="button" class="layui-btn layui-btn-sm layui-btn-normal layui-btn-radius">启动</button><button id="stop_server" onclick="start_server(0);" type="button" style="display: none;" class="layui-btn layui-btn-sm layui-btn-normal layui-btn-radius">停止</button></td>
							
						</tr>
					</tbody>
				</table>
				<br>
				<table class="layui-table server-status"  lay-skin="line">
					<colgroup>
						<col width="100">
						<col width="80">
						<col width="80">
						<col >
						<col width="80">
					</colgroup>
					<thead>
						<tr>
						<th>任务名</th>
						<td>状态</td>
						<th>已完成</th>
						<th>剩余时间</th>
						<th>操作</th>
						</tr> 
					</thead>
					<tbody>
						<tr>
							<td>暂无任务</td>
							<td></td>
							<td></td>
							<td></td>
							<td></td>
						</tr>
						<!--
						<tr>
							<td>211</td>
							<td>计算中</td>
							<td>20/100</td>
							<td>24小时33分钟</td>
							<td><button type="button" class="layui-btn layui-btn-sm layui-btn-danger layui-btn-radius">取消</button></td>
						</tr>
						-->
					</tbody>
				</table>
			</div>
			<div class="layui-col-xs6">
				<pre id="control-view" class="layui-code control-view" lay-title="Master控制台" lay-skin="notepad" lay-about="false">等待服务器上线...</pre>
			</div>
		</div>


		<fieldset class="layui-elem-field layui-field-title" style="margin-top: 30px;">
			<legend>计算结果</legend>
		</fieldset>
		<br>
		<div class="layui-row">
			<div class="layui-col-xs12" style="padding: 0px 10%;">
				<div class="excel_save">
					<table lay-filter="parse-table-demo" style="border: 1px solid #e2e2e2;">
						<thead>
							<tr>
								<th lay-data="{field:'id',width:80 ,sort: true}">ID</th>
								<th lay-data="{field:'fileName', sort: true}">文件名</th>
								<th lay-data="{field:'active',width:64}">操作</th>
							</tr>
						</thead>
						<tbody id='excel_save_tbody'>
						</tbody>
					</table>
    				<!--
					<table id="demo" lay-filter="test"></table>
					-->
				</div>
			</div>
		</div>
		<br>
		<br>
	</div>





</body>

<!-- 载入layui JS -->
<script src="<?php echo base_url('/limit/core/layui/layui.js');?>"></script>
<!-- 载入jquery -->
<!-- 
<script src="https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
-->
<script src="<?php echo base_url('/limit/core/jquery.min.js');?>"></script>
<!-- 载入jquery cookie -->
<script src="<?php echo base_url('/limit/core/jquery.cookie.min.js');?>"></script>
<!-- 载入md5插件 -->
<script src="<?php echo base_url('/limit/core/')."md5.js";?>"></script>
<!-- 载入LimitControl控制模块 -->
<script src="<?php echo base_url('/limit/core/')."LimitControl.js";?>"></script>
<!-- 模块组入口 -->
<script>
	//载入layer模块
	layui.use('layer', function(){});
    layui.use('element', function(){});
	//设置网站域名
	LimitControl.setHostName("<?php echo $host_url;?>");
	//设置Limit框架目录路径
	LimitControl.setStaticHost("<?php echo $CDN_url;?>");
</script>
<!-- 载入页面脚本 -->
<script src="<?php echo base_url('/limit/js/').$pageName.'.js';?>"></script>
</html>
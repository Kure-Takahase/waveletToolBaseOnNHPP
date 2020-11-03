<html style="overflow: hidden;">
<head>
	<meta charset="UTF-8">
	<title><?php echo $title; ?></title>
	<link rel="shortcut icon" href="<?php echo base_url('/limit/img/'.$shortcutIcon);?>" />
	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
	<!-- 载入layui CSS -->
	<link rel="stylesheet" href="<?php echo base_url('/limit/core/layui/css/layui.css');?>"  media="all">
	<link rel="stylesheet" href="<?php echo base_url('/limit/css/'.$pageName.'.css');?>"  media="all">
</head>

<body id="body" style="position:relative; overflow: hidden;">
	<ul class="layui-nav" lay-filter="">
		<li class="layui-nav-item layui-this"><a href="<?php echo site_url('welcome\index\waveletShrinkageEstimationTool');?>">小波收缩工具</a></li>
		<li class="layui-nav-item"><a href="<?php echo site_url('welcome\index\pythonDistributedComputing');?>">Python分布式计算平台</a></li>
	</ul>
 

	<!-- 登录页 -->
	<div class="login_shade_div">
		<!-- 登录内容 -->
		<div class="layadmin-user-login layadmin-user-display-show" id="LAY-user-login" style="display: none;">
			<div class="layadmin-user-login-main">
				<div class="layadmin-user-login-box layadmin-user-login-header">
					<h2>Waveletデノイズツール</h2>
					<p>作者：Wu JingChi</p>
				</div>
				<div class="layadmin-user-login-box layadmin-user-login-body layui-form" lay-filter="formTest">
					<div class="layui-form-item">
						<label class="layui-form-label">データセット</label>
						<button type="button" class="layui-btn" id="test1">
							<i class="layui-icon">&#xe67c;</i>アップロード
						</button>
					</div>
					<div class="layui-form-item">
						<label class="layui-form-label">データ変換</label>
						<div class="layui-input-block">
							<input type="radio" name="dataTransform" value="Anscombe" title="Anscombe" checked/>
							<input type="radio" name="dataTransform" value="Fisz" title="Fisz"/>
							<input type="radio" name="dataTransform" value="Bartlett" title="Bartlett"/>
						</div>
					</div>
					<div class="layui-form-item">
						<label class="layui-form-label">閾値ルール</label>
						<div class="layui-input-block">
							<input type="radio" name="thresholdRule" value="s" title="Soft" checked/>
							<input type="radio" name="thresholdRule" value="h" title="Hard"/>
						</div>
					</div>
					<div class="layui-form-item">
						<label class="layui-form-label">閾値方法</label>
						<div class="layui-input-block">
							<input type="radio" name="thresholdMethod" value="ut" title="Universal" checked/>
							<input type="radio" name="thresholdMethod" value="lht" title="Leave-out-half Cross-Validation"/>
						</div>
					</div>
					<div class="layui-form-item">
						<label class="layui-form-label">全組み合わせ</label>
						<div class="layui-input-block">
							<input type="checkbox" name="mode" lay-skin="switch">
						</div>
					</div>
					<div class="layui-form-item">
						<div class="layui-input-block" id="res">
						<button id="testListAction" class="layui-btn" lay-submit lay-filter="formDemo" >計算する</button>
						<button type="reset" class="layui-btn layui-btn-primary">リセット</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</body>

<!-- 载入layui JS -->
<script src="<?php echo base_url('/limit/core/layui/layui.js');?>"></script>
<!-- 载入jquery -->
<script src="https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
<!-- 载入jquery cookie -->
<script src="https://cdn.bootcss.com/jquery-cookie/1.4.1/jquery.cookie.min.js"></script>
<!-- 载入md5插件 -->
<script src="<?php echo base_url('/limit/core/')."md5.js";?>"></script>
<!-- 载入LimitControl控制模块 -->
<script src="<?php echo base_url('/limit/core/')."LimitControl.js";?>"></script>
<!-- 载入页面脚本 -->
<script src="<?php echo base_url('/limit/js/').$pageName.'.js';?>"></script>
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
</html>
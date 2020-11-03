function module_host_page() 
{
	
}
function host_page() 
{

	layui.use('form', function(){
	  var form = layui.form;
	  //监听提交
	  form.on('submit(host_page)', function(data){
	    layer.msg(JSON.stringify(data.field));
	    host_page_post(data);
	    return false;
	  });
	  form.render();
	});

	/*
	layui.use('form', function(){
	var form = layui.form;
	//监听提交
	form.on('submit(host_page)', function(data)
	{
		console.log("ok");
		console.log(data.field);
		layer.msg(JSON.stringify(data.field));
		
		var url = LimitControl.hostName() + 'Volunteer/post';
		var data_arr =
		{
			email 						: $.cookie('yourEmail'),
			password 					: $.cookie('yourPassword'),
			name 						: data.field['name']
			age 						: data.field['age'],
			sex 						: data.field['sex'],
			country 					: data.field['country'],
			province 					: data.field['province'],
			city 						: data.field['city'],
			drink_prefer				: data.field['drink_prefer'],
			eat_prefer 					: data.field['eat_prefer'],
			is_smoke 					: data.field['is_smoke'],
			is_cat 						: data.field['is_cat'],
			is_dog 						: data.field['is_dog'],
			is_handmade_article_room	: data.field['is_handmade_article_room'],
			is_animal_husbandry 		: data.field['is_animal_husbandry'],
			is_farming_tree 			: data.field['is_farming_tree'],
			is_farming_vegetable 		: data.field['is_farming_vegetable'],
			is_farming_rice 			: data.field['is_farming_rice'],
			is_restaurant 				: data.field['is_restaurant'],
			is_home_stay 				: data.field['is_home_stay'],
			introduction 				: data.field['introduction']
		}
		console.log(data_arr);
		function success_host_page(data) 
		{
			console.log(data);
		}
		function fail_host_page(e) 
		{
			console.log(e.responseText);
		}
		LimitControl.sendAjax(url,data_arr,success_host_page,fail_host_page);
		
		return false;
	});
	form.render();
	});*/
}
function destruct_host_page() 
{
	
}

function host_page_post(data) 
{
	var url = LimitControl.hostName() + 'Volunteer/post';
	var data_arr =
	{
		email 						: $.cookie('yourEmail'),
		password 					: $.cookie('yourPassword'),
		name 						: data.field['name'],
		age 						: data.field['age'],
		sex 						: data.field['sex'],
		country 					: data.field['country'],
		province 					: data.field['province'],
		city 						: data.field['city'],
		drink_prefer				: data.field['drink_prefer'],
		eat_prefer 					: data.field['eat_prefer'],
		is_smoke 					: data.field['is_smoke'],
		is_cat 						: data.field['is_cat'],
		is_dog 						: data.field['is_dog'],
		is_handmade_article_room	: data.field['is_handmade_article_room'],
		is_animal_husbandry 		: data.field['is_animal_husbandry'],
		is_farming_tree 			: data.field['is_farming_tree'],
		is_farming_vegetable 		: data.field['is_farming_vegetable'],
		is_farming_rice 			: data.field['is_farming_rice'],
		is_restaurant 				: data.field['is_restaurant'],
		is_home_stay 				: data.field['is_home_stay'],
		introduction 				: data.field['introduction']
	}
	console.log(data_arr);
	function success_host_page(data) 
	{
		console.log(data);
	}
	function fail_host_page(e) 
	{
		console.log(e.responseText);
	}
	LimitControl.sendAjax(url,data_arr,success_host_page,fail_host_page);
}

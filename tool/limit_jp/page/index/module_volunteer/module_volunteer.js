function module_volunteer() 
{
	
}
function volunteer() 
{
	loadHostList();
}
function destruct_volunteer() 
{
	
}
function loadHostList() 
{
	var url = LimitControl.hostName() + 'Volunteer/getTie';
	var data = 
	{
		sum : 10
	}
	function success_loadHostList(data) 
	{
		data = JSON.parse( data );
		console.log(data);
		for(var i=0; i< data['data'].length;i++)
		{
			addHost(data['data'][i]);
		}
	}
	function fail_loadHostList(e) 
	{
		console.log(e);
	}
	LimitControl.sendAjax(url,data,success_loadHostList,fail_loadHostList);
}
function addHost(host) 
{
	console.log("addHost ok");
	var HTML = "";
	HTML += "<div class='layui-row volunteer_row_div' onclick = 'showPostVolunteer(event,this)' email = '"+host['email']+"'>";
	    HTML += "<div class='layui-col-xs3'>";
	    	if(host['country'] == '1')
		    	HTML += "<p>中国</p>";
		    else
		    	HTML += "<p>日本</p>";
		    HTML += "<p>"+host['province']+"</p>";
		    HTML += "<p>"+host['city']+"</p>";
	    HTML += "</div>";
	    HTML += "<div class='layui-col-xs2'>";
	    	HTML += "<p>"+host['hostName']+"</p>";
	    	HTML += "<p>"+host['age']+"</p>";
	    HTML += "</div>";
	    HTML += "<div class='layui-col-xs4'>";
	    	HTML += "<p>"+host['introduction']+"</p>";
	    HTML += "</div>";
	    HTML += "<div class='layui-col-xs3'>";
	    	if(host['is_farming_rice'] == 'on')
	    		HTML += "<p>農業(米为主)</p>";
	    	if(host['is_farming_tree'] == 'on')
	    		HTML += "<p>農業(果树为主)</p>";
	    	if(host['is_farming_vegetable'] == 'on')
	    		HTML += "<p>農業(蔬菜为主)</p>";
	    	if(host['is_handmade_article_room'] == 'on')
	    		HTML += "<p>手工艺品工坊</p>";
	    	if(host['is_home_stay'] == 'on')
	    		HTML += "<p>民宿</p>";
	    	if(host['is_restaurant'] == 'on')
	    		HTML += "<p>餐厅</p>";
	    HTML += "</div>";
	HTML += "</div>";
	$(".volunteer_list_div").append(HTML);
}

function showPostVolunteer(event,elm)
{
	var email = elm.getAttribute("email");
	LimitControl.loadPage('postVolunteerApply','none');
	LimitControl.moduleObject("postVolunteerApply","volunteer_apply").setHostEmail(email);
}

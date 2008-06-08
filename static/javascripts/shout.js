function confirmDelete(url){
	if(confirm("你确定要删除这条消息吗 ?")){
		location = url;
	}
}

function checkForm(){
	var title = document.getElementById("title");
	if(title.value==""){
		alert("The title value is null!");
		return false;
	}
}

function getHtml(){
	alert(navigator.userAgent);
}

function checkReply(){
	var content = document.getElementById("content").value;
	if(content==""){
		alert("The Content of the Reply is Null!");
		return false;
	}
}
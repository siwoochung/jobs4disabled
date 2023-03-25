
var isShow = false
function textShow(){
	if (isShow == false){
		document.getElementById('btn-sample').innerHTML="Hide";
		document.getElementById('sample').innerHTML='Hello,World!';
		isShow = true
	}else if(isShow == true){
		document.getElementById('btn-sample').innerHTML="Show";
		document.getElementById('sample').innerHTML='';
		isShow = false;
	}

}
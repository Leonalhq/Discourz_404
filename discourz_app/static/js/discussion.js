function toggleNav() {
	var x = document.getElementById("mySidenav").style.width;
	var elements = document.querySelectorAll('.sidebar-text');
	var content = document.querySelectorAll('.content2');

	if (x !== "160px") {
		document.getElementById("mySidenav").style.width = "160px";
		for(var i=0; i<elements.length; i++) {
    		elements[i].style.color = "#818181";
		}
		content[0].style.left = "160px";
	}
	else {
		document.getElementById("mySidenav").style.width = "45px";
		for(var i=0; i<elements.length; i++) {
    		elements[i].style.color = "#111";
		}
		content[0].style.left = "45px";
	}
         
}

$(document).ready(function() {
	resizeContent2();

    $(window).resize(function() {
        resizeContent2();
    });
});

	
function resizeContent2() {
    var height = $(window).height();
	$('.left-chat').css('height', (height - 138) + 'px');
	$('.right-header-contentChat').css('height', (height - 209) + 'px');
}
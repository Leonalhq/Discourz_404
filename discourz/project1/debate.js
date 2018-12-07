



$(document).ready(function(){

	countdown();
	resizeContent2();

    $(window).resize(function() {
        resizeContent2();
    });
});

	
function resizeContent2() {
	var width = $(window).width();
	var sidebarWidth = $('#mySidenav').width();
	$('.content').css('width', (width - sidebarWidth) + 'px');

	var height = $(window).height();
	
	$('.right-header-contentChat').css('height', (height - 206) + 'px');
}

function toggleNav2() {
	var width = $(window).width();
	var x = $('#mySidenav');
	var elements = $('.sidebar-text');
	var content = $('.content');


	if (x.width() !== 160) {
		x.css('width', '160px');
		elements.css('color', '#818181');
		content.css('left', '160px');
		content.css('width', (width - 160) + 'px');
	}
	else {
		x.css('width', '45px');
		elements.css('color', '#111');
		content.css('left', '45px');
		content.css('width', (width - 45) + 'px');
	}
}

function countdown() {
	var timer2 = "5:01";
	var interval = setInterval(function() {


  	var timer = timer2.split(':');
  	//by parsing integer, I avoid all extra string processing
  	var minutes = parseInt(timer[0], 10);
  	var seconds = parseInt(timer[1], 10);
  	--seconds;
  	minutes = (seconds < 0) ? --minutes : minutes;
  	if (minutes < 0) clearInterval(interval);
  	seconds = (seconds < 0) ? 59 : seconds;
  	seconds = (seconds < 10) ? '0' + seconds : seconds;
  	//minutes = (minutes < 10) ?  minutes : minutes;
  	$('.countdown').text(minutes + ':' + seconds);
  	timer2 = minutes + ':' + seconds;
	}, 1000);
}

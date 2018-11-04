$(document).ready(function(){

    $('[data-toggle="tooltip"]').tooltip();   
    resizeContent();

    $(window).resize(function() {
        resizeContent();
    });

    let path = window.location.pathname;
    let page = path.split("/")[2];

    console.log(path);
    console.log(page);

    page = page.split(".")[0];
    page = page.split("_")[0];
    
    console.log( page );
    

    switch (page) {
        case "": $('.sidebar a').eq(0).css('color', 'white'); break;
        case "discussion": $('.sidebar a').eq(1).css('color', 'white'); break;
        case "debate": $('.sidebar a').eq(2).css('color', 'white'); break;
		case "poll": $('.sidebar a').eq(3).css('color', 'white'); break;
    }
    
    
    passingToggleStatus();
    getToggleStatus();
});

	
function resizeContent() {
	var width = $(window).width();
	var sidebarWidth = $('#mySidenav').width();
	$('.content').css('width', (width - sidebarWidth) + 'px');
}

function toggleNav2() {
	let width = $(window).width();
	let x = $('#mySidenav');
	let elements = $('.sidebar-text');
	let content = $('.content');


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

function getToggleStatus() {
    let query = window.location.search.substring(1);
    query = query.split("=")[1];
    console.log(query);
    if (query === 'off') {
        toggleNav2();
    }
}

function passingToggleStatus () {
    
    $('.external_link').click(function () {
        
        let text = "";
        let current = $(this).attr('seq');
        //current = current.substr(0, current.length - 1);
        console.log(current + " 1");
        if ($('#mySidenav').width() === 160) {
            text = 'on';
        }
        else {
            text = 'off';
        }

        // if (current === "/discourz/") {
        //     console.log("in");
        //     current = current.substr(0, current.length - 1);
        // }
        window.location.href = current + "?cal=" + text;
    });
}
// Setting title of the page
let title = $('#selected').text();
$('title').text(title);

// For not developing border around buttons on click
let styles_button = {
	"text-decoration": "none",
	"color": "#192231",
	"outline": "none",
}
$('button').click(function() {
	$(this).css(styles_button)
});

if(title === 'Profile') {
	$('button').first().click(function() {
		$(this).parent().attr('class', 'not-show');
		$('.container > div').last().attr('class', 'show');
	});
	$('button[type=button]').click(function() {
		// Clearing passwords
		$('input').val("");
		$('button').first().parent().attr('class', 'show');
		$('.container > div').last().attr('class', 'not-show');
	});
	// make sure current and new passwords are not same
	$('button[type=submit]').click(function() {
		let old = $('input')[0].value;
		let new_ = $('input')[1].value;
		if(old === new_ && old != "") {
			alert('Please choose a new password');
			return false;
		}
		return true;
	});
}

// Timeline Logic
if(title === 'Timeline') {
	// months
	let months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
	// today's date
	let today = new Date();
	let cur_date = today.getDate();
	let cur_month = today.getMonth();
	let cur_year = today.getFullYear();
	let today_date_obj = new Date(cur_year, cur_month, cur_date);
	// logic for marking completed events with blue
	let lis = $('.box ul li');
	for(li of lis) {
		let mentioned = li.children[2].innerText.split("\n");
		let mentioned_date = mentioned[0];
		let mentioned_month = months.indexOf(mentioned[1]);
		let mentioned_date_obj = new Date(cur_year, mentioned_month, mentioned_date);
		if(today_date_obj > mentioned_date_obj) {
			li.children[0].removeAttribute('class');
			li.children[0].setAttribute('class', 'over');
		}
	}
	if(lis[1].innerText.split("\n")[0] === "Team Formation completed") {
		lis[1].children[0].removeAttribute('class');
		lis[1].children[0].setAttribute('class', 'over');
	}
	if(lis[2].innerText.split("\n")[0] === "Assignment Submission recorded") {
		lis[2].children[0].removeAttribute('class');
		lis[2].children[0].setAttribute('class', 'over');
	}
	if(lis[5].innerText.split("\n")[0] === "Project Week begins" || lis[5].innerText.split("\n")[0] === "Sorry to hear you discontinue") {
		lis[5].children[0].removeAttribute('class');
		lis[5].children[0].setAttribute('class', 'over');
	}
}

if(title === 'Forum') {
	$('.query').parent().last().css('border', 'none');
	$('button').last().click(function() {
		let divs = $('.container div');
		divs[0].removeAttribute('class'); divs[0].setAttribute('class', 'show');
		divs[1].removeAttribute('class'); divs[1].setAttribute('class', 'not-show');
	});
	function cancel() {
		// Clearing the existing text
		$('textarea').val("");
		let divs = $('.container div');
		divs[0].removeAttribute('class'); divs[0].setAttribute('class', 'not-show');
		divs[1].removeAttribute('class'); divs[1].setAttribute('class', 'show');
	}
}
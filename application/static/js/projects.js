var MY_FUNCS = {};

MY_FUNCS.refreshStatusBars = function() {
	$('.status-bar-fill').each(function(index) {
		// get data from element
		var complete = Number($(this).attr('data-complete'));
		var goal = Number($(this).attr('data-goal'));

		// calculate % of time goal complete, cap at 100
		var percent_done = Math.floor(complete / goal * 100);
		var width = Math.min(percent_done, 100);
		var width = String(width) + '%';

		// set width of element
		$(this).animate({'width': width});
	})
};

$(window).load(MY_FUNCS.refreshStatusBars);
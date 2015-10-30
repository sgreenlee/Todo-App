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

MY_FUNCS.submitTaskComplete = function(event) {
	var btn = $(event.target);
	var id = btn.attr('data-id');
	$.ajax(url='/tasks', {
		'data-type': 'json',
		'method': 'post',
		'data': {'complete': id}
	}).done(function(data){
		if (data.success){
			var id = data.success;
			$('.task[data-id=' + id + ']').fadeOut();
		}
	});
};

MY_FUNCS.submitAddTime = function(event) {
	var $target = $(event.target);
	var data = {};
	var fields = $target.serializeArray();
	
	fields.forEach(function(element, index, array) {
		var name = element['name'];
		var value = element['value'];
		data[name] = value;
	});

	console.log(data);

	$.ajax(url="/projects/contribute", settings={
		'data': data,
		'method': 'post',
		'data-type': 'json'
	}).done(function(data){
		if (data.status === 'success'){
			var id = data.id;
			var bar = $('.status-bar-fill[data-id=' + id +']');
			var complete = Number(bar.attr('data-complete'));
			complete += Number(data.time);
			bar.attr('data-complete', complete);
			MY_FUNCS.refreshStatusBars();

			$('.completed-text[data-id=' + id + ']').text(complete);
		}
	});

	$target.find('input[type=number]').val('');
};

$('.complete-task-btn').on('click', function(event) {
	event.preventDefault();
	MY_FUNCS.submitTaskComplete(event);
});

$('.add-time-form').on('submit', function(event) {
	event.preventDefault();
	MY_FUNCS.submitAddTime(event);
});

$(window).load(MY_FUNCS.refreshStatusBars);
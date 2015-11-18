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
		'dataType': 'json',
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

			$('.completed-text[data-id=' + 	id + ']').text(complete);
		}
	});

	$target.find('input[type=number]').val('');
};

$('.complete-task-form').on('submit', function(event) {
	event.preventDefault();
	// submit form data
	$.post("/tasks", $(this).serialize()).done(function(data){
		// fade task out on success
		if (data.success){
			var id = data.success;
			$('.task[data-id=' + id + ']').fadeOut();
		}
	});
});

$('.add-time-form').on('submit', function(event) {
	event.preventDefault();
	MY_FUNCS.submitAddTime(event);
});

$(window).load(MY_FUNCS.refreshStatusBars);


// set up event handlers for tabbed navigation in modules
$('.module-nav .tab a').on('click', function (event) {
	//
	event.preventDefault();
	var $this = $(event.target);
	var $newTab = $this.parent();
	console.log($newTab)
	if ($newTab.hasClass('active'))
		// if clicked-on tab is already active, do nothing
		return;

	else {
		// find new content panel
		var targetId = $newTab.data('target');
		console.log(targetId)
		var $newContent = $('#' + targetId);

		// find old tab and content panel
		var $oldTab = $('.module-nav li.active');
		var $oldContent = $('.module-content.active');

		// remove active classes from old tab and content
		// and add to new tab and content
		$oldTab.removeClass('active');
		$oldContent.removeClass('active');

		$newTab.addClass('active');
		$newContent.addClass('active');


	}


});
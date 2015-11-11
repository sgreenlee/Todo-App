// modal window object
var modal = (function(){

	var $window = $(window);
	var $modal = $('#modal');
	var $backdrop = $('.modal-backdrop');

	$modal.css({
		backgroundColor: 'white',
		color: '#333'
	});

	$backdrop.css({
		backgroundColor: '#666',
		opacity: 0.5,
		width: $window.width(),
		height: $window.height(),
		top: 0,
		left: 0
	});

	$backdrop.on('click', function(event){
		event.preventDefault();
		modal.close();
	});

	return {

		center : function() {
			// center the modal window

			// calculate modal position
			var top = Math.max($window.height() - $modal.outerHeight(), 0) / 2;
			var left = Math.max($window.width() - $modal.outerWidth(), 0) / 2;

			// set modal position
			$modal.css({
				top: top,
				left: left
			});

			// resize the backdrop
			$backdrop.css({
				width: $window.width(),
				height: $window.height()
			});
		},

		open: function(content){
			// open modal window with specified content

			// load modal content
			// var content = $(content);
			$modal.empty();
			$modal.append(content);	

			content.fadeIn(400);
			modal.center();

			// load backdrop
			$backdrop.fadeIn(300);
			$modal.slideDown(500);
			

			// attach event handler to center modal on window resize
			$window.on('resize', modal.center);


			var $close = $('.modal-header button.close');
			$close.on('click', function(event){
				event.preventDefault();
				modal.close();
			});
		},
	
		close : function(){
			// close modal window

			var content = $('#modal .modal-content');

			// hide modal and backdrop
			$modal.slideUp(500);
			$backdrop.fadeOut(600);

			// remove content from modal
			setTimeout(function() {
				content.hide();
				content.appendTo($('body'));
			}, 500);

			// remove event handler from window
			$window.off('resize', modal.center);
		}
	};
})();

var modalCache = {};


// attach event handlers for opening modal windows

// open new task modal
$('#add-task-link').on('click', function (event) {
	event.preventDefault();
	if (!modalCache.tasks) {
		$.get('/modals/tasks/new', success=function(data) {
			modalCache.tasks = $(data);
			modal.open(modalCache.tasks);
		});
	}
	else
		modal.open(modalCache.tasks);
	
});

// open projects modal
$('#project-modal-open').on('click', function(event) {
	event.preventDefault();
	if (!modalCache.projects) {
		$.get('/modals/projects', success=function(data) {
			modalCache.projects = $(data);
			modal.open(modalCache.projects);
		});
	}
	else
		modal.open(modalCache.projects);
});
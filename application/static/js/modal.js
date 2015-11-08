var modal = (function(){

	var $window = $(window);
	var $modal = $('#modal');
	var $backdrop = $('.modal-backdrop');

	$modal.css({
		backgroundColor: 'white',
		color: '#333'
	});

	$backdrop.css({
		backgroundColor: '#AAA',
		opacity: 0.5,
		width: $window.width(),
		height: $window.height(),
		top: 0,
		left: 0
	});

	var $close = $('.modal-header button.close');

	$close.on('click', function(event){
		event.preventDefault();
		modal.close();
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
				top: top + $window.scrollTop(),
				left: left + $window.scrollLeft()
			});

			// resize the backdrop
			$backdrop.css({
				width: $window.width(),
				height: $window.height()
			});
		},

		open: function(content_id){
			// open modal window with specified content

			// load modal content
			var content = $(content_id);
			$modal.append(content);	


			modal.center();

			// load backdrop
			$backdrop.fadeIn(300);
			$modal.slideDown(500);
			content.fadeIn(400);

			// attach event handler to center modal on window resize
			$window.on('resize', modal.center);
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
			$window.off('resize', modal.center());
		}
	};
})();


// attach event handlers for opening modal windows

// open new task modal
$('#add-task-link').on('click', function (event) {
	// body.
	event.preventDefault();
	modal.open('#modal-add-task');
});
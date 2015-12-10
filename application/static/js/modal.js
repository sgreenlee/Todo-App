// modal window object
var modal = (function(){

	var $window = $(window);
	var $modal = $('#modal');
	var $backdrop = $('.modal-backdrop');

	$modal.css({
		backgroundColor: 'white',
		color: '#333',
		maxHeight: $window.height()
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

			content.show();
			modal.center();

			// load backdrop
			$backdrop.show();
			$modal.slideDown(300);
			

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
			$modal.slideUp(300);
			setTimeout(300, $backdrop.fadeOut(100));

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

			// attach event handler for submitting new tasks
			$('#modal-task-form').on('submit', function(event) {
				event.preventDefault();
				console.log($(this).serialize());
				$.post('/modals/tasks/new', $(this).serialize(), success=function(data){
					if (data.redirect) {
						window.location.href = data.redirect;
					}
					else {
						// update form
						var $form = $(data).find('#new-task-form-inputs');
						console.log($form);
						$oldForm = modalCache.tasks.find('#new-task-form-inputs');
						$oldForm.replaceWith($form);
					}
				});
			});
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

// open delete goal modal
$('.delete-goal-link').on('click', function(event) {
	event.preventDefault();
	var id = $(this).data('id');
	$('#delete-goal-id-field').val(id);
	console.log(id);
	modal.open($('#modal-delete-goal'));
});

// open cancel project modal
$('.cancel-project-link').on('click', function(event) {
	event.preventDefault();
	var id = $(this).data('id');
	$('#cancel-project-id-field').val(id);
	modal.open($('#modal-cancel-project'));
});

// open new project modal
$('#add-project-link').on('click', function(event) {
	event.preventDefault();
	if (!modalCache.newProject) {
		$.get('/modals/projects/new', success=function(data) {
			var $data = $(data);
			modalCache.newProject = $data.find('#modal-add-project');
			var $goalForm = $data.find('.goal-form');

			modal.open(modalCache.newProject);

			// attach event handler to add new goals to form
			$('.add-goal-link').on('click', function(event){
				event.preventDefault();
				$('.goal-form-container .goals').append($goalForm.clone(true).fadeIn());
				modal.center();
			});

			// attach event handler to remove goals
			$goalForm.find('button.close').click(function(event) {
				event.preventDefault();
				$(this).parent().remove();
				modal.center();
			});

			// event handler for submitting new projects
			$('#modal-project-form').on('submit', function(event) {
				event.preventDefault();

				// get form fields
				var name = $(this).find('input[name="name"]').val();
				var description = $(this).find('input[name="description"]').val();
				var csrf_token = $(this).find('input[name="csrf_token"]').val();

				// get time goal data
				var goals = [];
				$(this).find($('li.goal-form')).each(function(){
					var $this = $(this);
					var time = $this.find('input[type="number"]').val();
					var days = [];
					$this.find('input:checked').each(function(){
						days.push($(this).val());
					});
					goals.push({
						'time' : time,
						'days' : days
					});
				});
				
				var data = {
					'csrf_token' : csrf_token,
					'name' : name,
					'description' : description,
					'goals' : JSON.stringify(goals)
				};

				$.post("/modals/projects/new", data, success=function(data, textStatus) {
					if (data.redirect) {
						window.location.href = data.redirect;
					}
					else {
						var $form = $(data).find('#new-project-form-inputs');
						console.log($form);
						$oldForm = modalCache.newProject.find('#new-project-form-inputs');
						$oldForm.replaceWith($form);
					}
				});

			});


		});
	}
	else
		modal.open(modalCache.newProject);
});
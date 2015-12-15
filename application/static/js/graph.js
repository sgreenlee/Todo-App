var graph = (function(){
	var graphData = {
    	labels: [],
    	datasets: 
    	[{
            label: "Project contributions",
            fillColor: "rgba(220,220,220,0.5)",
            strokeColor: "rgba(220,220,220,0.8)",
            highlightFill: "rgba(220,220,220,0.75)",
            highlightStroke: "rgba(220,220,220,1)",
            data: []
        }]
	};

	var ctx = document.getElementById("myChart").getContext("2d");
	var projectGraph;

	var getData = function(){
		$.get('/contributions/history', success=updateGraph);
	}

	var updateGraph = function(data){
		console.log(data);
		graphData.labels = data.labels;
		graphData.datasets[0].data = data.data;
		projectGraph = new Chart(ctx).Bar(graphData)
	}

	$(window).load(getData);

	return projectGraph;
})();


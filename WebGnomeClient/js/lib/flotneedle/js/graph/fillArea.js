$(function(){
	var dataset = generateDataSeries();

	function generateDataSeries(){
		var startTime = 1426779289;
		var timeStep = 900;
		var data = [];
		for (var i = 0; i < 97; i++){
			data.push([startTime + timeStep * i, 100 + 5 * i, 0, 100 + 2 * i, 100 + 7 * i]);
		}
		return data;
	}
});
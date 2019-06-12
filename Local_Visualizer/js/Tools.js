//Function used to filter names
function filterNames(names, filter){
	var res=[];
	for(var i =0; i < names.length;i++){
		if (names[i].includes(filter)){
			res.push(names[i]);
		}
	}
	return res;
}
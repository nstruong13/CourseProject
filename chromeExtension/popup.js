let submitButton = document.getElementById("submitButton");

submitButton.addEventListener("click", async () => {
	queryInput = document.getElementById("queryInput").value
  
  var tempText;
  var imageElement = document.createElement("img");

  queryResult = await fetch("http://localhost:105/query?query="+queryInput);
  queryResultJson = await queryResult.json();
  heatMapResult = await fetch("http://localhost:105/getHeatMapImage");
  heapMapResultBlob = await heatMapResult.blob();


  imageElement.setAttribute('src', URL.createObjectURL(heapMapResultBlob));
  document.getElementById('body').appendChild(imageElement);
  var i = 0;
  while (i < queryResultJson.html.length) {
  	document.body.insertAdjacentHTML('beforeend', queryResultJson.html[i]);
  	i = i +1;
  }
});
let submitButton = document.getElementById("submitButton");


submitButton.addEventListener("click", async () => {
	queryInput = document.getElementById("queryInput").value
  var imageElement = document.createElement("img");

  fetch("http://localhost:105/query?query="+queryInput)
  .then(res=>{ return res.json()})
  .then(text=>{
    console.log(text.html);
    var i = 0;
    while (i < text.html.length) {
    	console.log(text.html[i]);
    	document.body.insertAdjacentHTML('beforeend', text.html[i]);
    	i = i +1;
    }
  })
});
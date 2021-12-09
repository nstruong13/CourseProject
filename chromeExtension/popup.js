// Initialize butotn with users's prefered color
let submitButton = document.getElementById("submitButton");

// submitButton.addEventListener("click", async () => {
// 	queryInput = document.getElementById("queryInput").value
//   var imageElement = document.createElement("img");

//   fetch("http://localhost:105/query?query="+queryInput)
//   .then(res=>{return res.blob()})
//   .then(b=>{
//     imageElement.setAttribute('src', URL.createObjectURL(b));
//     document.getElementById('body').appendChild(imageElement)
//   })
// });


submitButton.addEventListener("click", async () => {
	queryInput = document.getElementById("queryInput").value
  var imageElement = document.createElement("img");

  fetch("http://localhost:105/query2?query="+queryInput)
  .then(res=>{ return res.text()})
  .then(text=>{
    console.log(text);
    // console.log(document.getElementById('body').innerHtml)
    document.body.insertAdjacentHTML('beforeend', text)
  })
});
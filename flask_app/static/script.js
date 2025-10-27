let add_result = document.querySelector("add-result");

document.getElementById("add-form").addEventListener("submit", function(e){
    e.preventDefault()
    document.getElementById("add-result").innerText = "Added";
})
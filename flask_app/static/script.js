document.getElementById("add-form").addEventListener("submit", async function(e){
    // stop form submission
    e.preventDefault()

    // collect all form fields
    const form = e.target;
    const data_in = new FormData(form);

    // Send manually to Flask
    const response = await fetch(form.action, {method: "POST", body: data_in});
    const data_out = await response.json();
    console.log(data_out.error);

    // Display result of form post
    document.getElementById("add-result").innerText = data_out.error;
})
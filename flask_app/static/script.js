function display_add_result(is_json, text)
{
    let element = document.getElementById("add-result");
    if (is_json)
    {
        if(element.classList.contains("alert-success"))
        {
            element.classList.remove("alert-success");
        }
        element.classList.add("alert-danger");
        element.innerText = text;
    }
    else
    {
        if(element.classList.contains("alert-danger"))
        {
            element.classList.remove("alert-danger");
        }
        element.classList.add("alert-success");
        element.innerText = text;
    }
}

function clear_input_form(form)
{
    form.elements["actor"].value = "";
    form.elements["event_action"].value = "";
    form.elements["details"].value = "";
}

var add_form = document.getElementById("add-form");

add_form.addEventListener("submit", async function(e){
    // stop form submission
    e.preventDefault()

    // collect all form fields
    const form = e.target;
    const data_in = new FormData(form);

    // Send manually to Flask and get the response
    const response = await fetch(form.action, {method: "POST", body: data_in});

    // Check if response content is JSON
    let content_type = response.headers.get("content-type");
    if(content_type && content_type.includes("application/json"))
    {
        console.log(response);
        const data_out = await response.json();
        display_add_result(true, data_out.error);
    }
    else
    {   
        display_add_result(false, "Event successfully added");
    }
    clear_input_form(add_form);
})
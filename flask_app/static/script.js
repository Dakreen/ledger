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

let add_form = document.getElementById("add-form");
let load_events = document.getElementById("load-events");
let verify_btn = document.getElementById("verify-btn");

add_form.addEventListener("submit", async function(e)
{
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

load_events.addEventListener("click", async function()
{
    // Clear the event list
    let events_body = document.getElementById("events-body");
    events_body.innerHTML = "";

    // Get data from Flask /events
    const res = await fetch("/events");
    const data = await res.json();

    // Create elements to display data
    for(item of data)
    {
        tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${item.id}</td>
            <td>${item.actor}</td>
            <td>${item.action}</td>
            <td>${item.hash}</td>
        `;
        events_body.appendChild(tr);
    }
})

verify_btn.addEventListener("click", async function()
{
    let verify_result = document.getElementById("verify-result");
    verify_result.textContent = "";
    const res = await fetch("/verify");
    const data = await res.json();
    if(data.verified)
    {
        if(data.missing_records == 0)
        {
            if(verify_result.classList.contains("alert-danger"))
            {
                verify_result.classList.remove("alert-danger");
            }
            verify_result.classList.add("alert-success");
            verify_result.textContent = "Ledger verified — no tampering.";
        }
        else
        {
            if(verify_result.classList.contains("alert-success"))
            {
                verify_result.classList.remove("alert-success");
            }
            verify_result.classList.add("alert-danger");
            verify_result.textContent = `Missing records detected: ${data.missing_records}`;
        }
    }
    else
    {
        if(verify_result.classList.contains("alert-success"))
        {
            verify_result.classList.remove("alert-success");
        }
        verify_result.classList.add("alert-danger");
        verify_result.textContent = `Tampering detected at record ID ${data.tampered_records} - Missing records detected: ${data.missing_records}`;
    }
})

$('.datepicker').datepicker({
    format: 'dd/mm/yyyy',
    autoclose: true,
    todayHighlight: true
})

var project_type = ""

function storeValue(selectedButton) {
    project_type = selectedButton
}

function update_helpers_amount(helpers_amount) {
    document.getElementById("helpers_amount").innerHTML = helpers_amount
}

function add_a_sub_job() {
    window.location.replace(`/add_job`)
}

function send_project_data() {
    document.getElementById("project_form").addEventListener("submit", function (e) {
        e.preventDefault()
        document.getElementById("helpout_title").value = ""
        document.getElementById("helpout_description").value = ""
        document.getElementById("helpers_amount").innerHTML = ""
        document.getElementById("start_date").value = ""
        document.getElementById("end_date").value = ""
    })
    let data = new FormData()

    data.append("title", document.getElementById("helpout_title").value)
    data.append("description", document.getElementById("helpout_description").value)
    data.append("type", project_type)
    data.append("helpers", document.getElementById("helpers_amount").innerHTML)
    data.append("start_date", document.getElementById("start_date").value)
    data.append("end_date", document.getElementById("end_date").value)
    fileInput = document.getElementById("project_form_file_multiple")
    for (let i = 0; i < fileInput.files.length; i++) {
        data.append("images", fileInput.files[i])
    }


    fetch("/create_project", { method: "POST", body: data })
        .then(window.location.replace(`/home_page/`))
}

function send_job_data() {
    document.getElementById("job_form").addEventListener("submit", function (e) {
        e.preventDefault()
        document.getElementById("job_title").value = ""
        document.getElementById("job_description").value = ""
        document.getElementById("job_area").value = ""
    })
    let data = new FormData()
    data.append("title", document.getElementById("job_title").value)
    data.append("description", document.getElementById("job_description").value)
    data.append("area", document.getElementById("job_area").value)
    fileInput = document.getElementById("job_form_file_multiple")
    for (let i = 0; i < fileInput.files.length; i++) {
        data.append("images", fileInput.files[i])
    }
    fetch("/create_job", { method: "POST", body: data })
        .then(response => response.text())
        .then(jsonData => {
            data = JSON.parse(jsonData)
            console.log(data.id)
            window.location.replace(`/view_post/${data.id}`)
        })
}


function open_edit() {
    document.getElementById("edit_title").style.display = "block"
    document.getElementById("edit_description").style.display = "block"
    document.getElementById("edit_submit").style.display = "block"

}

function accept_job() {
    // let user_id = document.getElementById("job_accepted").value
    job_id = document.getElementById("job_id").value
    // HARDCODED
    let user_id = 1
    dataArray = [job_id, user_id]
    fetch("/job_accepted", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: dataArray }) })
    .then(window.location.replace(`/home_page`))
}

function send_updated_data() {
    id = document.getElementById("job_id").value
    updated_title = document.getElementById("edit_title").value
    updated_description = document.getElementById("edit_description").value

    dataArray = [id, updated_title, updated_description]
    console.log(dataArray)
    fetch("/edit_post", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ edit_data: dataArray }) })
        .then(window.location.reload())
}

function delete_post_data() {
    id = document.getElementById("job_id").value
    fetch("/delete_post", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ post_id: id }) })
        .then(window.location.replace(`/home_page/`))

}


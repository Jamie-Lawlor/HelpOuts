
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

function send_form_data() {
    document.getElementById("postForm").addEventListener("submit", function (e) {
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
    fileInput = document.getElementById("formFileMultiple")
    for (let i = 0; i < fileInput.files.length; i++) {
        data.append("images", fileInput.files[i])
    }


    fetch("/create_post", { method: "POST", body: data })
    // .then(response => response.text())
    // .then(jsonData => {
    //     data = JSON.parse(jsonData)
    //     console.log(data.id)
    //     window.location.replace(`/view_post/${data.id}`)
    // })
}

function open_edit() {
    document.getElementById("edit_title").style.display = "block"
    document.getElementById("edit_description").style.display = "block"
    document.getElementById("edit_submit").style.display = "block"

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
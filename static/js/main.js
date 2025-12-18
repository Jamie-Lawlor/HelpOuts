
$('.datepicker').datepicker({
    format: 'dd/mm/yyyy',
    autoclose: true, 
    todayHighlight: true
})

function send_form_data() {
    document.getElementById("postForm").addEventListener("submit", function (e) {
        e.preventDefault()
        document.getElementById("helpout_title").value = ""
        document.getElementById("helpout_description").value = ""
        document.getElementById("helpout_area").value = ""
    })

    title = document.getElementById("helpout_title").value
    description = document.getElementById("helpout_description").value
    area = document.getElementById("helpout_area").value
    dataArray = [title, description, area]
    console.log(dataArray)

    fetch("/create_post", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ form_data: dataArray }) })
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
    document.getElementById("edit_area").style.display = "block"
    document.getElementById("edit_submit").style.display = "block"

}

function send_updated_data() {
    id = document.getElementById("job_id").value
    updated_title = document.getElementById("edit_title").value
    updated_description = document.getElementById("edit_description").value
    updated_area = document.getElementById("edit_area").value

    dataArray = [id, updated_title, updated_description, updated_area]
    console.log(dataArray)
    fetch("/edit_post", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ edit_data: dataArray }) })
        .then(window.location.reload())
}

function delete_post_data() {
    id = document.getElementById("job_id").value
    fetch("/delete_post", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ post_id: id }) })
        .then(window.location.replace(`/home_page/`))

}
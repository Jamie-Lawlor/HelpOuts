

function sendFormData() {
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

    fetch("/create_post", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ formData: dataArray }) })
        .then(response => response.text())
        .then(jsonData => {
            data = JSON.parse(jsonData)
            console.log(data.id)
            window.location.replace(`/view_post/${data.id}`)
        })
}


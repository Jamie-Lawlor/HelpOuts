document.addEventListener('DOMContentLoaded', () =>{
    
    if(window.location.pathname=="/home_page/"){
      job_container = document.getElementById("jobs-container")
    fetch("/get_jobs")
        .then(response => response.json())
        .then(responseJson => {
            dataArray = responseJson
            dataArray.forEach(job => {
            content = `<div id="jobs-section">
                <div class="row g-3">
                        <div class="col-12">
                        <a href="/view_post/${job.job_title}"
                                class="text-decoration-none">
                                <div class="card border-0 shadow-sm p-3 h-100" style="border-radius: 12px; border-left: 4px solid #85D6D6 !important;">
                                <div class="d-flex justify-content-between align-items-center">
                                        <div>
                                        <h6 class="mb-1 fw-bold text-dark">${job.job_title}</h6>
                                        </div>
                                       <span class="badge bg-success rounded-pill px-3">Available</span>
                                </div>
                                </div>
                        </a>
                        </div>
                </div>
                </div>`    
                job_container.innerHTML += content;
            });
        })  
    }
})

$('.datepicker').datepicker({
    format: 'dd/mm/yyyy',
    autoclose: true,
    todayHighlight: true
})

var project_type = ""
var job_type = ""


function storeValue(selectedButton, label) {
    project_type = selectedButton
    document.getElementById("projectTypeButton").innerText = label
}

function storeJobValue(selectedButton, label) {
    job_type = selectedButton
    document.getElementById("jobTypeButton").innerText = label
}


function update_helpers_amount(helpers_amount) {
    document.getElementById("helpers_amount").innerHTML = helpers_amount
}

function add_a_sub_job() {
    window.location.replace(`/add_job`)
}

function send_project_data() {
    let data = new FormData()
    const allowedFileTypes = ['image/png', 'image/jpeg', 'image/jpg']
    const allowedFileExtensions = ['.jpeg', '.jpg', '.png']


    data.append("title", document.getElementById("helpout_title").value)
    data.append("description", document.getElementById("helpout_description").value)
    data.append("type", project_type)
    data.append("helpers", document.getElementById("helpers_amount").innerHTML)
    data.append("start_date", document.getElementById("start_date").value)
    data.append("end_date", document.getElementById("end_date").value)
    fileInput = document.getElementById("project-upload-images")
    
    for (let i = 0; i < fileInput.files.length; i++) {
        let validFile = true
        const fileExtension = fileInput.files[i].name.slice(fileInput.files[i].name.lastIndexOf('.')).toLowerCase()
        const mimeType = fileInput.files[i].type

        if(!allowedFileExtensions.includes(fileExtension)){
            alert("File Extension is Invalid, Cannot Use:\n" + fileExtension + "\nMust Use .jpg, .jpeg pr .png")
            validFile = false
        }

        if(!allowedFileTypes.includes(mimeType)){
            alert("File MIME Type is Invalid, Cannot Use:\n" + mimeType + "\nMust Use image/png, image/jpeg or image/jpg")
            validFile = false
        }

        if(validFile){
            data.append("images", fileInput.files[i])
        }
    }
    
    fetch("/create_project", { method: "POST", body: data })
        .then(window.location.replace(`/home_page/`))
}

function send_job_data() {
    let data = new FormData()
    // const allowedFileTypes = ['image/png', 'image/jpeg', 'image/jpg']
    // const allowedFileExtensions = ['.jpeg', '.jpg', '.png']
    data.append("title", document.getElementById("job_title").value)
    data.append("description", document.getElementById("job_description").value)
    data.append("area", document.getElementById("job_area").value)
    data.append("type", job_type.toLowerCase())
    data.append("start_date", document.getElementById("start_date").value)
    data.append("end_date", document.getElementById("end_date").value)
    fileInput = document.getElementById("job_form_file_multiple")
    // for (let i = 0; i < fileInput.files.length; i++) {
    //     let validFile = true
    //     const fileExtension = fileInput.files[i].name.slice(fileInput.files[i].name.lastIndexOf('.')).toLowerCase()
    //     const mimeType = fileInput.files[i].type

    //     if(!allowedFileExtensions.includes(fileExtension)){
    //         alert("File Extension is Invalid, Cannot Use:\n" + fileExtension + "\nMust Use .jpg, .jpeg pr .png")
    //         validFile = false
    //     }

    //     if(!allowedFileTypes.includes(mimeType)){
    //         alert("File MIME Type is Invalid, Cannot Use:\n" + mimeType + "\nMust Use image/png, image/jpeg or image/jpg")
    //         validFile = false
    //     }

    //     if(validFile){
    //         data.append("images", fileInput.files[i])
    //     }
        
    // }
    data.append("project_id", document.getElementById("project_id").value)
    fetch("/create_job", { method: "POST", body: data })
        .then(response => response.text())
        .then(jsonData => {
            data = JSON.parse(jsonData)
            window.location.replace(`/view_post/${data.job_title}`)
        })
}


function open_edit() {
    document.getElementById("edit_title").style.display = "block"
    document.getElementById("edit_description").style.display = "block"
    // document.getElementById("edit_submit").style.display = "block"
    document.getElementById("edit_area").style.display = "block"
    document.getElementById("edit-job-details").style.display = "block"

    // document.getElementById("job_title_display").style.display = "none"
    // document.getElementById("job_desc_display").style.display = "none"
    // document.getElementById("job_area_display").style.display = "none"
    // document.getElementById("manage-job").style.display = "none"

    // document.getElementById("public-actions").style.display = "none"
}

function accept_job() {
    // let user_id = document.getElementById("job_accepted").value
    job_id = document.getElementById("job_id").value
    // HARDCODED
    let helper_id = sessionStorage.getItem("id")
    dataArray = [job_id, helper_id]
    fetch("/job_accepted", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: dataArray }) })
    fetch("/send_job_accepted_notification", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: dataArray }) })
    // .then(window.location.replace(`/home_page`))
}

function send_updated_data() {
    id = document.getElementById("job_id").value
    updated_title = document.getElementById("edit_title").value
    updated_description = document.getElementById("edit_description").value
    updated_area = document.getElementById("edit_area").value
    dataArray = [id, updated_title, updated_description, updated_area]
    fetch("/edit_post", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ edit_data: dataArray }) })
        .then(response => response.text())
        .then(responseText => {
            window.location.replace(`/view_post/${responseText}`)
        })
}

function delete_post_data() {
    id = document.getElementById("job_id").value
    fetch("/delete_post", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ post_id: id }) })
        .then(window.location.replace(`/home_page/`))

}
function accept_helper_job_request(job_list_id){
    fetch("/accept_helper_job_request", {method:"POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: job_list_id }) })
        .then(window.location.reload())
}

function filter_jobs(value){
    if(value !== "view_all"){
          typeArray = []
    dataArray.forEach(job =>{

        if(typeArray.length < 1){
        job_container.innerHTML ="";
        }
            if(job.short_type === value){
            typeArray.push(value)
        content = `<div id="jobs-section">
                <div class="row g-3">
                        <div class="col-12">
                        <a href="/view_post/${job.job_title}"
                                class="text-decoration-none">
                                <div class="card border-0 shadow-sm p-3 h-100" style="border-radius: 12px; border-left: 4px solid #85D6D6 !important;">
                                <div class="d-flex justify-content-between align-items-center">
                                        <div>
                                        <h6 class="mb-1 fw-bold text-dark">${job.job_title}</h6>
                                        </div>
                                       <span class="badge bg-success rounded-pill px-3">Available</span>
                                </div>
                                </div>
                        </a>
                        </div>
                </div>
                </div>`    
                job_container.innerHTML += content;
        }
        
    })
    }else{
        job_container.innerHTML ="";
        dataArray.forEach(job => {
            content = `<div id="jobs-section">
                <div class="row g-3">
                        <div class="col-12">
                        <a href="/view_post/${job.job_title}"
                                class="text-decoration-none">
                                <div class="card border-0 shadow-sm p-3 h-100" style="border-radius: 12px; border-left: 4px solid #85D6D6 !important;">
                                <div class="d-flex justify-content-between align-items-center">
                                        <div>
                                        <h6 class="mb-1 fw-bold text-dark">${job.job_title}</h6>
                                        </div>
                                       <span class="badge bg-success rounded-pill px-3">Available</span>
                                </div>
                                </div>
                        </a>
                        </div>
                </div>
                </div>`    
                job_container.innerHTML += content;
            });
    }
}

function join_community(community_id){
        fetch("/request_join_community", {method:"POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: community_id }) })

}

function join_community_request(helper_id, button_selected){
    dataArray=[helper_id, button_selected]
    fetch("/accept_join_community", {method:"POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: dataArray }) })
    .then(window.location.reload())
}


//Remove when no longer needed as test

function test_login_helper(){
        fetch("/test_login_user", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: 2 }) })
            .then(response => response.json())
            .then(data =>{
                sessionStorage.setItem("id", data[0])
                sessionStorage.setItem("profile_picture", data[1])
                window.location.replace(`/home_page/`)
            })
}
function test_login_admin(){
    
        fetch("/test_login_admin", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: 1 }) })
           .then(response => response.json())
            .then(data =>{
                sessionStorage.setItem("id", data[0])
                sessionStorage.setItem("profile_picture", data[1])
                window.location.replace(`/community_profile/Mens_Shed_Dundalk`)
            })
}

function closeSideBar(){
    document.getElementById("sideBar").classList.add("closed");
    document.getElementById("openSideBarBtn").style.display = "flex";
}

function openSideBar(){
    document.getElementById("sideBar").classList.remove("closed");
    document.getElementById("openSideBarBtn").style.display = "none";
}


// function showSection(mobileSection){
//     let projects = document.getElementById("projects-section")
//     let jobs =  document.getElementById("jobs-section")
//     let placeholder = document.getElementById("mobile-placeholder-profile")

//     if (placeholder) placeholder.style.display = "none" // hide once jobs or projects button clicked

//     if(mobileSection === "projects"){
//         document.getElementById("projects-section").classList.style.display = "flex"
//         document.getElementById("jobs-section").className.style.display = "none"
//     }else{
//         document.getElementById("projects-section").classList.style.display = "none"
//         document.getElementById("jobs-section").className.style.display = "flex"
//     }
// }



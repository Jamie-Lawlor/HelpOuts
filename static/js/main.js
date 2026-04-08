document.addEventListener('DOMContentLoaded', () =>{
    
    if(window.location.pathname=="/home_page/"){
      job_container = document.getElementById("jobs-container")
    fetch("/get_jobs")
        .then(response => response.json())
        .then(responseJson => {
            dataArray = responseJson
            if(dataArray != "SKIP"){
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
        })  
    }
    if(window.location.href.includes("/community_profile/")){
        recommended_jobs_container = document.getElementById("recommended_jobs_list")
        fetch("/get_type", {method:"GET"})
        .then(response => response.text())
        .then(user_type =>{
            if(user_type =="helper"){
                fetch("/getJobRecommendations", {method:"GET"})
                .then(response => response.json())
                .then(data =>{
                    if(data.length!=0){
                        data.forEach(recommended =>{
                        console.log(recommended)
                        content =`<div id="jobs-section" style=margin-top:10px;>
                        <div class="row g-3">
                            <div class="col-12">
                        <a href="/view_post/${recommended[1]}"
                                class="text-decoration-none">
                                <div class="card border-0 shadow-sm p-3 h-100" style="border-radius: 12px; border-left: 4px solid #85D6D6 !important;">
                                <div class="d-flex justify-content-between align-items-center">
                                        <div>
                                        <h6 class="mb-1 fw-bold text-dark">${recommended[1]}</h6>
                                        </div>
                                       <span class="badge bg-success rounded-pill px-3">Available</span>
                                </div>
                                </div>
                        </a>
                            </div>
                        </div>
                    </div>
                    </div>`
                    recommended_jobs_container.innerHTML += content;
                    })
                    } else{
                      content =`<div id="jobs-section">
                        <div class="row g-3">
                            <div class="col-12">
                            <div class="card border-0 shadow-sm p-3 h-100" style="border-radius: 12px; border-left: 4px solid #85D6D6 !important;">
                                <div class="d-flex justify-content-between align-items-center">
                                        <h6 class="mb-1 fw-bold text-dark">Looks like there are no recommended jobs available,<br><br> Please enter your skills on your profile to find the right job for you!</h6>
                                </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    `
                    recommended_jobs_container.innerHTML += content;  
                    }
                    
                })
            }

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

    // TODO Make location required, keep this statement until then
    if(selectedLat !== null && selectedLng !== null) {
        data.append("lat", selectedLat)
        data.append("lng", selectedLng)
    }




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
    openPostModal()
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

function join_community(community_id, user_id){
        fetch("/request_join_community", {method:"POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: community_id }) })
        fetch("/send_community_notification", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: user_id }) })

        openJoinModal()
}

function join_community_request(helper_id, button_selected, icon, message, helperName){
    dataArray=[helper_id, button_selected]
    fetch("/accept_join_community", {method:"POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: dataArray }) })
    .then(response => {
        if(response.ok){
            openActionModal(message, icon)
        }
    })
}

function searchJobs(){
    let userInput = document.getElementById("job-search-input").value.toLowerCase()
    let job_container = document.getElementById("jobs-container")

    job_container.innerHTML = ""

    dataArray.forEach(job =>{

      if(job.job_title.toLowerCase().includes(userInput) || job.short_type.toLowerCase().includes(userInput) || job.area.toLowerCase().includes(userInput)){

        content = `
                        <div class="col-lg-4 col-md-6 mb-4">
                        <a href="/view_post/${job.job_title}"
                                class="text-decoration-none text-dark">
                                <div class="card border-0 shadow-sm h-100 rounded-4 overflow-hidden">
                                <div class="p-3 pb-0">
                                    <img src="/static/images/park.png" class="rounded-4 w-100" style="height:100px; object-fit:cover;">
                                </div>
                                <div class="card-body pt-2">
                                    <h6 class="fw-bold mb-2">${job.job_title}</h6>

                                    <div class="d-flex align-items-center">
                                    <img src="/static/images/location_icon.svg" class="rounded-4 w-100" style="width:14px; height:14px; margin-right:6px;">
                                    <p class="text-muted mb-0">
                                    ${ job.area }
                                    </p>
                                    </div>
                                </div>                        
                                </div>
                        </a>
                </div>`    
                job_container.innerHTML += content;
        }
    })
   

    if(job_container.innerHTML === ""){
        job_container.innerHTML = `<p class="text-center mt-4 text-muted">No jobs found called"${userInput}"</p>`
    }
}

//Remove when no longer needed as test

function test_login_helper(){
        fetch("/test_login_user", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: 7 }) })
            .then(response => response.json())
            .then(data =>{
                sessionStorage.setItem("id", data[0])
                sessionStorage.setItem("profile_picture", data[1])
                window.location.replace(`/home_page/`)
            })
}
function test_login_admin(){
    
        fetch("/test_login_admin", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: 4 }) })
           .then(response => response.json())
            .then(data =>{
                sessionStorage.setItem("id", data[0])
                sessionStorage.setItem("profile_picture", data[1])
                window.location.replace(`/community_profile/${data[2]}`)
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

function edit_helper_profile(){
    document.getElementById("manage_helper_profile").style.display = "none";
    document.getElementById("edit_helper_profile_actions").style.display = "block";

    document.getElementById("availability_display").style.display = "none";
    document.getElementById("edit_availability").style.display = "block";

    document.getElementById("skills_display").style.display = "none";
    document.getElementById("edit_skills").style.display = "block";

    document.getElementById("experience_display").style.display = "none";
    document.getElementById("edit_experience").style.display = "block";
}

function remove_skill(user_skill){
   fetch("/remove_skill", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: user_skill }) })
           .then(window.location.reload()) 
}

function update_helper_profile(){
    updated_availability = document.getElementById("edit_availability").value

    updated_skills = document.getElementById("edit_skills").selectedOptions
    skillsArray = []
    for(let i =0; i< updated_skills.length; i++){
       skillsArray.push(updated_skills[i].label) 
    }

    updated_experience = document.getElementById("edit_experience").value
    dataArray = [updated_availability, skillsArray, updated_experience]
    fetch("/update_helper_profile", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: dataArray }) })
        .then(window.location.reload())
}


function openJoinModal(){
    document.getElementById("joinModal").style.display = "block"
}

function closeJoinModal(){
    document.getElementById("joinModal").style.display = "none"
}

function openActionModal(message, iconType){
    const iconContainer = document.querySelector("#actionModal .bi");
    const iconCircle = iconContainer.parentElement

    const icons = {
        'accept': `<path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425z"/>`,
        'reject': `<path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/>`
    };

    iconContainer.innerHTML = icons[iconType] || icons['accept']; 

    if (iconType === 'reject'){
        iconCircle.style.backgroundColor = "#FFCFCF"
        iconContainer.setAttribute('fill', '#F76363')
    }else{
        iconCircle.style.backgroundColor = "#D8F2E1"
        iconContainer.setAttribute('fill', '#4CED83')
    }

    document.getElementById("actionModalMessage").innerHTML = message;    
    document.getElementById("actionModal").style.display = "block";
    document.getElementById("modalContainer").style.display = "block";
}

function closeActionModal(){
    document.getElementById("actionModal").style.display = "none"
    document.getElementById("modalContainer").style.display = "none"
}

/* View Post Modal*/
function openPostModal(){
    document.getElementById("postModal").style.display = "block"
}

function closePostModal(){
    document.getElementById("postModal").style.display = "none"
}

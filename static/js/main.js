document.addEventListener('DOMContentLoaded', () =>{
    
    if(window.location.pathname=="/home_page/"){
      job_container = document.getElementById("jobs-container")
    fetch("/get_jobs")
        .then(response => response.json())
        .then(responseJson => {
            dataArray = responseJson
            if(dataArray != "SKIP"){
               dataArray.forEach(job => {
    const formattedDate = new Date(job.start_date).toLocaleDateString('en-GB', { 
        weekday: 'short', 
        month: 'short', 
        day: 'numeric' 
    });
    console.log(dataArray)

    let content = `
    <div class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4">
        <a href="/view_post/${job.job_title}" class="text-decoration-none">
            <div class="card border-0 shadow-sm rounded-4 h-100 overflow-hidden" 
                 style="transition: transform 0.3s ease; cursor: pointer;" 
                >
                
                <div class="position-relative">
                    <img src="https://helpouts-bucket.s3.eu-west-1.amazonaws.com/jobs/${job.id}/0.j" class="w-100" style="height:130px; object-fit:cover;">
                    <span class="badge position-absolute top-0 end-0 m-2 rounded-pill px-2 py-1 fw-bold" 
                          style="background-color: rgba(255, 255, 255, 0.9); color: #3d6978; font-size: 0.65rem; backdrop-filter: blur(4px);">
                        Available
                    </span>
                </div>

                <div class="card-body p-3 d-flex flex-column">
                    <h6 class="fw-bold mb-2" style="color: #212529; letter-spacing: -0.2px; line-height: 1.2;">
                        ${job.job_title}
                    </h6>

               <div class="d-flex align-items-center gap-3 mb-3">
    <div class="text-muted d-flex align-items-center" style="font-size: 0.75rem;">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="#3d6978" class="bi bi-geo-alt-fill me-1" viewBox="0 0 16 16">
            <path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10m0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6"/>
        </svg>
        <span>${job.area}</span>
    </div>

    <div class="text-muted fw-bold d-flex align-items-center" style="font-size: 0.75rem; color: #3d6978 !important;">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" class="bi bi-calendar3 me-1" viewBox="0 0 16 16">
            <path d="M14 0H2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zM1 3.857C1 3.384 1.448 3 2 3h12c.552 0 1 .384 1 .857v10.286c0 .473-.448.857-1 .857H2c-.552 0-1-.384-1-.857V3.857z"/>
            <path d="M6.5 7a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm-9 3a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm-9 3a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/>
        </svg>
        <span>${formattedDate}</span>
    </div>
</div>
                    <div class="d-flex justify-content-between align-items-center pt-2 border-top mt-auto">
                        <span class="fw-bold" style="color: #d57a44; font-size: 0.75rem;">View Post</span>
                                            </div>
                </div>
            </div>
        </a>
    </div>`;
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

function updateJobMarkerIcon() {
    console.log("UPDATING MAP ICON---" + job_type)
    let jobIconSrc = ""
    switch(job_type) {
        case "Environment":
            jobIconSrc = "/static/images/map_icons/enviornment.svg"
            break
        case "social_and_events":
            jobIconSrc = "/static/images/map_icons/socialevents.svg"
            break
        case "construction":
            jobIconSrc = "/static/images/map_icons/construction.svg"
            break
        case "general_maintenance":
            jobIconSrc = "/static/images/map_icons/general.svg"
            break
        case "safety":
            jobIconSrc = "/static/images/map_icons/safety.svg"
            break
        default:
            jobIconSrc = "/static/images/default_image.jpg"
    }
    const img = document.createElement("img")
    img.src = jobIconSrc
    img.style.width = "50px"
    img.style.height = "50px"
    return img
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
    data.append("start_date", document.getElementById("start_date").value)
    data.append("end_date", document.getElementById("end_date").value)
    fileInput = document.getElementById("project-upload-images").files
    for(let i = 0; i < fileInput.length; i++) {
        data.append("images", fileInput[i])
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
    
    fetch("/create_project", { method: "POST", body: data })
        .then(response => response.text())
        .then(responseText => {
            window.location.replace(`/community_profile/${responseText}`)
        })
        
}

var jobPostPage = ""
function send_job_data() {
    let data = new FormData()
    const jobTitle = document.getElementById("job_title").value
    // const allowedFileTypes = ['image/png', 'image/jpeg', 'image/jpg']
    // const allowedFileExtensions = ['.jpeg', '.jpg', '.png']
    data.append("title", document.getElementById("job_title").value)
    data.append("description", document.getElementById("job_description").value)
    data.append("area", document.getElementById("job_area").value)
    data.append("helpers", document.getElementById("helpers_amount").innerHTML)
    data.append("type", job_type.toLowerCase())
    data.append("start_date", document.getElementById("start_date").value)
    data.append("end_date", document.getElementById("end_date").value)
    
    fileInput = document.getElementById("job_form_file_multiple").files
    for(let i = 0; i < fileInput.length; i++) {
        data.append("images", fileInput[i])
    }





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
    console.log(data)
    fetch("/create_job", { method: "POST", body: data })
        .then(response => response.text())
        .then(jsonData => {
            data = JSON.parse(jsonData)
            // jobPostPage = `/view_post/${data.job_title}`
            // document.getElementById('display-job-name').innerText = jobTitle
            // document.getElementById("jobModal").style.display = 'block'
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

function accept_job(message, icon) {
    // let user_id = document.getElementById("job_accepted").value
    job_id = document.getElementById("job_id").value
    fetch("/job_accepted", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: job_id }) })
    .then(response => response.text())
    .then(trigger =>{
        if(trigger == "Alert triggered"){
            message = "Maximum number of requests have been submitted for this job.<br/><br/> Please contact the community about your interest to help out, or help with another job on the list!"
            icon = "reject"
            document.getElementById("requestResponse").innerHTML = "Request failed!"
            document.getElementById("closeJobModalResponse").innerHTML = "Ok"
            openActionModal(message,icon)
        }
        else if(trigger == "Request exists"){
                 message = "You already submitted a request for this job!"
            icon = "reject"
            document.getElementById("requestResponse").innerHTML = "Request failed!"
            document.getElementById("closeJobModalResponse").innerHTML = "Ok"
            openActionModal(message,icon)
        }        
        else{
            fetch("/send_job_accepted_notification", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: job_id }) })
            openActionModal(message,icon)
        }
    })
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
        .then(response => response.text())
        .then(responseText => {
            window.location.replace(`/community_profile/${responseText}`)
        })

}

function accept_helper_job_request(job_list_id, icon, message){
    console.log(job_list_id)
     fetch("/accept_helper_job_request", {method:"POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: job_list_id }) })
        .then(response=>{
            if(response.ok){
            openActionModal(message, icon)
        }
        })
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

    const formattedDate = new Date(job.start_date).toLocaleDateString('en-GB', { 
        weekday: 'short', 
        month: 'short', 
        day: 'numeric' 
    });

        content = `<div class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4">
                    <a href="/view_post/${job.job_title}" class="text-decoration-none">
                        <div class="card border-0 shadow-sm rounded-4 h-100 overflow-hidden" 
                             style="transition: transform 0.3s ease; cursor: pointer;" 
                            >
                            
                            <div class="position-relative">
                                <img src="/static/images/park.png" class="w-100" style="height:130px; object-fit:cover;">
                                <span class="badge position-absolute top-0 end-0 m-2 rounded-pill px-2 py-1 fw-bold" 
                                      style="background-color: rgba(255, 255, 255, 0.9); color: #3d6978; font-size: 0.65rem; backdrop-filter: blur(4px);">
                                    Available
                                </span>
                            </div>

                            <div class="card-body p-3 d-flex flex-column">
                                <h6 class="fw-bold mb-2 text-dark" style="letter-spacing: -0.2px; line-height: 1.2;">
                                    ${job.job_title}
                                </h6>

                                <div class="d-flex align-items-center gap-3 mb-3">
                                    <div class="text-muted d-flex align-items-center" style="font-size: 0.75rem;">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="#3d6978" class="bi bi-geo-alt-fill me-1" viewBox="0 0 16 16">
                                            <path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10m0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6"/>
                                        </svg>
                                        <span>${job.area}</span>
                                    </div>
                                    <div class="text-muted fw-bold d-flex align-items-center" style="font-size: 0.75rem; color: #3d6978 !important;">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" class="bi bi-calendar3 me-1" viewBox="0 0 16 16">
                                            <path d="M14 0H2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zM1 3.857C1 3.384 1.448 3 2 3h12c.552 0 1 .384 1 .857v10.286c0 .473-.448.857-1 .857H2c-.552 0-1-.384-1-.857V3.857z"/>
                                        </svg>
                                        <span>${formattedDate}</span>
                                    </div>
                                </div>

                                <div class="d-flex justify-content-between align-items-center pt-2 border-top mt-auto">
                                    <span class="fw-bold" style="color: #d57a44; font-size: 0.75rem;">View Post</span>
                                </div>
                            </div>
                        </div>
                    </a>
                </div>`    
                job_container.innerHTML += content;
        }
        
    })
    }else{
        job_container.innerHTML ="";
        dataArray.forEach(job => {
             const formattedDate = new Date(job.start_date).toLocaleDateString('en-GB', { 
        weekday: 'short', 
        month: 'short', 
        day: 'numeric' 
    });

            content = `<div class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4">
                <a href="/view_post/${job.job_title}" class="text-decoration-none">
                    <div class="card border-0 shadow-sm rounded-4 h-100 overflow-hidden" 
                         style="transition: transform 0.3s ease; cursor: pointer;" >
                        
                        <div class="position-relative">
                            <img src="/static/images/park.png" class="w-100" style="height:130px; object-fit:cover;">
                            <span class="badge position-absolute top-0 end-0 m-2 rounded-pill px-2 py-1 fw-bold" 
                                  style="background-color: rgba(255, 255, 255, 0.9); color: #3d6978; font-size: 0.65rem; backdrop-filter: blur(4px);">
                                Available
                            </span>
                        </div>

                        <div class="card-body p-3 d-flex flex-column">
                            <h6 class="fw-bold mb-2 text-dark">${job.job_title}</h6>
                            <div class="d-flex align-items-center gap-3 mb-3">
                                <div class="text-muted d-flex align-items-center" style="font-size: 0.75rem;">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="#3d6978" class="bi bi-geo-alt-fill me-1" viewBox="0 0 16 16"><path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10m0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6"/></svg>
                                    <span>${job.area}</span>
                                </div>
                                <div class="text-muted fw-bold d-flex align-items-center" style="font-size: 0.75rem; color: #3d6978 !important;">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" class="bi bi-calendar3 me-1" viewBox="0 0 16 16"><path d="M14 0H2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zM1 3.857C1 3.384 1.448 3 2 3h12c.552 0 1 .384 1 .857v10.286c0 .473-.448.857-1 .857H2c-.552 0-1-.384-1-.857V3.857z"/></svg>
                                    <span>${formattedDate}</span>
                                </div>
                            </div>
                            <div class="d-flex justify-content-between align-items-center pt-2 border-top mt-auto">
                                <span class="fw-bold" style="color: #d57a44; font-size: 0.75rem;">View Post</span>
                                <div class="btn btn-sm rounded-pill px-3 py-1 fw-bold text-white" style="background-color: #3d6978; font-size: 0.7rem;">Apply</div>
                            </div>
                        </div>
                    </div>
                </a>
            </div>`    
                job_container.innerHTML += content;
            });
    }
}

function join_community(community_id, user_id){
        fetch("/request_join_community", {method:"POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: community_id }) })
        .then(response => response.text())
    .then(trigger =>{
        if(trigger == "Alert triggered"){
            message = "You already submitted a request to join this community!"
            icon = "reject"
            document.getElementById("requestResponse").innerHTML = "Request failed!"
            document.getElementById("closeJobModalResponse").innerHTML = "Ok"
            openActionModal(message,icon)
        }
      
        else{
        fetch("/send_community_notification", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: user_id }) })
            openJoinModal()
        }
    })

        
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

        const formattedDate = new Date(job.start_date).toLocaleDateString('en-GB', { 
        weekday: 'short', 
        month: 'short', 
        day: 'numeric' 
    });


      if(job.job_title.toLowerCase().includes(userInput) || job.short_type.toLowerCase().includes(userInput) || job.area.toLowerCase().includes(userInput)){

        content = `
                         <div class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4">
        <a href="/view_post/${job.job_title}" class="text-decoration-none">
            <div class="card border-0 shadow-sm rounded-4 h-100 overflow-hidden" 
                 style="transition: transform 0.3s ease; cursor: pointer;" 
                >
                
                <div class="position-relative">
                    <img src="/static/images/park.png" class="w-100" style="height:130px; object-fit:cover;">
                    <span class="badge position-absolute top-0 end-0 m-2 rounded-pill px-2 py-1 fw-bold" 
                          style="background-color: rgba(255, 255, 255, 0.9); color: #3d6978; font-size: 0.65rem; backdrop-filter: blur(4px);">
                        Available
                    </span>
                </div>

                <div class="card-body p-3 d-flex flex-column">
                    <h6 class="fw-bold mb-2" style="color: #212529; letter-spacing: -0.2px; line-height: 1.2;">
                        ${job.job_title}
                    </h6>

               <div class="d-flex align-items-center gap-3 mb-3">
    <div class="text-muted d-flex align-items-center" style="font-size: 0.75rem;">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="#3d6978" class="bi bi-geo-alt-fill me-1" viewBox="0 0 16 16">
            <path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10m0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6"/>
        </svg>
        <span>${job.area}</span>
    </div>

    <div class="text-muted fw-bold d-flex align-items-center" style="font-size: 0.75rem; color: #3d6978 !important;">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" class="bi bi-calendar3 me-1" viewBox="0 0 16 16">
            <path d="M14 0H2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zM1 3.857C1 3.384 1.448 3 2 3h12c.552 0 1 .384 1 .857v10.286c0 .473-.448.857-1 .857H2c-.552 0-1-.384-1-.857V3.857z"/>
            <path d="M6.5 7a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm-9 3a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm-9 3a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/>
        </svg>
        <span>${formattedDate}</span>
    </div>
</div>
                    <div class="d-flex justify-content-between align-items-center pt-2 border-top mt-auto">
                        <span class="fw-bold" style="color: #d57a44; font-size: 0.75rem;">View Post</span>
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
                window.location.replace(`/home_page/`)
            })
}
function test_login_admin(){
    
        fetch("/test_login_admin", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ data: 5 }) })
           .then(response => response.json())
            .then(data =>{
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
    document.getElementById("cancel_helper_profile_actions").style.display = "block";

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
    window.location.reload()
}

/* View Post Modal*/
function openPostModal(){
    document.getElementById("postModal").style.display = "block"
}

function closePostModal(){
    document.getElementById("postModal").style.display = "none"
}

/* Add job modal */
function closeJobModal(){
    // document.getElementById("jobModal").style.display = "none"
    window.location.replace(jobPostPage)
}



function open_edit_project() {
    document.getElementById("edit_title").style.display = "block"
    document.getElementById("project_title_display").style.display = "none"
    document.getElementById("manage-project").style.display = "none"
    document.getElementById("edit-project-details").style.display = "block"
    document.getElementById("desc-display").style.display = "none"
    document.getElementById("edit-labels").style.display = "none"
}

function send_updated_project_data() {
    id = document.getElementById("project_id").value
    updated_title = document.getElementById("edit_title").value
    updated_description = document.getElementById("edit_description").value
    updated_helpers = document.getElementById("edit_helpers").value
    updated_start = document.getElementById("edit_project_start").value
    updated_end = document.getElementById("edit_project_end").value
    dataArray = [id, updated_title, updated_description, updated_helpers, updated_start, updated_end]
    fetch("/edit_project", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ edit_data: dataArray }) })
        .then(response => response.text())
        .then(responseText => {
            window.location.replace(`/view_project/${responseText}`)
        })
}

function delete_project_data() {
    id = document.getElementById("project_id").value
    fetch("/delete_project", { method: "POST", headers: { 'Content-Type': "application/json" }, body: JSON.stringify({ project_id: id }) })
        .then(response => response.text())
        .then(responseText => {
            window.location.replace(`/community_profile/${responseText}`)
        })
}
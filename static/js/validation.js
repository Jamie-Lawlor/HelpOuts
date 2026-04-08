// Regex Patterns
const name_regex = /^[a-zA-Z\s\-\']{2,}$/
const email_regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
const password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
const location_regex = /^(?=.*[a-zA-Z\s])[a-zA-Z\s,.]+$/
const allowedFileTypes = ['image/png', 'image/jpeg', 'image/jpg']
const allowedFileExtensions = ['.jpeg', '.jpg', '.png']

const validateStep1 = () => {

  const firstnameInput = document.getElementsByName("first_name")[0]
  const lastnameInput = document.getElementsByName("last_name")[0]
  const emailInput = document.getElementsByName("email")[0]
  const passwordInput = document.getElementsByName("password")[0]
  const confirmationInput = document.getElementsByName("confirm_password")[0]
  const firstnameError = document.getElementById("firstname_error")
  const lastnameError = document.getElementById("lastname_error")
  const emailError = document.getElementById("email_error")
  const passwordError = document.getElementById("password_error")
  const confirmationError = document.getElementById("confirmation_error")
  const emailUsedError = document.getElementById("email_taken_error")

  const firstNameValid = name_regex.test(firstnameInput.value)
  const lastNameValid = name_regex.test(lastnameInput.value)

  const emailValid = email_regex.test(emailInput.value)
  const passwordValid = password_regex.test(passwordInput.value)
  const confirmPasswordValid = confirmationInput.value === passwordInput.value && confirmationInput.value != ""

  firstnameError.style.visibility = firstNameValid ? "hidden" : "visible"
  lastnameError.style.visibility = lastNameValid ? "hidden" : "visible"
  emailError.style.visibility = emailValid ? "hidden" : "visible"
  passwordError.style.visibility = passwordValid ? "hidden" : "visible"
  confirmationError.style.visibility = confirmPasswordValid ? "hidden" : "visible"

  return(
    firstNameValid &&
    lastNameValid &&
    emailValid &&
    passwordValid &&
    confirmPasswordValid
  )
}

const validateStep2 = () => {

  const locationInput = document.getElementsByName("location")[0]
  const communityNameInput = document.getElementsByName("community_name")[0]
  const isCommunitySelected = document.getElementById("register-step-community")
  const locationError = document.getElementById("location_error")
  const communityNameError = document.getElementById("community_name_error")
  const uploadedImage = document.getElementById("project-upload-images")
  const imageError = document.getElementById("image_error")

  const locationValid = location_regex.test(locationInput.value)
  locationError.style.visibility = locationValid ? "hidden" : "visible"

  let communityNameValid = true
  const isVisible = isCommunitySelected.style.display !== "none"

  if(isVisible){
    communityNameValid = communityNameInput.value.length > 0
    communityNameError.style.visibility = communityNameValid ? "hidden" : "visible"
  }else{
    communityNameValid = true
    communityNameError.style.visibility = "hidden"
  }

  let imageValid = false

  for (let i = 0; i < uploadedImage.files.length; i++) {
      const fileExtension = uploadedImage.files[i].name.slice(uploadedImage.files[i].name.lastIndexOf('.')).toLowerCase()
      const mimeType = uploadedImage.files[i].type
      
        if(!allowedFileExtensions.includes(fileExtension)){
        imageValid = false  
        }
        else if(!allowedFileTypes.includes(mimeType)){
            imageValid = false  
        }else{
           imageValid = true  
        }
    }
  imageError.style.visibility = imageValid ? "hidden" : "visible"

  return(
    locationValid &&
    communityNameValid &&
    imageValid
  )
}
const validateStep1 = () => {
  const name_regex = /^[a-zA-Z\s\-\']{2,}$/
  const email_regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  const number_regex = /^\+\d{10,12}$/
  const password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/

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
  const numberInput = document.getElementsByName("phone")[0]
  const numberError = document.getElementById("phone_error")

  const firstNameValid = name_regex.test(firstnameInput.value)
  const lastNameValid = name_regex.test(lastnameInput.value)

  const emailValid = email_regex.test(emailInput.value)
  const passwordValid = password_regex.test(passwordInput.value)
  const confirmPasswordValid = confirmationInput.value === passwordInput.value && confirmationInput.value != ""

  const phoneValid = number_regex.test(numberInput.value)

  firstnameError.style.visibility = firstNameValid ? "hidden" : "visible"
  lastnameError.style.visibility = lastNameValid ? "hidden" : "visible"
  emailError.style.visibility = emailValid ? "hidden" : "visible"
  numberError.style.visibility = phoneValid ? "hidden" : "visible"
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

  const name_regex = /^[a-zA-Z\s\-\']{2,}$/
  const locationInput = document.getElementsByName("location")[0]
  const locationError = document.getElementById("location_error")

  const locationValid = name_regex.test(locationInput.value)

  locationError.style.visibility = locationValid ? "hidden" : "visible"

  return(
    locationValid
  )
}

const validateLogin = () => {

  const numberInput = document.getElementsByName("phone")[0]
  const numberError = document.getElementById("phone_error")

  const locationValid = name_regex.test(locationInput.value)

  locationError.style.visibility = locationValid ? "hidden" : "visible"

  return(
    phoneValid
  )
}

'use strict'

function urlB64ToUint8Array(base64String) {
  //Padding ensures the length is of the string is a multiple of 4 (required for base64decoding)
  const padding = '='.repeat((4 - base64String.length % 4) % 4)
  //Converting URL-Safe characters back to standard base64 characters
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/')

  //Decoding the string
  const rawData = window.atob(base64)
  const outputArray = new Uint8Array(rawData.length)

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i)
  }
  return outputArray
}

function updateSubscriptionOnServer(subscription, apiEndpoint) {
  // TODO: Send subscription to application server
  console.log("APIENDPOINTUPDATE: ", apiEndpoint)

  return fetch(apiEndpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      subscription_json: JSON.stringify(subscription)
    })
  })

}

function subscribeUser(swRegistration, applicationServerPublicKey, apiEndpoint) {
  console.log("APIENDPOINT: ", apiEndpoint)
  const applicationServerKey = urlB64ToUint8Array(applicationServerPublicKey)
  //Triggers the browser's permission prompt for notifications
  swRegistration.pushManager.subscribe({
    //userVisibleOnly ensures every pushed message will result in a visible notification
    userVisibleOnly: true,
    applicationServerKey: applicationServerKey
  })
  .then(function(subscription) {
    console.log('User is subscribed.')

    return updateSubscriptionOnServer(subscription, apiEndpoint)

  })
  .then(function(response) {
    if (!response.ok) {
      throw new Error('Bad status code from server.')
    }
    return response.json()
  })
  .then(function(responseData) {
    console.log(responseData)
    if (responseData.status!=="success") {
      throw new Error('Bad response from server.')
    }
  })
  .catch(function(err) {
    console.log('Failed to subscribe the user: ', err)
    console.log(err.stack)
  })
}

function registerServiceWorker(serviceWorkerUrl, applicationServerPublicKey, apiEndpoint){
  let swRegistration = null
  //Ensuring service workers are supported on browser
  if ('serviceWorker' in navigator && 'PushManager' in window) {
    console.log('Service Worker and Push is supported')

    navigator.serviceWorker.register(serviceWorkerUrl)
    .then(function(swReg) {
      console.log('Service Worker is registered', swReg)
      //Starts the subscription flow for notifications
      subscribeUser(swReg, applicationServerPublicKey, apiEndpoint)

      swRegistration = swReg
    })
    .catch(function(error) {
      console.error('Service Worker Error', error)
    })
  } else {
    console.warn('Push messaging is not supported')
  } 
  return swRegistration
}
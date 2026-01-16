'use strict'

self.addEventListener('install', function(event) {
  console.log('Service Worker installing.')
})

self.addEventListener('activate', function(event) {
  console.log('Service Worker activating.')
})

self.addEventListener('push', function(event) {
  console.log('[Service Worker] Push Received.')
  const pushData = event.data.text()
  console.log(`[Service Worker] Push received this data - "${pushData}"`)
  let data, title, body
  try {
    //Converting event data from text to JSON
    data = JSON.parse(pushData)
    title = data.title
    body = data.body
  } catch(e) {
    //If its not in JSON format, it assumes that the event data is to be used in the entire body
    title = "HelpOuts"
    body = pushData
  }
  const options = {
    body: body
  }
  console.log(title, options)

  event.waitUntil(
    self.registration.showNotification(title, options)
  )
})
// function stringToArrayBuffer(str) {
//   const buf = new ArrayBuffer(str.length * 2);
//   const bufView = new Uint8Array(buf);
//   for (let i = 0, strLen = str.length; i < strLen; i++) {
//     bufView[i] = str.charCodeAt(i);
//   }
//   return buf;
// }

function ArrayBufferToBase64(buffer){
  var binary = ''
  var bytes = new Uint8Array(buffer)
  var len = bytes.byteLength
  for(var i = 0; i < len; i++){
    binary += String.fromCharCode(bytes[i])
  }
  return window.btoa(binary)
}

document.getElementById('register-form').addEventListener('submit', async function (event) {
  //console.log("clicked")
  event.preventDefault()
  const regForm = event.target

  const key_pair = await window.crypto.subtle.generateKey(
    {
      name: "RSA-OAEP",
      modulusLength: 4096,
      publicExponent: new Uint8Array([1, 0, 1]),
      hash: "SHA-256",
    },
    true,
    ["encrypt", "decrypt"],
  );

  const public_key = key_pair.publicKey;
  const private_key = key_pair.privateKey;

  const exported_public_key = await window.crypto.subtle.exportKey(
    "spki",
    public_key
  )
  const base64_public_key = ArrayBufferToBase64(exported_public_key)
  document.getElementById('key_generation').value = base64_public_key

  const exported_private_key = await window.crypto.subtle.exportKey(
    "pkcs8",
    private_key
  )
  const base64_private_key = ArrayBufferToBase64(exported_private_key)
  localStorage.setItem("private_key", base64_private_key)

  regForm.submit()

  //   const encoded_private_key = String.fromCharCode.apply(
  //     null,
  //     new Uint8Array(exported_private_key),
  //   );
  //   const ascii_private_key = window.btoa(encoded_private_key);
  //   const base64_private_key = [
  //     "-----BEGIN PRIVATE KEY-----",
  //     ascii_private_key.replace(/(.{80})/g, "$1\n"),
  //     "-----END PRIVATE KEY-----",
  //   ].join("\n");

  //   const encoded_public_key = String.fromCharCode.apply(
  //     null,
  //     new Uint8Array(exported_public_key),
  //   );
  //   const ascii_public_key = window.btoa(encoded_public_key);
  //   const base64_public_key = [
  //     "-----BEGIN PUBLIC KEY-----",
  //     ascii_public_key.replace(/(.{80})/g, "$1\n"),
  //     "-----END PUBLIC KEY-----",
  //   ].join("\n");

  //   const public_key_PEM = base64_public_key;
  //   const public_key_string = public_key_PEM
  //     .replaceAll(/^\-+[^\-]+\-+$/gm, "")
  //     .replace(/\n/gm, "");
  //   const b64_public_decoded_string = atob(public_key_string);
  //   const spki_public_key_data = this.stringToArrayBuffer(
  //     b64_public_decoded_string,
  //   );

  //   const public_key_encrypt = await crypto.subtle.importKey(
  //     "spki",
  //     spki_public_key_data,
  //     {
  //       name: "RSA-OAEP",
  //       hash: "SHA-256",
  //     },
  //     true,
  //     ["encrypt"],
  //   );

  //   const private_key_PEM = base64_private_key;
  //   const private_key_string = private_key_PEM
  //     .replaceAll(/^\-+[^\-]+\-+$/gm, "")
  //     .replace(/\n/gm, "");
  //   const b64_private_decoded_string = atob(private_key_string);
  //   const spki_private_key_data = this.stringToArrayBuffer(
  //     b64_private_decoded_string,
  //   );

  //   const private_key_encrypt = await crypto.subtle.importKey(
  //     "pkcs8",
  //     spki_private_key_data,
  //     {
  //       name: "RSA-OAEP",
  //       hash: "SHA-256",
  //     },
  //     true,
  //     ["decrypt"],
  //   );

  //   localStorage.setItem("private_key", base64_private_key)
  //   print(base64_private_key)
  //   print(base64_public_key)
  //   fetch("/generate_keys", {
  //     headers: {
  //       "Content-Type": "application/json",
  //     },
  //     method: "POST",
  //     body: JSON.stringify({
  //       receiver_id: receiver_id,
  //       // private_key: base64_private_key,
  //       public_key: base64_public_key,
  //     })

})
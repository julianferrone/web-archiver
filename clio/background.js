function post(details) {
  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://127.0.0.1:5000/archive', false);
  xhr.setRequestHeader('Content-Type', 'application/json');
  const message = JSON.stringify({ 'url': details.url })
  console.log(`Sending message to archival server ${message}`);
  xhr.send(message);
  console.log('Request sent');
  return xhr.responseText;
}

browser.webNavigation.onCompleted.addListener(post);
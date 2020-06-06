const web_server = 'http://192.168.8.148:4000'

function turnUp() {
  const url=`${web_server}/temperature/up`;
  const request = new Request(url, {method: 'POST'});
  fetch(request)
    .then(response => {
      if (response.status === 200) {
        return response.json();
      } else {
        throw new Error('Something went wrong on api server! ' + response.status);
      }
    }).then(response => {
      let p = document.getElementById('desired');
      t = parseFloat(response.desired);
      t = t.toFixed(1);
      p.innerText = "Desired: "+t+" °F";
    }).catch(error => {
      console.log(error);
    })
}

function turnDown() {
  const url=`${web_server}/temperature/down`;
  const request = new Request(url, {method: 'POST'});
  fetch(request)
    .then(response => {
      if (response.status === 200) {
        return response.json();
      } else {
        throw new Error('Something went wrong on api server! ' + response.status);
      }
    }).then(response => {
      let p = document.getElementById('desired');
      t = parseFloat(response.desired);
      t = t.toFixed(1);
      p.innerText = "Desired: "+t+" °F";
    }).catch(error => {
      console.log(error);
    })
}

function updateDesired() {
  const url=`${web_server}/temperature/desired`;
  const request = new Request(url, {method: 'GET'});
  fetch(request)
    .then(response => {
      if (response.status === 200) {
        return response.json();
      } else {
        throw new Error('Something went wrong on api server! ' + response.status);
      }
    }).then(response => {
      let p = document.getElementById('desired');
      t = parseFloat(response.temperature)
      t = t.toFixed(1);
      p.innerText = "Desired: "+t+" °F";
    }).catch(error => {
      console.log(error);
    })
}

function updateTemp() {
  const url=`${web_server}/temperature/get`;
  const request = new Request(url, {method: 'GET'});
  fetch(request)
    .then(response => {
      if (response.status === 200) {
        return response.json();
      } else {
        throw new Error('Something went wrong on api server! ' + response.status);
      }
    }).then(response => {
      let p = document.getElementById('current');
      t = parseFloat(response.temperature)
      t = t.toFixed(1);
      p.innerText = "Current: "+t+" °F";
    }).catch(error => {
      console.log(error);
    })
}

function getTemperatureHistory(days) {
  const url=`${web_server}/temperature/history/${days}`;
  const request = new Request(url, {method: 'GET'});
  fetch(request)
    .then(response => {
      if (response.status === 200) {
        return response.json();
      } else {
        throw new Error('Something went wrong on api server! ' + response.status);
      }
    }).then(response => {
      console.log(response)
    })
}

updateTemp();
updateDesired();
setInterval(updateTemp, 30*1000);

function turnUp() {
  const Http = new XMLHttpRequest();
  const url='http://thermostat-wifi.bluezone.usu.edu:4000/temperature/up';
  Http.open("POST", url);
  Http.send();

  Http.onreadystatechange = (e) => {
    let p = document.getElementById('desired');
    t = parseFloat(Http.responseText);
    t = t.toFixed(1);
    p.innerText = "Desired: "+t+" °F";
  }
}

function turnDown() {
  const Http = new XMLHttpRequest();
  const url='http://thermostat-wifi.bluezone.usu.edu:4000/temperature/down';
  Http.open("POST", url);
  Http.send();

  Http.onreadystatechange = (e) => {
    let p = document.getElementById('desired');
    t = parseFloat(Http.responseText);
    t = t.toFixed(1);
    p.innerText = "Desired: "+t+" °F";
  }
}

function getTemp() {
  const Http = new XMLHttpRequest();
  const url='http://thermostat-wifi.bluezone.usu.edu:4000/temperature/get';
  Http.open("GET", url);
  Http.send();

  Http.onreadystatechange = (e) => {
    console.log(Http.responseText)
  }
}

function updateTemp() {
  const Http = new XMLHttpRequest();
  const url='http://thermostat-wifi.bluezone.usu.edu:4000/temperature/get';
  Http.open("GET", url);
  Http.send();

  Http.onreadystatechange = (e) => {
    let p = document.getElementById('temperature');
    t = parseFloat(Http.responseText);
    t = t.toFixed(1);
    p.innerText = "Current: "+t+" °F";
  }
}

updateTemp();
setInterval(updateTemp, 3*1000);

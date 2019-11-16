function turnUp() {
  const Http = new XMLHttpRequest();
  const url='http://thermostat-wifi.bluezone.usu.edu:4000/temperature/up';
  Http.open("POST", url);
  Http.send();

  Http.onreadystatechange = (e) => {
    console.log(Http.responseText)
  }
}

function turnDown() {
  const Http = new XMLHttpRequest();
  const url='http://thermostat-wifi.bluezone.usu.edu:4000/temperature/down';
  Http.open("POST", url);
  Http.send();

  Http.onreadystatechange = (e) => {
    console.log(Http.responseText)
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

const sendOrderButton = document.querySelector('#sendOrder')

sendOrderButton.addEventListener('click', (e) => {
    e.preventDefault()
    alert("We are currently working on this form, please accept our appologies")
})

function toggle_raspberrypi() {
  var x = document.getElementById("raspberrypi");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function toggle_raspberrypi4_bld4() {
  var x = document.getElementById("raspberrypi4_bld4");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

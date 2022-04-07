prev = localStorage.getItem("theme");
if (prev) {
	setTheme(prev);
}

var toggleLight = document.getElementById("toggle--light");
var toggleDark = document.getElementById("toggle--dark");
var toggleRust = document.getElementById("toggle--rust");

toggleLight.addEventListener("click", function(){setTheme("theme--light")});
toggleDark.addEventListener("click", function(){setTheme("theme--dark")});
toggleRust.addEventListener("click", function(){setTheme("theme--rust")});

function setTheme(t) {
	document.body.className = t;
	localStorage.setItem("theme", t);
}

function toast(a) {
	navigator.clipboard.writeText(a);
	var x = document.getElementById("snackbar");
	x.className = "show";
	setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

window.toast = toast;

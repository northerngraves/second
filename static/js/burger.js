
const navbar = document.getElementById("navbar_drop");
var toggle = "close"

var buttonlist = document.querySelectorAll('.mybutton');
buttonlist.forEach(function(auth) {
    auth.addEventListener('click', function() {
        if (toggle === "close") {
            navbar.classList.remove('h-[48px]');
            navbar.classList.add('h-screen');
            toggle = "open";
        } else {
            navbar.classList.remove('h-screen');
            navbar.classList.add('h-[48px]');
            toggle = "close";
        }
    })
})

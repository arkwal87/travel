let my_buttons = document.querySelectorAll('.nav-link')
my_buttons.forEach(button => {
    button.addEventListener("click", e => {
      document.querySelector('.nav-link.active').classList.remove("active")
      button.classList.add("active")
      document.querySelector('.tab-pane.fade.show.active').classList.remove("show", "active")
      document.querySelector('#' + button.id.slice(4,button.id.length)).classList.add("show", "active")
    })
})

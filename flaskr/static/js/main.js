document.addEventListener('DOMContentLoaded', () => {
  const navMenu = document.getElementById('navMenu')
  const navToggle = document.getElementById('navToggle')
  const navClose = document.getElementById('navClose')

  if (navToggle) {
    navToggle.addEventListener('click', () => {
      navMenu.classList.add('show-menu')
    })
  }

  if (navClose) {
    navClose.addEventListener('click', () => {
      navMenu.classList.remove('show-menu')
    })
  }
})

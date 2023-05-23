document.addEventListener('DOMContentLoaded', () => {
  const header = document.getElementById('header')
  const navMenu = document.getElementById('navMenu')
  const navToggle = document.getElementById('navToggle')
  const navClose = document.getElementById('navClose')

  if (navToggle) {
    navToggle.addEventListener('click', () => {
      header.classList.remove('scrolling-header')
      navMenu.classList.add('show-menu')
    })
  }

  if (navClose) {
    navClose.addEventListener('click', () => {
      header.classList.add('scrolling-header')
      navMenu.classList.remove('show-menu')
    })
  }

  if (header) {
    window.addEventListener('scroll', () => {
      const scroll = window.scrollY

      if (scroll) navMenu.classList.remove('show-menu')

      scroll >= 400
        ? header.classList.add('scrolling-header')
        : header.classList.remove('scrolling-header')
    })
  }
})

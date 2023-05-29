document.addEventListener('DOMContentLoaded', () => {
  const header = document.getElementById('header')
  const navMenu = document.getElementById('navMenu')
  const navToggle = document.getElementById('navToggle')
  const navClose = document.getElementById('navClose')

  const navLogo = document.querySelector('.nav__logo')
  const navBtn = document.querySelector('.nav__btn')
  const navLinks = document.querySelectorAll('.nav__link')

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

  if (header) {
    window.addEventListener('scroll', () => {
      const scroll = window.scrollY

      if (scroll) navMenu.classList.remove('show-menu')

      scroll >= 400
        ? header.classList.add('scrolling-header')
        : header.classList.remove('scrolling-header')

      if (scroll >= 400 && window.innerWidth >= 850) {
        navLogo.classList.add('scrolling-nav-logo')
        navBtn.classList.add('scrolling-nav-btn')
        navLinks.forEach((navLink) => {
          navLink.classList.add('scrolling-nav-link')
        })
      } else if (scroll >= 400 && window.innerWidth < 850) {
        navLogo.classList.add('scrolling-nav-logo')
      } else {
        navLogo.classList.remove('scrolling-nav-logo')
        navBtn.classList.remove('scrolling-nav-btn')
        navLinks.forEach((navLink) => {
          navLink.classList.remove('scrolling-nav-link')
        })
      }
    })
  }
})

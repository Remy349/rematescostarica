document.addEventListener('DOMContentLoaded', () => {
  if (localStorage.getItem('currentPage')) {
    localStorage.removeItem('currentPage')
  }

  // Nav and header
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

  // Close notifications
  const notification = document.getElementById('notification')

  if (notification) {
    const notificationBtnsClose = document.querySelectorAll(
      '.notification__close'
    )
    const notificationItems = document.querySelectorAll('.notification__item')

    notificationBtnsClose.forEach((notificationBtnClose, pos) => {
      notificationBtnClose.addEventListener('click', () => {
        notificationItems[pos].style.display = 'none'
      })
    })
  }

  // Multi step form
  const registroForm = document.getElementById('registroForm')
  const btnsPrev = document.querySelectorAll('.registro__btn-prev')
  const btnsNext = document.querySelectorAll('.registro__btn-next')
  const registroStep = document.querySelectorAll('.registro__info-step')

  if (registroForm) {
    btnsPrev.forEach((btnPrev, pos) => {
      let position = pos
      let operation = position * -100

      btnPrev.addEventListener('click', () => {
        registroForm.style.marginLeft = `${operation}%`
        registroStep[pos + 1].classList.remove('current-step')
      })
    })

    btnsNext.forEach((btnNext, pos) => {
      let position = pos + 1
      let operation = position * -100

      btnNext.addEventListener('click', () => {
        registroForm.style.marginLeft = `${operation}%`
        registroStep[pos + 1].classList.add('current-step')
      })
    })
  }
})

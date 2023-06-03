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
    // ======================>
    registroForm.addEventListener('submit', () => {
      let courseName = ''
      let coursePrice = ''

      const registroPriceCards = document.querySelectorAll(
        '.registro__form-prices_card'
      )

      registroPriceCards.forEach((registroPriceCard) => {
        if (registroPriceCard.classList[1] === 'current-price') {
          courseName =
            registroPriceCard.lastElementChild.firstElementChild.outerText
          coursePrice =
            registroPriceCard.lastElementChild.lastElementChild.outerText
        }
      })

      coursePrice = coursePrice.substring(1)
      coursePrice = coursePrice.replace(',', '')

      const registroPaymentData = {
        coursePrice,
        courseName,
      }

      localStorage.setItem('registroPaymentData', registroPaymentData)
    })

    // ======================>
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

    // ======================>
    const registroPricingCardOne = document.getElementById(
      'registroPricingCardOne'
    )
    const registroPricingCardTwo = document.getElementById(
      'registroPricingCardTwo'
    )

    if (registroPricingCardOne && registroPricingCardTwo) {
      registroPricingCardOne.addEventListener('click', () => {
        registroPricingCardOne.classList.add('current-price')
        registroPricingCardTwo.classList.remove('current-price')
      })

      registroPricingCardTwo.addEventListener('click', () => {
        registroPricingCardOne.classList.remove('current-price')
        registroPricingCardTwo.classList.add('current-price')
      })
    }

    // ======================>
    const registroFormSummary = document.getElementById('registroFormSummary')

    btnsNext[0].addEventListener('click', () => {
      const firstname = document.getElementById('firstname').value
      const firstLastname = document.getElementById('first_lastname').value
      const secondLastname = document.getElementById('second_lastname').value
      const email = document.getElementById('email').value
      const phonenumber = document.getElementById('phone_number').value

      registroFormSummary.innerHTML = `
        <div>
          <h2 class="registro__form-summary_subtitle">Información del estudiante</h2>
          <p class="registro__form-summary_text">
            <span>Nombre completo</span>: ${firstname} ${firstLastname} ${secondLastname}
          </p>
          <p class="registro__form-summary_text">
            <span>Correo</span>: ${email}
          </p>
          <p class="registro__form-summary_text">
            <span>Teléfono</span>: ${phonenumber}
          </p>
        </div>
        <div>
          <h2 class="registro__form-summary_subtitle">Información del curso</h2>
          <div class="registro__form-summary_price" id='registroFormSummaryCourse'></div>
        </div>
      `
    })

    btnsNext[1].addEventListener('click', () => {
      const registroPriceCards = document.querySelectorAll(
        '.registro__form-prices_card'
      )
      let courseName = ''
      let coursePrice = ''

      registroPriceCards.forEach((registroPriceCard) => {
        if (registroPriceCard.classList[1] === 'current-price') {
          courseName =
            registroPriceCard.lastElementChild.firstElementChild.outerText
          coursePrice =
            registroPriceCard.lastElementChild.lastElementChild.outerText
        }
      })

      document.getElementById('registroFormSummaryCourse').innerHTML = `
        <p class="registro__form-summary_text">
          <span>Curso elegido</span>: ${courseName}
        </p>
        <p class="registro__form-summary_text">
          <span>Precio</span>: ${coursePrice}
        </p>
      `
    })
  }
})

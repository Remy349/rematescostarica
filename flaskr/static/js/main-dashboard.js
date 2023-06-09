document.addEventListener('DOMContentLoaded', () => {
  // =======================>
  const navLinks = document.querySelectorAll('.nav__link')

  if (localStorage.getItem('currentPage') === null) {
    localStorage.setItem('currentPage', window.location.href)
  }

  navLinks.forEach((navLink) => {
    navLink.addEventListener('click', () => {
      localStorage.setItem('currentPage', navLink.href)
    })

    if (navLink.href === localStorage.getItem('currentPage')) {
      navLink.classList.add('current-page')
    }
  })

  // =======================>
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

  // =======================>
  const navDashboard = document.getElementById('navDashboard')
  const navToggleDashboard = document.getElementById('navToggleDashboard')
  const navCloseDashboard = document.getElementById('navCloseDashboard')

  if (navToggleDashboard) {
    navToggleDashboard.addEventListener('click', () => {
      navDashboard.classList.add('show-nav')
    })

    navCloseDashboard.addEventListener('click', () => {
      navDashboard.classList.remove('show-nav')
    })
  }

  // =======================>
  const adminAddUpdateUserForm = document.getElementById('adminAddUpdateUserForm')

  if (adminAddUpdateUserForm) {
    // ======================>
    const phoneNumberInput = document.getElementById('phone_number')

    const iti = window.intlTelInput(phoneNumberInput, {
      separateDialCode: true,
      initialCountry: 'auto',
      geoIpLookup: (callback) => {
        fetch('https://ipapi.co/json')
          .then((res) => res.json())
          .then((data) => callback(data.country_code))
          .catch(() => callback('us'))
      },
      utilsScript:
        'https://cdn.jsdelivr.net/npm/intl-tel-input@18.1.1/build/js/utils.js',
    })

    iti.setNumber(phoneNumberInput.value)

    phoneNumberInput.addEventListener('blur', () => {
      phoneNumberInput.value = iti.getNumber()
    })
  }
})

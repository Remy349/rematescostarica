document.addEventListener('DOMContentLoaded', () => {
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
})

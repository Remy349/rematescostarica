document.addEventListener('DOMContentLoaded', () => {
    /* SHOW/HIDE MENU */
    const navMenu = document.getElementById('navMenu'),
        navClose = document.getElementById('navClose'),
        navToggle = document.getElementById('navToggle');
    const navItems = document.querySelectorAll('.nav__item');

    if (navToggle) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.add('show-menu');
            navItems.forEach(item => item.classList.add('open'));
        });
    }

    if (navClose) {
        navClose.addEventListener('click', () => {
            navMenu.classList.remove('show-menu');
            navItems.forEach(item => item.classList.remove('open'));
        });
    }


});

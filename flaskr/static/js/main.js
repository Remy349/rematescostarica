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

    /* ACCORDION CURSO */
    const cursosMoreContent = document.getElementsByClassName('cursos__more-content'),
        cursosMoreHeader = document.querySelectorAll('.cursos__more-header');

    function accordionCursos() {
        let itemClass = this.parentNode.className;

        for (let i = 0; i < cursosMoreContent.length; i++) {
            cursosMoreContent[i].className = 'cursos__more-content cursos__more-close';
        }

        if (itemClass === 'cursos__more-content cursos__more-close') {
            this.parentNode.className = 'cursos__more-content cursos__more-open';
        }
    }

    cursosMoreHeader.forEach(cursoHeader => {
        cursoHeader.addEventListener('click', accordionCursos);
    });

    /* NOTIFICATION ALERT */
    const notification = document.querySelector('.notification'),
        notificationContainer = document.querySelector('.notification__container');

    if (notification) {
        setTimeout(() => {
            notification.style.transform = 'translateX(calc(100% + 1rem))';
        }, 7000);

        setTimeout(() => {
            notificationContainer.style.display = 'none';
        }, 7500);
    }
});

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

    /* VALIDAR FORMULARIO DE REGISTRO DE USUARIO */
    const registrateForm = document.getElementById('registrateForm');

    if (registrateForm) {
        registrateForm.addEventListener('submit', validarFormulario);
    }
});

const validarFormulario = (e) => {
    let errors = false;
    const firstname = document.getElementById('firstname').value,
        lastname = document.getElementById('lastname').value,
        username = document.getElementById('username').value;
    const firstnameCont = document.getElementById('firstnameCont'),
        lastnameCont = document.getElementById('lastnameCont'),
        usernameCont = document.getElementById('usernameCont');
    const firstnameLabel = document.getElementById('firstnameLabel'),
        lastnameLabel = document.getElementById('lastnameLabel'),
        usernameLabel = document.getElementById('usernameLabel');
    const justLetters = new RegExp('^[A-Z\ áéíóúñü \]+$', 'i');

    /* validar nombre */
    if (firstname.length == 0) {
        errorInput(firstnameCont, firstnameLabel, 'Nombre no puede estar vacio!');
        errors = true;
    } else if (firstname.length < 3) {
        errorInput(firstnameCont, firstnameLabel, 'Nombre no puede ser menor a 3 caracteres!');
        errors = true;
    } else if (firstname.length > 15) {
        errorInput(firstnameCont, firstnameLabel, 'Nombre no puede ser mayor a 15 caracteres!');
        errors = true;
    } else if (!justLetters.test(firstname)) {
        errorInput(firstnameCont, firstnameLabel, 'Nombre solo debe contener letras!');
        errors = true;
    } else {
        firstnameCont.style.border = 'none';
        firstnameLabel.style.display = 'none';
    }

    /* validar apellido */
    if (lastname.length == 0) {
        errorInput(lastnameCont, lastnameLabel, 'Apellido no puede estar vacio!');
        errors = true;
    } else if (lastname.length < 4) {
        errorInput(lastnameCont, lastnameLabel, 'Apellido no puede ser menor a 4 caracteres!');
        errors = true;
    } else if (lastname.length > 15) {
        errorInput(lastnameCont, lastnameLabel, 'Apellido no puede ser mayor a 15 caracteres!');
        errors = true;
    } else if (!justLetters.test(lastname)) {
        errorInput(lastnameCont, lastnameLabel, 'Apellido solo debe contener letras!');
        errors = true;
    } else {
        lastnameCont.style.border = 'none';
        lastnameLabel.style.display = 'none';
    }

    /* validar username */

    if (errors) {
        e.preventDefault();
    }
}

const errorInput = (idCont, idLabel, message) => {
    idCont.style.border = '2px solid #ff2d2d';
    idLabel.innerText = message;
    idLabel.style.color = '#ff2d2d';
    idLabel.style.fontSize = '1.05rem';
    idLabel.style.display = 'block';
}

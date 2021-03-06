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

    /* VALIDAR FORMULARIOS */
    const registrateForm = document.getElementById('registrateForm');
    const editarAdminForm = document.getElementById('editarAdminForm');
    const editarUserForm = document.getElementById('editarUserForm');

    if (registrateForm) {
        registrateForm.addEventListener('submit', validarFormulario);
    }

    if (editarAdminForm) {
        editarAdminForm.addEventListener('submit', editarAdminValidate);
    }

    if (editarUserForm) {
        editarUserForm.addEventListener('submit', editarUserValidate);
    }

    /* LINK DE DESCARGA PARA ARCHIVO EXCEL */
    const downloadBtn = document.getElementById('downloadBtn');

    if (downloadBtn) {
        downloadBtn.addEventListener('click', () => {
            fetch('/create_file', {
                method: 'GET',
            })
                .then(resp => resp.json())
                .then(data => {
                    const downloadLink = document.getElementById('downloadLink');
                    
                    downloadLink.style.display = 'block';
                    downloadLink.innerHTML = `
                        <a href="${location.origin}/static/files/Usuarios.xlsx" class="download-link" download>
                            Descargar archivo - Usuarios.xlsx
                        </a>
                    `;

                    setTimeout(() => {
                        downloadLink.style.display = 'none';
                    }, 30000);
                })
                .catch(error => console.log(error))
            ;
        });
    }

    /* SWIPER VIDEOS */
    const swiper = new Swiper('.admin__videos-content_slide_cont', {
        slidesPerView: 3,
        spaceBetween: 25,
        loop: true,
        centerSlide: true,
        fade: true,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
            type: 'bullets',
            dynamicBullets: true
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev'
        },
        breakpoints: {
            0: {
                slidesPerView: 1
            },
            //520: {
                //slidesPerView: 2
            //},
            //950: {
                //slidesPerView: 3
            //}
        }
    });
});

const editarUserValidate = (e) => {
    let errors = false;
    const firstname = document.getElementById('firstname').value,
        lastname = document.getElementById('lastname').value,
        phone = document.getElementById('phone').value,
        email = document.getElementById('email').value;
    const firstnameCont = document.getElementById('firstnameCont'),
        lastnameCont = document.getElementById('lastnameCont'),
        phoneCont = document.getElementById('phoneCont'),
        emailCont = document.getElementById('emailCont');
    const firstnameLabel = document.getElementById('firstnameLabel'),
        lastnameLabel = document.getElementById('lastnameLabel'),
        phoneLabel = document.getElementById('phoneLabel'),
        emailLabel = document.getElementById('emailLabel'); 
    const justLetters = new RegExp('^[A-Z\ ?????????????? \]+$', 'i');
    const justNumbers = new RegExp('^[0-9]+$');
    const notWhiteSpace = /\s/;
    const validateEmail = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;

    /* validar nombre */
    if (notWhiteSpace.test(firstname)) {
        errorInput(firstnameCont, firstnameLabel, 'No ingresar espacios en blanco!');
        errors = true;
    } else if (firstname.length == 0) {
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
    if (notWhiteSpace.test(lastname)) {
        errorInput(lastnameCont, lastnameLabel, 'No ingresar espacios en blanco!');
        errors = true;
    } else if (lastname.length == 0) {
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

    /* validar telefono */
    if (phone.length == 0) {
        errorInput(phoneCont, phoneLabel, 'Telefono no puede estar vacio!');
        errors = true;
    } else if (phone.length < 8) {
        errorInput(phoneCont, phoneLabel, 'Telefono no puder ser menor a 8 digitos!');
        errors = true;
    } else if (phone.length > 18) {
        errorInput(phoneCont, phoneLabel, 'Telefono no puede ser mayor a 18 digitos!');
        errors = true;
    } else if (!justNumbers.test(phone)) {
        errorInput(phoneCont, phoneLabel, 'Telefono solo debe contener digitos entre [0-9]!');
        errors = true;
    } else {
        phoneCont.style.border = 'none';
        phoneLabel.style.display = 'none';
    }

    /* validar email */
    if (notWhiteSpace.test(email)) {
        errorInput(emailCont, emailLabel, 'No ingresar espacios en blanco!');
        errors = true;
    } else if (email.length == 0) {
        errorInput(emailCont, emailLabel, 'Direcci??n E-Mail no puede estar vacia!');
        errors = true;
    } else if (!validateEmail.test(email)) {
        errorInput(emailCont, emailLabel, 'Direcci??n E-Mail no permitida! Usa el siguiente formato "ejemplo@ejemplo.com"');
        errors = true
    } else if (email.length < 10) {
        errorInput(emailCont, emailLabel, 'Direcci??n E-Mail muy corta. No menos de 10 caracteres!');
        errors = true;
    } else if (email.length > 150) {
        errorInput(emailCont, emailLabel, 'Direcci??n E-Mail muy larga. No mas de 150 caracteres!');
        errors = true;
    } else {
        emailCont.style.border = 'none';
        emailLabel.style.display = 'none';
    }

    if (errors) {
        e.preventDefault();
    }
}

const editarAdminValidate = (e) => {
    let errors = false;
    const firstname = document.getElementById('firstname').value,
        lastname = document.getElementById('lastname').value,
        email = document.getElementById('email').value;
    const firstnameCont = document.getElementById('firstnameCont'),
        lastnameCont = document.getElementById('lastnameCont'),
        emailCont = document.getElementById('emailCont');
    const firstnameLabel = document.getElementById('firstnameLabel'),
        lastnameLabel = document.getElementById('lastnameLabel'),
        emailLabel = document.getElementById('emailLabel');
    const justLetters = new RegExp('^[A-Z\ ?????????????? \]+$', 'i');
    const notWhiteSpace = /\s/;
    const validateEmail = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;

    /* validar nombre */
    if (notWhiteSpace.test(firstname)) {
        errorInput(firstnameCont, firstnameLabel, 'No ingresar espacios en blanco!');
        errors = true;
    } else if (firstname.length == 0) {
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
    if (notWhiteSpace.test(lastname)) {
        errorInput(lastnameCont, lastnameLabel, 'No ingresar espacios en blanco!');
        errors = true;
    } else if (lastname.length == 0) {
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

    /* validar email */
    if (notWhiteSpace.test(email)) {
        errorInput(emailCont, emailLabel, 'No ingresar espacios en blanco!');
        errors = true;
    } else if (email.length == 0) {
        errorInput(emailCont, emailLabel, 'Direcci??n E-Mail no puede estar vacia!');
        errors = true;
    } else if (!validateEmail.test(email)) {
        errorInput(emailCont, emailLabel, 'Direcci??n E-Mail no permitida! Usa el siguiente formato "ejemplo@ejemplo.com"');
        errors = true
    } else if (email.length < 10) {
        errorInput(emailCont, emailLabel, 'Direcci??n E-Mail muy corta. No menos de 10 caracteres!');
        errors = true;
    } else if (email.length > 150) {
        errorInput(emailCont, emailLabel, 'Direcci??n E-Mail muy larga. No mas de 150 caracteres!');
        errors = true;
    } else {
        emailCont.style.border = 'none';
        emailLabel.style.display = 'none';
    }

    if (errors) {
        e.preventDefault();
    }
}

const validarFormulario = (e) => {
    let errors = false;
    const firstname = document.getElementById('firstname').value,
        lastname = document.getElementById('lastname').value,
        username = document.getElementById('username').value,
        phone = document.getElementById('phone').value,
        email = document.getElementById('email').value,
        password = document.getElementById('password').value,
        passwordT = document.getElementById('passwordT').value;
    const firstnameCont = document.getElementById('firstnameCont'),
        lastnameCont = document.getElementById('lastnameCont'),
        usernameCont = document.getElementById('usernameCont'),
        phoneCont = document.getElementById('phoneCont'),
        emailCont = document.getElementById('emailCont'),
        passwordCont = document.getElementById('passwordCont'),
        passwordContT = document.getElementById('passwordContT');
    const firstnameLabel = document.getElementById('firstnameLabel'),
        lastnameLabel = document.getElementById('lastnameLabel'),
        usernameLabel = document.getElementById('usernameLabel'),
        phoneLabel = document.getElementById('phoneLabel'),
        emailLabel = document.getElementById('emailLabel'),
        passwordLabel = document.getElementById('passwordLabel'),
        passwordLabelT = document.getElementById('passwordLabelT');
    const justLetters = new RegExp('^[A-Z\ ?????????????? \]+$', 'i');
    const justNumbers = new RegExp('^[0-9]+$');
    const notWhiteSpace = /\s/;
    const validateEmail = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;

    /* validar nombre */
    if (notWhiteSpace.test(firstname)) {
        errorInput(firstnameCont, firstnameLabel, 'No ingresar espacios en blanco!');
        errors = true;
    } else if (firstname.length == 0) {
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
    if (notWhiteSpace.test(lastname)) {
        errorInput(lastnameCont, lastnameLabel, 'No ingresar espacios en blanco!');
        errors = true;
    } else if (lastname.length == 0) {
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
    if (notWhiteSpace.test(username)) {
        errorInput(usernameCont, usernameLabel, 'No ingresar espacios en blanco!');
        errors = true;
    } else if (username.length == 0) {
        errorInput(usernameCont, usernameLabel, 'Nombre de usuario no puede estar vacio!');
        errors = true;
    } else if (username.length < 5) {
        errorInput(usernameCont, usernameLabel, 'Nombre de usuario no puede ser menor a 5 caracteres!');
        errors = true;
    } else if (username.length > 15) {
        errorInput(usernameCont, usernameLabel, 'Nombre de usuario no puede ser mayor a 15 caracteres!');
        errors = true;
    } else {
        usernameCont.style.border = 'none';
        usernameLabel.style.display = 'none';
    }

    /* validar telefono */
    if (phone.length == 0) {
        errorInput(phoneCont, phoneLabel, 'Telefono no puede estar vacio!');
        errors = true;
    } else if (phone.length < 8) {
        errorInput(phoneCont, phoneLabel, 'Telefono no puder ser menor a 8 digitos!');
        errors = true;
    } else if (phone.length > 18) {
        errorInput(phoneCont, phoneLabel, 'Telefono no puede ser mayor a 18 digitos!');
        errors = true;
    } else if (!justNumbers.test(phone)) {
        errorInput(phoneCont, phoneLabel, 'Telefono solo debe contener digitos entre [0-9]!');
        errors = true;
    } else {
        phoneCont.style.border = 'none';
        phoneLabel.style.display = 'none';
    }

    /* validar email */
    if (notWhiteSpace.test(email)) {
        errorInput(emailCont, emailLabel, 'No ingresar espacios en blanco!');
        errors = true;
    } else if (email.length == 0) {
        errorInput(emailCont, emailLabel, 'Direcci??n E-Mail no puede estar vacia!');
        errors = true;
    } else if (!validateEmail.test(email)) {
        errorInput(emailCont, emailLabel, 'Direcci??n E-Mail no permitida! Usa el siguiente formato "ejemplo@ejemplo.com"');
        errors = true
    } else if (email.length < 10) {
        errorInput(emailCont, emailLabel, 'Direcci??n E-Mail muy corta. No menos de 10 caracteres!');
        errors = true;
    } else if (email.length > 150) {
        errorInput(emailCont, emailLabel, 'Direcci??n E-Mail muy larga. No mas de 150 caracteres!');
        errors = true;
    } else {
        emailCont.style.border = 'none';
        emailLabel.style.display = 'none';
    }

    /* validar contrase??a */
    if (notWhiteSpace.test(password)) {
        errorInput(passwordCont, passwordLabel, 'No ingresar espacios en blanco!');
        errors = true;
    } else if (password.length == 0) {
        errorInput(passwordCont, passwordLabel, 'Contrase??a no puede estar vacia!');
        errors = true;
    } else if (password.length < 8) {
        errorInput(passwordCont, passwordLabel, 'Contrase??a no puede ser menor a 8 caracteres!');
        errors = true;
    } else {
        passwordCont.style.border = 'none';
        passwordLabel.style.display = 'none';
    }

    if (notWhiteSpace.test(passwordT)) {
        errorInput(passwordContT, passwordLabelT, 'No ingresar espacios en blanco!');
        errors = true;
    } else if (passwordT.length == 0) {
        errorInput(passwordContT, passwordLabelT, 'Confirmar contrase??a no puede estar vacia!');
        errors = true;
    } else if (passwordT !== password) {
        errorInput(passwordContT, passwordLabelT, 'La contrase??a no coinside!');
        errors = true;
    } else {
        passwordContT.style.border = 'none';
        passwordLabelT.style.display = 'none';
    }

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

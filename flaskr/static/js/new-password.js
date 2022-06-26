document.addEventListener('DOMContentLoaded', () => {
    /* RESET USER PASSWORD */
    const newPasswordForm = document.getElementById('newPasswordForm');

    if (newPasswordForm) {
        newPasswordForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const dataForm = new FormData(newPasswordForm);

            try {
                const res = await fetch('/iniciar_sesion/new_password', {
                    method: 'POST',
                    body: dataForm
                });

                if (res.ok) {
                    const data = await res.json();

                    if (data.response === 404) {
                        const newPasswordError = document.getElementById('newPasswordError');
                        newPasswordError.innerHTML = `<p>${data.message}</p>`;
                    } else {
                        const newPasswordContent = document.getElementById('newPasswordContent');

                        newPasswordContent.innerHTML = `
                            <form
                                action="/create_new_password"
                                method="POST"
                                id="newPasswordCreateForm"
                                class="newP__form"
                                accept-charset="utf-8"
                            >
                                <div class="newP__form-title">
                                    <h1>Nueva Contraseña</h1>
                                </div>
                                <div class="newP__form-success">
                                    <p>¡Usuario '${data.message}' encontrado!</p>
                                </div>
                                <div class="newP__form-inputs" id="passwordCont">
                                    <p id="passwordLabel"></p>
                                    <label>Nueva Contraseña</label>
                                    <input
                                        class="newP__form-input"
                                        id="password"
                                        type="password"
                                        autocomplete="off"
                                        name="password"
                                    />
                                </div>
                                <div class="newP__form-btns grid">
                                    <div class="newP__form-btns_confirm">
                                        <button class="newP__form-btns_confirm_btn" type="submit">
                                            Confirmar
                                        </button>
                                    </div>
                                    <div class="newP__form-btns_cancel">
                                        <a href="/iniciar_sesion" class="newP__form-btns_cancel_btn">
                                            Cancelar
                                        </a>
                                    </div>
                                </div>
                            </form>
                        `;

                        newPasswordValidate();
                    }
                } else {
                    throw 'Error en la comunicacion entre el servidor y cliente!';
                }
            } catch (err) {
                console.log(err);
            }
        });
    }
});

const newPasswordValidate = () => {
    const newPasswordCreateForm = document.getElementById('newPasswordCreateForm');

    if (newPasswordCreateForm) {
        newPasswordCreateForm.addEventListener('submit', (e) => {
            let errors = false;
            const password = document.getElementById('password').value;
            const passwordCont = document.getElementById('passwordCont');
            const passwordLabel = document.getElementById('passwordLabel');
            const notWhiteSpace = /\s/;

            /* validar contraseña */
            if (notWhiteSpace.test(password)) {
                errorInput(passwordCont, passwordLabel, 'No ingresar espacios en blanco!');
                errors = true;
            } else if (password.length == 0) {
                errorInput(passwordCont, passwordLabel, 'Contraseña no puede estar vacia!');
                errors = true;
            } else if (password.length < 8) {
                errorInput(passwordCont, passwordLabel, 'Contraseña no puede ser menor a 8 caracteres!');
                errors = true;
            } else {
                passwordCont.style.border = 'none';
                passwordLabel.style.display = 'none';
            }

            if (errors) {
                e.preventDefault();
            }
        });
    }
}

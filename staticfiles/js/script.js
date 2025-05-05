document.addEventListener("DOMContentLoaded", function () {
    // Animación fade-in al cargar
    const main = document.querySelector("main");
    if (main) {
        main.style.opacity = 0;
        main.style.transition = "opacity 0.6s ease-in-out";
        requestAnimationFrame(() => {
            main.style.opacity = 1;
        });
    }

    // Inicializar tooltips de Bootstrap
    const djangoMessages = document.getElementById('django-messages');
    if (djangoMessages) {
        const messages = JSON.parse(djangoMessages.textContent);
        const container = document.getElementById('toast-container');

        messages.forEach(msg => {
            const toastHTML = `
            <div class="toast align-items-center text-white bg-success border-0 mb-2" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">🚀 Esto es un toast de prueba manual desde la consola</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Cerrar"></button>
            </div>
            </div>
            `;

            container.insertAdjacentHTML('beforeend', toastHTML);

            // Inicia el toast con Bootstrap 5
            const toastElement = container.lastElementChild;
            const toast = new bootstrap.Toast(toastElement, {
            delay: 4000  // El tiempo de retraso del toast (en milisegundos)
            });

            toast.show();  // Muestra el toast
        });

    }

    // ✅ AJAX para formulario de perfil
    const form = document.getElementById("profile-form");
    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();
            const formData = new FormData(form);

            fetch(window.location.href, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const toastHTML = `
                    <div class="toast align-items-center text-white bg-${data.success ? 'success' : 'danger'} border-0 mb-2" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="4000">
                        <div class="d-flex">
                            <div class="toast-body">${data.message}</div>
                            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Cerrar"></button>
                        </div>
                    </div>
                `;
                const container = document.getElementById("toast-container");
                container.insertAdjacentHTML('beforeend', toastHTML);
                new bootstrap.Toast(container.lastElementChild).show();

                if (data.success && data.redirect_url) {
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 2000);
                }
            })
            .catch(() => {
                const toastHTML = `
                    <div class="toast align-items-center text-white bg-danger border-0 mb-2" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="4000">
                        <div class="d-flex">
                            <div class="toast-body">Error inesperado al enviar el formulario.</div>
                            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Cerrar"></button>
                        </div>
                    </div>
                `;
                const container = document.getElementById("toast-container");
                container.insertAdjacentHTML('beforeend', toastHTML);
                new bootstrap.Toast(container.lastElementChild).show();
            });
        });
    }
});

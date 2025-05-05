document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("profile-form");
    const messageBox = document.getElementById("ajax-message");
    const btn = document.getElementById("submit-btn");
    const btnText = document.getElementById("btn-text");
    const btnSpinner = document.getElementById("btn-spinner");

    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();
            const formData = new FormData(form);

            // Mostrar spinner
            btnSpinner.classList.remove("d-none");
            btnText.textContent = "Guardando...";
            btn.disabled = true;

            fetch(window.location.href, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                messageBox.textContent = data.message;
                messageBox.className = data.success ? "alert alert-success mt-3" : "alert alert-danger mt-3";

                if (data.success && data.redirect_url) {
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 2000);
                }
            })
            .catch(() => {
                messageBox.textContent = "Error inesperado.";
                messageBox.className = "alert alert-danger mt-3";
            })
            .finally(() => {
                // Ocultar spinner y restaurar botón
                btnSpinner.classList.add("d-none");
                btnText.textContent = "Guardar Cambios";
                btn.disabled = false;
            });
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const togglePassword = document.getElementById("togglePassword");
    const passwordField = document.getElementById("password");
    const usernameField = document.getElementById("username");

    if (togglePassword && passwordField) {
        togglePassword.addEventListener("click", function () {
            const type = passwordField.getAttribute("type") === "password" ? "text" : "password";
            passwordField.setAttribute("type", type);
            this.classList.toggle("fa-eye");
            this.classList.toggle("fa-eye-slash");
            
        });
    }

    // Vibrar solo los inputs si hay error de login
    const alert = document.querySelector(".alert-danger");

    if (alert && usernameField && passwordField) {
        usernameField.classList.add("vibrar");
        passwordField.classList.add("vibrar");

        // Sacar la clase vibrar después de 1.5 segundos
        setTimeout(() => {
            usernameField.classList.remove("vibrar");
            passwordField.classList.remove("vibrar");
        }, 1500);
    }
});

// ==============================================
// FUNCIONES REUTILIZABLES PARA TOASTS
// ==============================================

/**
 * Inicializa y muestra los toasts existentes en la página
 */
function initializeToasts() {
    document.querySelectorAll('.toast').forEach(toastEl => {
        const toast = new bootstrap.Toast(toastEl);
        toast.show();
        
        toastEl.addEventListener('hidden.bs.toast', () => {
            toastEl.remove();
        });
    });
}

/**
 * Crea y muestra un nuevo toast
 * @param {string} message - Mensaje a mostrar
 * @param {string} type - Tipo de toast (success, danger, warning, info)
 */
function createToast(message, type = 'info') {
    const icons = {
        success: 'fa-check-circle',
        danger: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };

    const toastContainer = document.querySelector('.toast-container');
    const toastEl = document.createElement('div');
    
    toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');
    toastEl.dataset.bsDelay = "5000";
    
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas ${icons[type] || icons.info} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white" 
                    data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    toastContainer.appendChild(toastEl);
    new bootstrap.Toast(toastEl).show();
    
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

// ==============================================
// FUNCIONALIDADES ESPECÍFICAS
// ==============================================

/**
 * Configura el toggle para mostrar/ocultar contraseña
 */
function setupPasswordToggle() {
    document.getElementById('togglePassword')?.addEventListener('click', function() {
        const password = document.getElementById('password');
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        this.classList.toggle('fa-eye-slash');
    });
}

/**
 * Maneja el envío del formulario de perfil via AJAX
 */
function handleProfileFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const btn = form.querySelector("#submit-btn");
    const btnText = form.querySelector("#btn-text");
    const btnSpinner = form.querySelector("#btn-spinner");

    // Mostrar estado de carga
    btnSpinner?.classList.remove("d-none");
    btnText.textContent = "Guardando...";
    btn.disabled = true;

    fetch(form.action, {
        method: "POST",
        headers: { "X-Requested-With": "XMLHttpRequest" },
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(data => {
        createToast(data.message, data.success ? 'success' : 'danger');
        if (data.success && data.redirect_url) {
            setTimeout(() => window.location.href = data.redirect_url, 2000);
        }
    })
    .catch(() => createToast("Error inesperado", 'danger'))
    .finally(() => {
        if (btnSpinner) {
            btnSpinner.classList.add("d-none");
            btnText.textContent = "Guardar Cambios";
            btn.disabled = false;
        }
    });
}

// ==============================================
// INICIALIZACIÓN GENERAL
// ==============================================

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar toasts existentes
    initializeToasts();
    
    // Configurar toggle de contraseña (si existe en la página)
    setupPasswordToggle();
    
    // Configurar formulario de perfil (si existe en la página)
    document.getElementById("profile-form")?.addEventListener("submit", handleProfileFormSubmit);
});
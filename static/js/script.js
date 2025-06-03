// ==============================================
// FUNCIONES REUTILIZABLES PARA TOASTS
// ==============================================

const ToastManager = {
    icons: {
        success: 'fa-check-circle',
        danger: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    },

    initializeToasts() {
        document.querySelectorAll('.toast').forEach(toastEl => {
            const toast = new bootstrap.Toast(toastEl);
            toast.show();
            
            toastEl.addEventListener('hidden.bs.toast', () => {
                toastEl.remove();
            });
        });
    },

    createToast(message, type = 'info') {
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
                    <i class="fas ${this.icons[type] || this.icons.info} me-2"></i>
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
};

// ==============================================
// MANEJO DE FORMULARIOS
// ==============================================

const FormHelper = {
    setupPasswordToggle() {
        document.getElementById('togglePassword')?.addEventListener('click', function() {
            const password = document.getElementById('password');
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);
            this.classList.toggle('fa-eye-slash');
        });
    },

    handleProfileFormSubmit(e) {
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
            headers: { 
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json"
            },
            body: new FormData(form)
        })
        .then(response => response.json())
        .then(data => {
            ToastManager.createToast(data.message, data.success ? 'success' : 'danger');
            if (data.success && data.redirect_url) {
                setTimeout(() => window.location.href = data.redirect_url, 2000);
            }
        })
        .catch(() => ToastManager.createToast("Error inesperado", 'danger'))
        .finally(() => {
            if (btnSpinner) {
                btnSpinner.classList.add("d-none");
                btnText.textContent = "Guardar Cambios";
                btn.disabled = false;
            }
        });
    }
};

// ==============================================
// VALIDACIÓN DE CAMPOS
// ==============================================

const FieldValidator = {
    showError(fieldId, message) {
        const field = document.getElementById(fieldId);
        let errorDiv = field.nextElementSibling;
        
        if (!errorDiv || !errorDiv.classList.contains('alert-danger')) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'alert alert-danger mt-2';
            field.parentNode.insertBefore(errorDiv, field.nextElementSibling);
        }
        
        errorDiv.innerHTML = `<small><i class="fas fa-exclamation-circle"></i> ${message}</small>`;
    },

    clearError(fieldId) {
        const field = document.getElementById(fieldId);
        const errorDiv = field.nextElementSibling;
        if (errorDiv && errorDiv.classList.contains('alert-danger')) {
            errorDiv.remove();
        }
    },

    setupNumericField(fieldId, maxLength, errorMessage) {
        const field = document.getElementById(fieldId);
        if (!field) return;

        field.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
            if (this.value.length > maxLength) {
                this.value = this.value.slice(0, maxLength);
            }
            
            if (this.value.length > 0 && this.value.length !== maxLength) {
                FieldValidator.showError(fieldId, errorMessage);
            } else {
                FieldValidator.clearError(fieldId);
            }
        });
    }
};

// ==============================================
// INICIALIZACIÓN GENERAL
// ==============================================

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar toasts
    ToastManager.initializeToasts();
    
    // Configurar toggle de contraseña
    FormHelper.setupPasswordToggle();
    
    // Configurar formulario de perfil
    document.getElementById("profile-form")?.addEventListener("submit", FormHelper.handleProfileFormSubmit);
    
    // Configurar validación de campos
    FieldValidator.setupNumericField('id_ci', 8, 'La cédula debe tener 8 dígitos');
    FieldValidator.setupNumericField('id_telefono', 10, 'El teléfono debe tener 10 dígitos');
    
    // Inicializar dropdowns (solución universal)
    $('.dropdown-toggle').dropdown();
});
// Career data by faculty
const carrerasPorFacultad = {
    "Ingeniería": ["Biomédica", "Biotecnología Industrial", "Ciencia de la Administración", "Ciencias de Alimentos", "Ciencias de Alimentos Industrial", "Civil", "Ciencias de la Computación", "Electrónica", "Industrial", "Mecánica", "Mecánica Industrial", "Mecatrónica", "Química", "Química Industrial"],
    "Ciencias Sociales": ["Antropología", "Arqueología", "Psicología", "Relaciones Internacionales"],
    "Ciencias y Humanidades": ["Biología", "Bioquímica", "Física", "Matemática Aplicada", "Nutrición", "Química", "Química Farmacéutica"],
    "Educación": ["Educación Musical", "Educación Primaria", "Educación Inclusiva"],
    "Bridge Business School": ["Administración de Empresas", "International Marketing and Business Analytics", "Comunicación Estratégica"],
    "Escuela de Arquitectura": ["Arquitectura"]
};

// Sample interests data (in a real app, this would come from the server)
const interesesEjemplo = [
    "Programación", "Inteligencia Artificial", "Ciencia de Datos", 
    "Diseño", "Investigación", "Emprendimiento", 
    "Sostenibilidad", "Robótica", "Medicina", 
    "Economía", "Psicología", "Educación"
];

// Initialize the form
document.addEventListener('DOMContentLoaded', function() {
    initializeForm();
    setupEventListeners();
    
    attachInterestCheckboxListeners();
    validateForm();
});

function attachInterestCheckboxListeners() {
    const checkboxes = document.querySelectorAll('.interest-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            updateSelectedInterests();
            validateForm(); // <-- Muy importante: revalidar cuando cambia
        });
    });
}

function initializeForm() {
    // Set up grade indicator
    updateGradeIndicator();
    
    // Validate form on load
    validateForm();

    const interestCheckboxes = document.querySelectorAll('.interest-checkbox');
    interestCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateSelectedInterests);
    });
}

function setupEventListeners() {
    // Faculty change handler
    const facultadSelect = document.getElementById('facultad');
    facultadSelect.addEventListener('change', actualizarCarreras);

    // Grade input handler
    const promedioInput = document.getElementById('promedio');
    promedioInput.addEventListener('input', updateGradeIndicator);
    promedioInput.addEventListener('blur', validateGrade);

    // Interest checkboxes handler
    const interestCheckboxes = document.querySelectorAll('.interest-checkbox:checked');
    interestCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateSelectedInterests);
        validateForm();
    });

    // Form validation on input changes
    const formInputs = document.querySelectorAll('.form-select, .form-input');
    formInputs.forEach(input => {
        input.addEventListener('change', validateForm);
        input.addEventListener('input', validateForm);
    });

    // Form submission
    const form = document.getElementById('academicForm');
    form.addEventListener('submit', handleFormSubmission);

    // Focus effects
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.closest('.form-group').classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.closest('.form-group').classList.remove('focused');
        });
    });
    validateForm();
}

function populateInterests(interests) {
    const container = document.getElementById('interestsContainer');
    container.innerHTML = '';
    
    interests.forEach(interest => {
        const label = document.createElement('label');
        label.className = 'interest-option';
        
        label.innerHTML = `
            <input type="checkbox" name="intereses[]" value="${interest}" class="interest-checkbox">
            <span class="interest-card">
                <span class="interest-name">${interest}</span>
            </span>
        `;
        
        container.appendChild(label);
    });
    
    // Re-attach event listeners
    const interestCheckboxes = document.querySelectorAll('.interest-checkbox');
    interestCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            updateSelectedInterests();
            validateForm();
        });
    });
    validateForm();
}

function actualizarCarreras() {
    const facultadSeleccionada = document.getElementById("facultad").value;
    const carreraSelect = document.getElementById("carrera");
    
    // Clear previous options
    carreraSelect.innerHTML = "";
    
    if (facultadSeleccionada && carrerasPorFacultad[facultadSeleccionada]) {
        // Enable the career select
        carreraSelect.disabled = false;
        
        // Add default option
        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.text = "Selecciona tu carrera";
        defaultOption.disabled = true;
        defaultOption.selected = true;
        carreraSelect.appendChild(defaultOption);
        
        // Add career options
        carrerasPorFacultad[facultadSeleccionada].forEach(carrera => {
            const option = document.createElement("option");
            option.value = carrera;
            option.text = carrera;
            carreraSelect.appendChild(option);
        });
        
        // Add success state to faculty
        document.getElementById('facultad').closest('.form-group').classList.add('success');
        document.getElementById('facultad').closest('.form-group').classList.remove('error');
    } else {
        // Disable career select if no faculty selected
        carreraSelect.disabled = true;
        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.text = "Primero selecciona una facultad";
        defaultOption.disabled = true;
        defaultOption.selected = true;
        carreraSelect.appendChild(defaultOption);
    }
    
    // Validate form after updating careers
    validateForm();
}

function updateGradeIndicator() {
    const promedioInput = document.getElementById('promedio');
    const gradeFill = document.getElementById('gradeFill');
    const gradeText = document.getElementById('gradeText');
    
    const promedio = parseFloat(promedioInput.value);
    
    if (isNaN(promedio) || promedio < 0 || promedio > 100) {
        gradeFill.style.width = '0%';
        gradeText.textContent = 'Ingresa tu promedio';
        gradeText.style.color = 'var(--neutral-600)';
        return;
    }
    
    // Calculate percentage (1-10 scale to 0-100%)
    const percentage = promedio;
    gradeFill.style.width = percentage + '%';
    
    // Update color based on grade
    let color = '';
    
    if (promedio >= 90) {
        color = 'var(--primary-green)';
    } else if (promedio >= 80) {
        color = 'var(--accent-blue)';
    } else if (promedio >= 70) {
        color = 'var(--accent-orange)';
    } else if (promedio >= 60) {
        color = 'var(--accent-orange)';
    } else {
        color = 'var(--accent-red)';
    }
    
    gradeText.style.color = color;
}

function validateGrade() {
    const promedioInput = document.getElementById('promedio');
    const promedio = parseFloat(promedioInput.value);
    const formGroup = promedioInput.closest('.form-group');
    
    if (isNaN(promedio) || promedio < 0 || promedio > 100) {
        formGroup.classList.add('error');
        formGroup.classList.remove('success');
        showFieldError(promedioInput, 'El promedio debe estar entre 0 y 100');
    } else {
        formGroup.classList.remove('error');
        formGroup.classList.add('success');
        clearFieldError(promedioInput);
    }
}

function updateSelectedInterests() {
    const checkboxes = document.querySelectorAll('.interest-checkbox:checked');
    const selectedContainer = document.getElementById('interestsSelected');
    
    if (checkboxes.length === 0) {
        selectedContainer.innerHTML = '<span>Ninguna área seleccionada</span>';
        return;
    }
    
    selectedContainer.innerHTML = '';
    checkboxes.forEach(checkbox => {
        const tag = document.createElement('div');
        tag.className = 'interest-tag';
        tag.innerHTML = `${checkbox.value} <i class="fas fa-check"></i>`;
        selectedContainer.appendChild(tag);
    });
}

function validateForm() {
    const facultad = document.getElementById('facultad').value;
    const carrera = document.getElementById('carrera').value;
    const promedio = document.getElementById('promedio').value;
    const interestCheckboxes = document.querySelectorAll('input.interest-checkbox:checked');
    const continueButton = document.getElementById('continueButton');

    const isValid = facultad && carrera &&
                    promedio !== '' &&
                    !isNaN(parseFloat(promedio)) &&
                    parseFloat(promedio) >= 0 &&
                    parseFloat(promedio) <= 100 &&
                    interestCheckboxes.length > 0;

    continueButton.disabled = !isValid;
    return isValid;
}


function handleFormSubmission(e) {
    e.preventDefault();
    
    if (!validateForm()) {
        if (document.querySelectorAll('.interest-checkbox:checked').length === 0) {
            showError('Por favor selecciona al menos un área de interés');
        } else {
            showError('Por favor completa todos los campos correctamente');
        }
        return;
    }
    
    // Collect selected interests
    const selectedInterests = Array.from(document.querySelectorAll('.interest-checkbox:checked')).map(cb => cb.value);
    console.log('Intereses seleccionados:', selectedInterests);
    
    // Show loading overlay
    const loadingOverlay = document.getElementById('loadingOverlay');
    loadingOverlay.classList.add('active');
    
    // Simulate form processing
    setTimeout(() => {
        // In a real application, this would submit to the server
        // For now, we'll just redirect or show success
        loadingOverlay.classList.remove('active');
        
        // Submit the form (uncomment for real submission)
        // e.target.submit();
        
        // For demo purposes, show success message
        showSuccess('Perfil académico guardado exitosamente. Redirigiendo al test de personalidad...');
        
        setTimeout(() => {
            // Redirect to personality test
            // window.location.href = '/test';
            console.log('Redirecting to personality test...');
        }, 2000);
    }, 2000);
}

function showFieldError(field, message) {
    // Remove existing error message
    const existingError = field.closest('.form-group').querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Add error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.cssText = `
        color: var(--accent-red);
        font-size: 0.875rem;
        margin-top: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        animation: slideIn 0.3s ease;
    `;
    errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i>${message}`;
    
    field.closest('.form-group').appendChild(errorDiv);
}

function clearFieldError(field) {
    const errorMessage = field.closest('.form-group').querySelector('.error-message');
    if (errorMessage) {
        errorMessage.remove();
    }
}

function showError(message) {
    showNotification(message, 'error');
}

function showSuccess(message) {
    showNotification(message, 'success');
}

function showNotification(message, type) {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}-notification`;
    
    const bgColor = type === 'error' ? 'var(--accent-red)' : 'var(--primary-green)';
    const icon = type === 'error' ? 'fas fa-exclamation-circle' : 'fas fa-check-circle';
    
    notification.style.cssText = `
        position: fixed;
        top: 2rem;
        right: 2rem;
        background: ${bgColor};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow-xl);
        z-index: 1001;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-weight: 600;
        font-size: 0.875rem;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 400px;
    `;
    
    notification.innerHTML = `<i class="${icon}"></i>${message}`;
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Hide notification
    const hideTimeout = type === 'error' ? 5000 : 3000;
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 300);
    }, hideTimeout);
}

// Add CSS animation for slideIn
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);
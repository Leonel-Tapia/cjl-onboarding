from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\templates\onboarding_form.html")
txt = p.read_text(encoding="utf-8")

# 1. Cambiar el id del span a uno oculto para guardar la hora exacta
old_span = '<span id="fechaRegistro"></span>'
new_span = '<span id="fechaRegistro"></span>'

# 2. Agregar la actualización en el evento submit (justo donde valida el nombre)
old_js = '''    const termsCheckbox = document.getElementById('termsCheckbox');
    const authName = document.getElementById('authName');
    const hint = document.getElementById('authNameHint');

    if (termsCheckbox && authName) {'''

new_js = '''    const termsCheckbox = document.getElementById('termsCheckbox');
    const authName = document.getElementById('authName');
    const hint = document.getElementById('authNameHint');

    // Actualizar la fecha exacta cuando se envía el formulario
    const form = document.getElementById('onboardingForm');
    if (form) {
        form.addEventListener('submit', function() {
            const fechaSpan = document.getElementById('fechaRegistro');
            if (fechaSpan) {
                const ahora = new Date();
                const opciones = { 
                    year: 'numeric', month: 'long', day: 'numeric',
                    hour: '2-digit', minute: '2-digit', second: '2-digit'
                };
                fechaSpan.textContent = ahora.toLocaleDateString('es-MX', opciones);
                // También guardamos en el sello para que quede en el PDF
                const sealField = document.getElementById('sealField');
                const name = document.getElementById('authName').value.trim();
                if (sealField) {
                    sealField.value = 'Authorized by: ' + name + ' — ' + ahora.toLocaleDateString('es-MX', opciones);
                }
            }
        });
    }

    if (termsCheckbox && authName) {'''

if old_js in txt:
    txt = txt.replace(old_js, new_js)
    p.write_text(txt, encoding="utf-8")
    print("OK fecha congelada al enviar")
else:
    print("NO encontrado - revisar")
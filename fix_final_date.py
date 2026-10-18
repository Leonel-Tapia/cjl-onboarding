from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\templates\onboarding_form.html")
txt = p.read_text(encoding="utf-8")

# 1. Reemplazar el bloque viejo de la fecha por el nuevo texto
old_block = '''<i class="fas fa-clock"></i> 
                <strong>Fecha de registro:</strong> 
                <span id="fechaRegistro"></span>'''
# Por si no coincide exactamente por espacios, buscamos solo el span
old_span = '<span id="fechaRegistro"></span>'

new_span = '<i class="fas fa-history"></i> <strong>Última actualización: {{ fecha_version }}</strong>'

if old_span in txt:
    txt = txt.replace(old_span, new_span)
    print("HTML actualizado: span reemplazado")

# 2. Quitar el JavaScript viejo que intentaba actualizar la fecha
old_js = '''    // Llenar la fecha de registro al cargar
    const fechaSpan = document.getElementById('fechaRegistro');
    if (fechaSpan) {
        const ahora = new Date();
        const opciones = { 
            year: 'numeric', month: 'long', day: 'numeric',
            hour: '2-digit', minute: '2-digit'
        };
        fechaSpan.textContent = ahora.toLocaleDateString('es-MX', opciones);
    }'''
if old_js in txt:
    txt = txt.replace(old_js, '')
    print("JS viejo eliminado")

# 3. Quitar el JS que actualiza la fecha al hacer submit (si existe)
old_js2 = '''    // Actualizar la fecha exacta cuando se envía el formulario
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
                const sealField = document.getElementById('sealField');
                const name = document.getElementById('authName').value.trim();
                if (sealField) {
                    sealField.value = 'Authorized by: ' + name + ' — ' + ahora.toLocaleDateString('es-MX', opciones);
                }
            }
        });
    }'''
if old_js2 in txt:
    txt = txt.replace(old_js2, '')
    print("JS submit viejo eliminado")

p.write_text(txt, encoding="utf-8")
print("OK HTML actualizado")
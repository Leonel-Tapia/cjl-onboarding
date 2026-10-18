from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\templates\onboarding_form.html")
txt = p.read_text(encoding="utf-8")

# Buscar el botón de autorización
old = '<div class="mt-3"><button type="submit" class="btn btn-success btn-lg" id="submitBtn" onclick="return generateSeal()" disabled><i class="fas fa-check"></i> Accept & Authorize</button></div>'

new = '''<div class="mt-3" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
            <div style="font-size: 13px; color: #666; background: #f8f9fa; padding: 8px 15px; border-radius: 6px; border-left: 3px solid #198754;">
                <i class="fas fa-clock"></i> 
                <strong>Fecha de registro:</strong> 
                <span id="fechaRegistro"></span>
            </div>
            <button type="submit" class="btn btn-success btn-lg" id="submitBtn" onclick="return generateSeal()" disabled>
                <i class="fas fa-check"></i> Accept & Authorize
            </button>
        </div>'''

if old in txt:
    txt = txt.replace(old, new)
    print("Timestamp agregado antes del botón")
else:
    print("Botón NO encontrado - revisar")

# Agregar JS para llenar la fecha automáticamente
old_js = '''document.addEventListener('DOMContentLoaded', function() {
    const termsCheckbox = document.getElementById('termsCheckbox');'''

new_js = '''document.addEventListener('DOMContentLoaded', function() {
    // Llenar la fecha de registro al cargar
    const fechaSpan = document.getElementById('fechaRegistro');
    if (fechaSpan) {
        const ahora = new Date();
        const opciones = { 
            year: 'numeric', month: 'long', day: 'numeric',
            hour: '2-digit', minute: '2-digit'
        };
        fechaSpan.textContent = ahora.toLocaleDateString('es-MX', opciones);
    }

    const termsCheckbox = document.getElementById('termsCheckbox');'''

if old_js in txt:
    txt = txt.replace(old_js, new_js)
    print("JS de fecha agregado")

p.write_text(txt, encoding="utf-8")
print("OK timestamp agregado")
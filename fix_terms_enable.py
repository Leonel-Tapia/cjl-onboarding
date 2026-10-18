from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\templates\onboarding_form.html")
txt = p.read_text(encoding="utf-8")

# 1. Checkbox con ID
old_terms = '<label class="form-label fw-bold"><input type="checkbox" name="acepta_terminos" required> Acepto los términos y condiciones del servicio</label>'
new_terms = '<label class="form-label fw-bold"><input type="checkbox" name="acepta_terminos" id="termsCheckbox" required> Acepto los términos y condiciones del servicio</label>'

if old_terms in txt:
    txt = txt.replace(old_terms, new_terms)
    print("Checkbox con ID agregado")
else:
    print("Checkbox NO encontrado")

# 2. Input de nombre deshabilitado por defecto
old_input = '<div class="col-md-6"><label class="form-label required-label">Full Name</label><input type="text" class="form-control" name="autoriza_cliente_nombre" id="authName" required></div>'
new_input = '<div class="col-md-6"><label class="form-label required-label">Full Name <small style="color:#999;" id="authNameHint">(marque los términos primero)</small></label><input type="text" class="form-control" name="autoriza_cliente_nombre" id="authName" required disabled></div>'

if old_input in txt:
    txt = txt.replace(old_input, new_input)
    print("Input deshabilitado por defecto")
else:
    print("Input NO encontrado")

# 3. JavaScript al final del template (antes del {% endblock %})
old_js = '{% endblock %}'
new_js = '''<script>
document.addEventListener('DOMContentLoaded', function() {
    const termsCheckbox = document.getElementById('termsCheckbox');
    const authName = document.getElementById('authName');
    const hint = document.getElementById('authNameHint');

    if (termsCheckbox && authName) {
        termsCheckbox.addEventListener('change', function() {
            if (this.checked) {
                authName.disabled = false;
                authName.focus();
                if (hint) hint.style.display = 'none';
            } else {
                authName.disabled = true;
                authName.value = '';
                if (hint) hint.style.display = 'inline';
            }
        });
    }
});
</script>
{% endblock %}'''

# Reemplazar solo el ULTIMO endblock (el que cierra block scripts)
idx = txt.rfind(old_js)
if idx != -1:
    txt = txt[:idx] + new_js + txt[idx + len(old_js):]
    print("JS agregado")

p.write_text(txt, encoding="utf-8")
print("OK formulario actualizado")
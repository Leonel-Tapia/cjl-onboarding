from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\templates\onboarding_form.html")
txt = p.read_text(encoding="utf-8")

# 1. Botón deshabilitado por defecto
old_btn = '<div class="mt-3"><button type="submit" class="btn btn-success btn-lg" onclick="return generateSeal()"><i class="fas fa-check"></i> Accept & Authorize</button></div>'
new_btn = '<div class="mt-3"><button type="submit" class="btn btn-success btn-lg" id="submitBtn" onclick="return generateSeal()" disabled><i class="fas fa-check"></i> Accept & Authorize</button></div>'

if old_btn in txt:
    txt = txt.replace(old_btn, new_btn)
    print("Botón deshabilitado por defecto")
else:
    print("Botón NO encontrado")

# 2. Modificar el JS para habilitar el botón
old_js = '''    if (termsCheckbox && authName) {
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
    }'''

new_js = '''    const submitBtn = document.getElementById('submitBtn');

    function updateSubmitBtn() {
        if (termsCheckbox && authName && submitBtn) {
            const ready = termsCheckbox.checked && authName.value.trim().length > 0;
            submitBtn.disabled = !ready;
            submitBtn.style.opacity = ready ? '1' : '0.5';
            submitBtn.style.cursor = ready ? 'pointer' : 'not-allowed';
        }
    }

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
            updateSubmitBtn();
        });

        authName.addEventListener('input', updateSubmitBtn);
        updateSubmitBtn();
    }'''

if old_js in txt:
    txt = txt.replace(old_js, new_js)
    print("JS actualizado para habilitar botón")
else:
    print("JS NO encontrado - revisar")

p.write_text(txt, encoding="utf-8")
print("OK formulario actualizado")
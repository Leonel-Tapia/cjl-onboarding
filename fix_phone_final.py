from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\templates\onboarding_form.html")
txt = p.read_text(encoding="utf-8")

# Reemplazar el campo de telefono del negocio para que use el mismo sistema
old = '<input type="text" class="form-control" name="telefono_negocio" oninput="formatPhone(this)" required>'
new = '<input type="text" class="form-control" name="telefono_negocio" oninput="formatPhoneInput(this)" required>'

if old in txt:
    txt = txt.replace(old, new)
    print("HTML actualizado para usar formatPhoneInput")

# Buscar si existe la funcion formatPhoneInput
if 'function formatPhoneInput' not in txt:
    # Si no existe, creamos una función exacta basada en la que ya funciona
    js_code = '''
    function formatPhoneInput(input) {
        let numbers = input.value.replace(/\\D/g, '');
        if (numbers.length > 10) numbers = numbers.substring(0, 10);
        let formatted = '';
        if (numbers.length > 6) {
            formatted = '(' + numbers.substring(0, 3) + ') ' + numbers.substring(3, 6) + '-' + numbers.substring(6);
        } else if (numbers.length > 3) {
            formatted = '(' + numbers.substring(0, 3) + ') ' + numbers.substring(3);
        } else if (numbers.length > 0) {
            formatted = '(' + numbers;
        }
        input.value = formatted;
    }
'''
    # Insertar la funcion justo antes del cierre del primer <script> que encuentre
    idx = txt.find('<script>')
    if idx != -1:
        txt = txt[:idx+8] + js_code + txt[idx+8:]
        print("Funcion formatPhoneInput creada")

p.write_text(txt, encoding="utf-8")
print("OK todo listo")
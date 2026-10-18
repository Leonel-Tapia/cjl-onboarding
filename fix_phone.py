from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\templates\onboarding_form.html")
txt = p.read_text(encoding="utf-8")

# Buscar el evento que no coincide
old = """document.addEventListener('input', function (e) {
    if (e.target && e.target.name === 'phone_for_quotes') {"""

new = """document.addEventListener('input', function (e) {
    if (e.target && (e.target.name === 'telefono_cotizaciones' || e.target.name === 'numero_principal_grupo')) {"""

if old in txt:
    txt = txt.replace(old, new)
    p.write_text(txt, encoding="utf-8")
    print("OK: funcion de formato de telefono corregida")
else:
    print("NO encontrado - intentando variante")
    # Variante por si el codigo tiene espacios distintos
    old2 = "if (e.target && e.target.name === 'phone_for_quotes')"
    new2 = "if (e.target && (e.target.name === 'telefono_cotizaciones' || e.target.name === 'numero_principal_grupo'))"
    if old2 in txt:
        txt = txt.replace(old2, new2)
        p.write_text(txt, encoding="utf-8")
        print("OK: corregido por variante")
    else:
        print("No se pudo encontrar la linea")
from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\templates\onboarding_form.html")
txt = p.read_text(encoding="utf-8")

# Agregar oninput al telefono del negocio
old = '<input type="text" class="form-control" name="telefono_negocio" required>'
new = '<input type="text" class="form-control" name="telefono_negocio" oninput="formatPhone(this)" required>'

if old in txt:
    txt = txt.replace(old, new)
    p.write_text(txt, encoding="utf-8")
    print("OK telefono_negocio ahora formatea")
else:
    print("NO encontrado - revisando variantes...")
    # Probar si tiene otra estructura
    old2 = '<input type="text" class="form-control" name="telefono_negocio"'
    if old2 in txt and 'oninput="formatPhone(this)"' not in txt[txt.find('telefono_negocio')-50:txt.find('telefono_negocio')+200]:
        txt = txt.replace(old2, '<input type="text" class="form-control" name="telefono_negocio" oninput="formatPhone(this)"', 1)
        p.write_text(txt, encoding="utf-8")
        print("OK: agregado por variante")
    else:
        print("No se encontro el campo")
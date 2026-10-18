from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\routers\onboarding.py")
txt = p.read_text(encoding="utf-8")

# 1. Agregar los 4 campos al inicio del router (submit_form)
old = 'email_cotizaciones: str = Form(...),'
new = '''nombre_negocio: str = Form(...), telefono_negocio: Optional[str] = Form(None),
    ciudad: Optional[str] = Form(None), codigo_postal: Optional[str] = Form(None),
    email_cotizaciones: str = Form(...),'''

if 'nombre_negocio: str = Form' not in txt:
    txt = txt.replace(old, new)
    print("Parámetros agregados al router")
else:
    print("Ya existían los parámetros")

# 2. Agregar los 4 campos al crear el registro
old_create = 'version_documento="v1.0",'
new_create = '''version_documento="v1.0",
        nombre_negocio=nombre_negocio, telefono_negocio=telefono_negocio,
        ciudad=ciudad, codigo_postal=codigo_postal,'''

if 'nombre_negocio=nombre_negocio' not in txt:
    txt = txt.replace(old_create, new_create)
    print("Campos agregados al crear registro")
else:
    print("Ya existían en el registro")

p.write_text(txt, encoding="utf-8")
print("OK router actualizado")
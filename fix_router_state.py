from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\routers\onboarding.py")
txt = p.read_text(encoding="utf-8")

# 1. Agregar parámetro
old = 'ciudad: Optional[str] = Form(None), codigo_postal: Optional[str] = Form(None),'
new = 'ciudad: Optional[str] = Form(None), estado_negocio: Optional[str] = Form(None), codigo_postal: Optional[str] = Form(None),'

if 'estado_negocio: Optional[str]' not in txt:
    txt = txt.replace(old, new)
    print("Parámetro estado_negocio agregado")

# 2. Agregar al crear registro
old_create = 'ciudad=ciudad, codigo_postal=codigo_postal,'
new_create = 'ciudad=ciudad, estado_negocio=estado_negocio, codigo_postal=codigo_postal,'

if 'estado_negocio=estado_negocio' not in txt:
    txt = txt.replace(old_create, new_create)
    print("Campo agregado al registro")

p.write_text(txt, encoding="utf-8")
print("OK router actualizado")
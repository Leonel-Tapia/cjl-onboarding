from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\routers\onboarding.py")
txt = p.read_text(encoding="utf-8")

# Buscamos la función submit_form
old = '''    registro = OnboardingOptiGlass(
        id_interno=id_interno, fecha_submit=datetime.now(), estado="pending", precios_json=precios,'''

new = '''    # Forzamos a que la fecha sea exactamente la hora actual local sin microsegundos problemáticos
    ahora = datetime.now().replace(microsecond=0)

    registro = OnboardingOptiGlass(
        id_interno=id_interno, fecha_submit=ahora, estado="pending", precios_json=precios,'''

if old in txt:
    txt = txt.replace(old, new)
    print("Fecha submit corregida")
else:
    print("NO se encontro fecha submit")

# Buscamos la fecha de autorización
old2 = '        autoriza_cliente=True, autoriza_cliente_nombre=autoriza_cliente_nombre, autoriza_cliente_sello=autoriza_cliente_sello, autoriza_cliente_fecha=datetime.now(), autoriza_cliente_ip=client_ip,'
new2 = '        autoriza_cliente=True, autoriza_cliente_nombre=autoriza_cliente_nombre, autoriza_cliente_sello=autoriza_cliente_sello, autoriza_cliente_fecha=ahora, autoriza_cliente_ip=client_ip,'

if old2 in txt:
    txt = txt.replace(old2, new2)
    print("Fecha autorizacion corregida")
else:
    print("NO se encontro fecha autorizacion")

p.write_text(txt, encoding="utf-8")
print("OK Fechas corregidas para formato Postgres")
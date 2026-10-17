from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\routers\onboarding.py")
txt = p.read_text(encoding="utf-8")

# Buscamos la creación del registro y forzamos un objeto datetime puro
old_1 = '        id_interno=id_interno, fecha_submit=datetime.utcnow(), estado="pending", precios_json=precios,'
new_1 = '        id_interno=id_interno, fecha_submit=datetime.now(), estado="pending", precios_json=precios,'

old_2 = '        autoriza_cliente=True, autoriza_cliente_nombre=autoriza_cliente_nombre, autoriza_cliente_sello=autoriza_cliente_sello, autoriza_cliente_fecha=datetime.utcnow(), autoriza_cliente_ip=client_ip,'
new_2 = '        autoriza_cliente=True, autoriza_cliente_nombre=autoriza_cliente_nombre, autoriza_cliente_sello=autoriza_cliente_sello, autoriza_cliente_fecha=datetime.now(), autoriza_cliente_ip=client_ip,'

if old_1 in txt:
    txt = txt.replace(old_1, new_1)
    print("Fecha submit actualizada")
else:
    print("No se encontro fecha submit")

if old_2 in txt:
    txt = txt.replace(old_2, new_2)
    print("Fecha autorizacion actualizada")
else:
    print("No se encontro fecha autorizacion")

# Revisar si en el update_status tambien hay un utcnow
old_3 = 'registro.status_changed_at = datetime.utcnow(); db.commit()'
new_3 = 'registro.status_changed_at = datetime.now(); db.commit()'

if old_3 in txt:
    txt = txt.replace(old_3, new_3)
    print("Fecha status actualizada")

p.write_text(txt, encoding="utf-8")
print("OK Fechas corregidas")
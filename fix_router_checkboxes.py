from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\routers\onboarding.py")
txt = p.read_text(encoding="utf-8")

old = '''    form = await request.form()
    garantias_json = {"fugas": "garantia_fugas" in form, "mano_obra": "garantia_mano_obra" in form, "fabrica": "garantia_fabrica" in form, "molduras": "garantia_molduras" in form, "otro": "garantia_otro" in form}
    metodos_pago_json = {"efectivo": "pago_efectivo" in form, "zelle": "pago_zelle" in form, "tarjeta": "pago_tarjeta" in form, "transferencia": "pago_transferencia" in form, "financiamiento": "pago_financiamiento" in form}
    aseguradoras_json = {"state_farm": "seguro_state_farm" in form, "geico": "seguro_geico" in form, "progressive": "seguro_progressive" in form, "allstate": "seguro_allstate" in form, "otra": "seguro_otra" in form}'''

new = '''    form = await request.form()
    # Leemos los checkboxes con el mismo nombre que se puso en el HTML (garantias[], metodos_pago[], aseguradoras[], material_visual[])
    garantias_list = form.getlist("garantias[]")
    garantias_json = {"fugas": "Fugas y filtraciones (por vida)" in garantias_list, "mano_obra": "Mano de obra / instalacion" in garantias_list, "fabrica": "Fabrica del vidrio" in garantias_list, "molduras": "Molduras y empaques" in garantias_list, "otro": form.get("garantia_otro", "")}

    metodos_list = form.getlist("metodos_pago[]")
    metodos_pago_json = {"efectivo": "Efectivo" in metodos_list, "zelle": "Zelle" in metodos_list, "tarjeta": "Tarjeta credito/debito" in metodos_list, "transferencia": "Transferencia" in metodos_list, "financiamiento": "Financiamiento" in metodos_list}

    aseguradoras_list = form.getlist("aseguradoras[]")
    aseguradoras_json = {"state_farm": "State Farm" in aseguradoras_list, "geico": "Geico" in aseguradoras_list, "progressive": "Progressive" in aseguradoras_list, "allstate": "Allstate" in aseguradoras_list, "otra": "Otra" in aseguradoras_list}'''

if old in txt:
    txt = txt.replace(old, new)
    p.write_text(txt, encoding="utf-8")
    print("OK router corregido")
else:
    print("NO encontrado")
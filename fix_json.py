from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\routers\onboarding.py")
txt = p.read_text(encoding="utf-8")

# 1. Importar json
if "import json" not in txt:
    txt = txt.replace("from datetime import datetime", "from datetime import datetime\nimport json")

# 2. Convertir los string a JSON
old_precios = 'id_interno=id_interno, fecha_submit=func.now(), estado="pending", precios_json=precios,'
new_precios = 'id_interno=id_interno, fecha_submit=func.now(), estado="pending", precios_json=precios if isinstance(precios, list) else json.loads(precios),'

if old_precios in txt:
    txt = txt.replace(old_precios, new_precios)
    print("Precios JSON corregido")
else:
    print("NO se encontro la linea de precios")

# 3. Convertir garantias a JSON
old_garantias = 'garantias_json=garantias_json'
new_garantias = 'garantias_json=garantias_json if isinstance(garantias_json, dict) else json.loads(garantias_json)'

if old_garantias in txt:
    txt = txt.replace(old_garantias, new_garantias)
    print("Garantias JSON corregido")

# 4. Convertir metodos_pago a JSON
old_metodos = 'metodos_pago_json=metodos_pago_json'
new_metodos = 'metodos_pago_json=metodos_pago_json if isinstance(metodos_pago_json, dict) else json.loads(metodos_pago_json)'

if old_metodos in txt:
    txt = txt.replace(old_metodos, new_metodos)
    print("Metodos Pago JSON corregido")

# 5. Convertir aseguradoras a JSON
old_aseguradoras = 'aseguradoras_json=aseguradoras_json'
new_aseguradoras = 'aseguradoras_json=aseguradoras_json if isinstance(aseguradoras_json, dict) else json.loads(aseguradoras_json)'

if old_aseguradoras in txt:
    txt = txt.replace(old_aseguradoras, new_aseguradoras)
    print("Aseguradoras JSON corregido")

p.write_text(txt, encoding="utf-8")
print("OK Todo convertido a JSON nativo")
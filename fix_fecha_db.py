from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\routers\onboarding.py")
txt = p.read_text(encoding="utf-8")

# Asegurarnos de importar func
if "from sqlalchemy import func" not in txt:
    txt = txt.replace("from sqlalchemy.orm import Session", "from sqlalchemy.orm import Session\nfrom sqlalchemy import func")

# Buscamos la variable 'ahora' y la eliminamos
old_var = '''    # Usamos datetime.utcnow() para que la base de datos lo reciba como objeto nativo sin problemas
    ahora = datetime.utcnow()'''
new_var = '''    # Usaremos func.now() directamente en el modelo'''

if old_var in txt:
    txt = txt.replace(old_var, new_var)
    print("Variable 'ahora' eliminada")
else:
    # Intentar con la variante anterior
    old_var2 = '''    # Forzamos a que la fecha sea un string simple: YYYY-MM-DD
    ahora = datetime.now().strftime("%Y-%m-%d")'''
    if old_var2 in txt:
        txt = txt.replace(old_var2, new_var)
        print("Variable 'ahora' eliminada (variante)")
    else:
        print("No se encontro la variable 'ahora'")

# Reemplazamos el uso de 'ahora' por func.now()
txt = txt.replace("fecha_submit=ahora", "fecha_submit=func.now()")
txt = txt.replace("autoriza_cliente_fecha=ahora", "autoriza_cliente_fecha=func.now()")

p.write_text(txt, encoding="utf-8")
print("OK Fecha cambiada a func.now()")
from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\routers\onboarding.py")
txt = p.read_text(encoding="utf-8")

old = '''    # Forzamos a que la fecha sea un string simple: YYYY-MM-DD
    ahora = datetime.now().strftime("%Y-%m-%d")'''

new = '''    # Usamos datetime.utcnow() para que la base de datos lo reciba como objeto nativo sin problemas
    ahora = datetime.utcnow()'''

if old in txt:
    txt = txt.replace(old, new)
    p.write_text(txt, encoding="utf-8")
    print("OK fecha cambiada a datetime.utcnow()")
else:
    print("NO se encontro la variable ahora")
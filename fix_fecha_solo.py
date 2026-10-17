from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\routers\onboarding.py")
txt = p.read_text(encoding="utf-8")

# Cambiamos a formato solo fecha YYYY-MM-DD
old = '''    # Forzamos a que la fecha sea un string en formato YYYY-MM-DD HH:MM:SS
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")'''

new = '''    # Forzamos a que la fecha sea un string simple: YYYY-MM-DD
    ahora = datetime.now().strftime("%Y-%m-%d")'''

if old in txt:
    txt = txt.replace(old, new)
    p.write_text(txt, encoding="utf-8")
    print("OK fecha cambiada a solo YYYY-MM-DD")
else:
    print("NO encontrado - intentando variante")
    # Variante por si no se aplicó el paso anterior
    old2 = '    ahora = datetime.now().replace(microsecond=0)'
    if old2 in txt:
        txt = txt.replace(old2, new)
        p.write_text(txt, encoding="utf-8")
        print("OK fecha cambiada a solo YYYY-MM-DD (desde microsecond)")
    else:
        print("No se encontro la variable ahora")
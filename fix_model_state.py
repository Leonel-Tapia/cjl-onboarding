from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\models\onboarding.py")
txt = p.read_text(encoding="utf-8")

old = '    codigo_postal = Column(String(20), nullable=True)'
new = '''    codigo_postal = Column(String(20), nullable=True)
    estado_negocio = Column(String(100), nullable=True)'''

if "estado_negocio" not in txt:
    txt = txt.replace(old, new)
    p.write_text(txt, encoding="utf-8")
    print("OK estado_negocio agregado al modelo")
else:
    print("Ya existía")
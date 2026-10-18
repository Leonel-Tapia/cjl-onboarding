from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\models\onboarding.py")
txt = p.read_text(encoding="utf-8")

old = '    version_documento = Column(String(20), default="v1.0", nullable=True)'
new = '''    version_documento = Column(String(20), default="v1.0", nullable=True)
    # Datos del negocio (llenados por el cliente)
    nombre_negocio = Column(String(200), nullable=True)
    ciudad = Column(String(100), nullable=True)
    codigo_postal = Column(String(20), nullable=True)
    telefono_negocio = Column(String(40), nullable=True)'''

if "nombre_negocio" not in txt:
    txt = txt.replace(old, new)
    p.write_text(txt, encoding="utf-8")
    print("OK modelo actualizado con campos de negocio")
else:
    print("Ya existían los campos")
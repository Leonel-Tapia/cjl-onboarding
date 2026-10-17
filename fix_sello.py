from pathlib import Path

# 1. Corregir el modelo
p_model = Path(r"C:\cjl_onboarding\app\models\onboarding.py")
txt_model = p_model.read_text(encoding="utf-8")

old1 = 'autoriza_cliente_sello = Column(String(200), nullable=True)'
new1 = 'autoriza_cliente_sello = Column(Text, nullable=True)'

if old1 in txt_model:
    txt_model = txt_model.replace(old1, new1)
    print("Modelo: sello de cliente cambiado a Text")
else:
    print("Modelo: NO se encontro sello de cliente")

old2 = 'autoriza_cjl_sello = Column(String(200), nullable=True)'
new2 = 'autoriza_cjl_sello = Column(Text, nullable=True)'

if old2 in txt_model:
    txt_model = txt_model.replace(old2, new2)
    print("Modelo: sello CJL cambiado a Text")

p_model.write_text(txt_model, encoding="utf-8")

# 2. Corregir la base de datos de Railway
sql = '''
ALTER TABLE onboarding_optiglass ALTER COLUMN autoriza_cliente_sello TYPE TEXT;
ALTER TABLE onboarding_optiglass ALTER COLUMN autoriza_cjl_sello TYPE TEXT;
'''
Path(r"C:\cjl_onboarding\alter_sello.sql").write_text(sql, encoding="utf-8")
print("Archivo alter_sello.sql creado")
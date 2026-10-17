from pathlib import Path
p = Path(r"C:\cjl_onboarding\app\database.py")
txt = p.read_text(encoding="utf-8")
old = 'if DATABASE_URL.startswith("postgres://"):\n    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)'
new = 'if DATABASE_URL.startswith("postgres://"):\n    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)\n\nif not DATABASE_URL.startswith("postgresql+psycopg2://"):\n    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)'
if old in txt:
    txt = txt.replace(old, new)
    p.write_text(txt, encoding="utf-8")
    print("OK codigo arreglado")
else:
    print("NO encontrado - dime")
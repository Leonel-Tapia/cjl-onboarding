from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\routers\onboarding.py")
txt = p.read_text(encoding="utf-8")

old = '''def generate_id_interno(db: Session) -> str:
    year = datetime.utcnow().year
    count = db.query(OnboardingOptiGlass).filter(OnboardingOptiGlass.id_interno.like(f"CJL-OPT-{year}-%")).count()
    return f"CJL-OPT-{year}-{count + 1:04d}"'''

new = '''def generate_id_interno(db: Session) -> str:
    year = datetime.utcnow().year
    prefix = f"CJL-OPT-{year}-"
    # Usamos func.substr y startswith para evitar problemas con el wildcard % en Postgres
    from sqlalchemy import func
    count = db.query(OnboardingOptiGlass).filter(
        func.substr(OnboardingOptiGlass.id_interno, 1, len(prefix)) == prefix
    ).count()
    return f"{prefix}{count + 1:04d}"'''

if old in txt:
    txt = txt.replace(old, new)
    p.write_text(txt, encoding="utf-8")
    print("OK generate_id_interno corregido")
else:
    print("NO encontrado")
from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\routers\onboarding.py")
txt = p.read_text(encoding="utf-8")

# Buscamos la función actual
old = '''def generate_id_interno(db: Session) -> str:
    year = datetime.utcnow().year
    prefix = f"CJL-OPT-{year}-"
    # Usamos func.substr y startswith para evitar problemas con el wildcard % en Postgres
    from sqlalchemy import func
    count = db.query(OnboardingOptiGlass).filter(
        func.substr(OnboardingOptiGlass.id_interno, 1, len(prefix)) == prefix
    ).count()
    return f"{prefix}{count + 1:04d}"'''

new = '''def generate_id_interno(db: Session) -> str:
    year = datetime.utcnow().year
    prefix = f"CJL-OPT-{year}-"
    
    # Obtenemos todos los IDs de este año (traerlos a Python evita problemas de compatibilidad SQL)
    registros = db.query(OnboardingOptiGlass.id_interno).all()
    existentes = [r[0] for r in registros if r[0] and r[0].startswith(prefix)]
    
    if not existentes:
        return f"{prefix}0001"
        
    # Encontramos el número más alto y le sumamos 1
    max_num = 0
    for e in existentes:
        try:
            num = int(e.split("-")[-1])
            if num > max_num:
                max_num = num
        except ValueError:
            pass
            
    return f"{prefix}{max_num + 1:04d}"'''

if old in txt:
    txt = txt.replace(old, new)
    p.write_text(txt, encoding="utf-8")
    print("OK generate_id_interno corregido definitivamente")
else:
    print("NO encontrado - revisar manualmente")
from pathlib import Path
from sqlalchemy import func

p = Path(r"C:\cjl_onboarding\app\routers\onboarding.py")
txt = p.read_text(encoding="utf-8")

old = '''def generate_id_interno(db: Session) -> str:
    year = datetime.utcnow().year
    prefix = f"CJL-OPT-{year}-"
    count = db.query(OnboardingOptiGlass).filter(OnboardingOptiGlass.id_interno.like(f"{prefix}%")).count()
    return f"{prefix}{count + 1:04d}"'''

new = '''def generate_id_interno(db: Session) -> str:
    year = datetime.utcnow().year
    prefix = f"CJL-OPT-{year}-"
    
    # Pedir a la BD el ID más alto que exista con este prefijo
    ultimo_id = db.query(func.max(OnboardingOptiGlass.id_interno)).filter(
        OnboardingOptiGlass.id_interno.like(f"{prefix}%")
    ).scalar()
    
    if ultimo_id:
        try:
            numero = int(ultimo_id.split("-")[-1])
            return f"{prefix}{numero + 1:04d}"
        except ValueError:
            pass
            
    return f"{prefix}0001"'''

if old in txt:
    txt = txt.replace(old, new)
    p.write_text(txt, encoding="utf-8")
    print("OK generate_id_interno arreglado de forma definitiva")
else:
    print("NO encontrado - buscando variante")
    # Por si el codigo actual tiene otra forma
    import re
    pattern = re.compile(r'def generate_id_interno\(db: Session\) -> str:.*?return f"\{prefix\}\{.*?\}"', re.DOTALL)
    if pattern.search(txt):
        txt = pattern.sub(new, txt)
        p.write_text(txt, encoding="utf-8")
        print("OK generate_id_interno arreglado (variante regex)")
    else:
        print("No se pudo encontrar la funcion")
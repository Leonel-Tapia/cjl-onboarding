from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\templates\onboarding_form.html")
txt = p.read_text(encoding="utf-8")

# Insertar la nueva sección antes de Pricing Structure
old = '    <div class="card section-card"><div class="card-body">\n        <h5 class="section-title"><i class="fas fa-dollar-sign"></i> 1. Pricing Structure</h5>'
new = '''    <div class="card section-card"><div class="card-body">
        <h5 class="section-title"><i class="fas fa-building"></i> Business Information</h5>
        <div class="row g-3">
            <div class="col-md-6"><label class="form-label required-label">Business Name</label><input type="text" class="form-control" name="nombre_negocio" required></div>
            <div class="col-md-6"><label class="form-label required-label">Phone</label><input type="text" class="form-control" name="telefono_negocio" oninput="formatPhone(this)" required></div>
            <div class="col-md-6"><label class="form-label">City</label><input type="text" class="form-control" name="ciudad" placeholder="e.g. McAllen"></div>
            <div class="col-md-6"><label class="form-label">ZIP Code</label><input type="text" class="form-control" name="codigo_postal" placeholder="e.g. 78501"></div>
        </div>
    </div></div>
    <div class="card section-card"><div class="card-body">
        <h5 class="section-title"><i class="fas fa-dollar-sign"></i> 1. Pricing Structure</h5>'''

if 'Business Information' not in txt:
    # Intentar con \n literales
    if '\n' in txt:
        old = old.replace('\\n', '\n')
    txt = txt.replace(old, new)
    p.write_text(txt, encoding="utf-8")
    print("Sección Business Information agregada")
else:
    print("La sección ya existía")

# Quitar el título hardcodeado "OptiGlass+ McAllen Texas"
old_title = '<p class="text-muted mb-4">OptiGlass+ McAllen Texas &times; CJL Creative Ideas Marketing</p>'
new_title = '<p class="text-muted mb-4">Onboarding Document &times; CJL Creative Ideas Marketing</p>'

if old_title in txt:
    txt = txt.replace(old_title, new_title)
    p.write_text(txt, encoding="utf-8")
    print("Título hardcodeado removido")

print("OK formulario actualizado")
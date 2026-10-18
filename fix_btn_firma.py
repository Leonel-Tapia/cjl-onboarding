from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\templates\onboarding_form.html")
txt = p.read_text(encoding="utf-8")

# 1. Botón HTML (justo después de <form method="POST">)
old_form = '<form method="POST" action="/onboarding/submit" id="onboardingForm">'
new_form = '''<form method="POST" action="/onboarding/submit" id="onboardingForm">
    <!-- Botón flotante para ir a la firma -->
    <a href="#authSection" id="goToSignBtn" style="position: fixed; bottom: 30px; right: 30px; z-index: 999; background: #198754; color: white; padding: 15px 20px; border-radius: 50px; text-decoration: none; box-shadow: 0 4px 15px rgba(0,0,0,0.3); font-weight: bold; display: flex; align-items: center; gap: 8px; transition: 0.2s;" onmouseover="this.style.background=\'#157347\'" onmouseout="this.style.background=\'#198754\'">
        <span>Ir a la firma</span>
        <i class="fas fa-arrow-down"></i>
    </a>'''

if 'id="goToSignBtn"' not in txt:
    txt = txt.replace(old_form, new_form)
    print("Botón flotante agregado")

# 2. Agregar id="authSection" a la sección de autorización
old_auth = '<div class="card section-card border-success mt-4"><div class="card-body">'
new_auth = '<div class="card section-card border-success mt-4" id="authSection"><div class="card-body">'

if 'id="authSection"' not in txt:
    txt = txt.replace(old_auth, new_auth)
    print("ID de sección de firma agregado")

# 3. Agregar scroll suave (CSS global)
old_style = '<style>'
# Buscar si ya hay un <style> en el template o en base.html
if 'scroll-behavior: smooth' not in txt:
    # Intentar agregar un style al inicio del content block
    marker = '<h2 class="mb-1">Onboarding Document</h2>'
    style_block = '''<style>
html { scroll-behavior: smooth; }
#authSection { scroll-margin-top: 20px; }
@media (max-width: 768px) {
    #goToSignBtn span { display: none; }
    #goToSignBtn { padding: 15px; border-radius: 50%; }
}
</style>
<h2 class="mb-1">Onboarding Document</h2>'''
    txt = txt.replace(marker, style_block)
    print("Scroll suave agregado")

p.write_text(txt, encoding="utf-8")
print("OK formulario actualizado")
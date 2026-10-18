from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\templates\onboarding_form.html")
txt = p.read_text(encoding="utf-8")

old = '''            <div class="col-md-6"><label class="form-label">City</label><input type="text" class="form-control" name="ciudad" placeholder="e.g. McAllen"></div>
            <div class="col-md-6"><label class="form-label">ZIP Code</label><input type="text" class="form-control" name="codigo_postal" placeholder="e.g. 78501"></div>'''

new = '''            <div class="col-md-4"><label class="form-label">City</label><input type="text" class="form-control" name="ciudad" placeholder="e.g. McAllen"></div>
            <div class="col-md-4"><label class="form-label">State</label><input type="text" class="form-control" name="estado_negocio" placeholder="e.g. TX" maxlength="2" style="text-transform: uppercase;"></div>
            <div class="col-md-4"><label class="form-label">ZIP Code</label><input type="text" class="form-control" name="codigo_postal" placeholder="e.g. 78501"></div>'''

if 'name="estado_negocio"' not in txt:
    txt = txt.replace(old, new)
    p.write_text(txt, encoding="utf-8")
    print("OK campo State agregado al HTML")
else:
    print("Ya existía")
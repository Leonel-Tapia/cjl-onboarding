from pathlib import Path

# 1. Modificar el Router para enviar la fecha con el formato deseado
p_router = Path(r"C:\cjl_onboarding\app\routers\onboarding.py")
txt_r = p_router.read_text(encoding="utf-8")

# Buscar la linea actual (puede ser fecha_version o fecha_actual)
import re
old_route = re.search(r'fecha_actual = .*', txt_r)

if old_route:
    # Reemplazar con el formato exacto
    new_route = 'fecha_actual = datetime.now().strftime("Última actualización: %d de %B de %Y - %I:%M %p")'
    txt_r = txt_r.replace(old_route.group(0), new_route)
    p_router.write_text(txt_r, encoding="utf-8")
    print("Router actualizado con nuevo formato")

# 2. Modificar el HTML para mostrar el texto correcto
p_html = Path(r"C:\cjl_onboarding\app\templates\onboarding_form.html")
txt_h = p_html.read_text(encoding="utf-8")

# Buscar el bloque del timestamp
old_span = '<i class="fas fa-clock"></i> \n                <strong>Fecha de registro:</strong> \n                <span>{{ fecha_version }}</span>'

# Si el reemplazo anterior borró los saltos de línea, intentar con otra variante
if old_span not in txt_h:
    old_span = '<i class="fas fa-clock"></i> <strong>Fecha de registro:</strong> <span>{{ fecha_version }}</span>'

new_span = '<i class="fas fa-history"></i> <strong>{{ fecha_version }}</strong>'

if old_span in txt_h:
    txt_h = txt_h.replace(old_span, new_span)
    p_html.write_text(txt_h, encoding="utf-8")
    print("HTML actualizado con nuevo diseño")
else:
    # Si no encuentra, buscar el span solo
    old_span2 = '<span>{{ fecha_version }}</span>'
    new_span2 = '<span style="font-weight: 600; color: #198754;">{{ fecha_version }}</span>'
    if old_span2 in txt_h:
        txt_h = txt_h.replace(old_span2, new_span2)
        p_html.write_text(txt_h, encoding="utf-8")
        print("HTML actualizado con color verde")

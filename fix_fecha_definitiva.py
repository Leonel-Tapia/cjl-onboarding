from pathlib import Path
from datetime import datetime

p = Path(r"C:\cjl_onboarding\app\templates\onboarding_form.html")
txt = p.read_text(encoding="utf-8")

# 1. Generar el texto de la fecha actual
meses = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
ahora = datetime.now()
fecha_str = f"{ahora.day} de {meses[ahora.month]} de {ahora.year} - {ahora.strftime('%I:%M %p')}"
texto_final = f"<i class=\"fas fa-history\"></i> <strong>Última actualización: {fecha_str}</strong>"

# 2. Reemplazar el span viejo por el texto fijo
old = '<span id="fechaRegistro"></span>'
if old in txt:
    txt = txt.replace(old, texto_final)
    print("HTML actualizado con fecha fija")

# También buscar si quedó el texto de "Fecha de registro"
old_label = '<strong>Fecha de registro:</strong>'
if old_label in txt:
    txt = txt.replace(old_label, '')

# 3. Limpiar el JS que intentaba llenar la fecha
import re
# Borrar el bloque JS que busca fechaRegistro
txt = re.sub(r"// Llenar la fecha de registro al cargar.*?fechaSpan\.textContent = ahora\.toLocaleDateString\('es-MX', opciones\);\s*\}\s*", "", txt, flags=re.DOTALL)
txt = re.sub(r"// Actualizar la fecha exacta cuando se envía el formulario.*?\}\s*\}\s*", "", txt, flags=re.DOTALL)

p.write_text(txt, encoding="utf-8")
print("OK Todo listo. Fecha fija puesta y JS limpiado.")
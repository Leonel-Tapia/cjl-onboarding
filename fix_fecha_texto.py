from pathlib import Path
from datetime import datetime

p = Path(r"C:\cjl_onboarding\app\templates\onboarding_form.html")
txt = p.read_text(encoding="utf-8")

# Generar la fecha actual formateada
meses = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
ahora = datetime.now()
fecha_str = f"{ahora.day} de {meses[ahora.month]} de {ahora.year} - {ahora.strftime('%I:%M %p')}"

# Buscar la etiqueta actual y agregarle la fecha
old_label = '<i class="fas fa-history"></i> <strong>Última actualización:</strong>'
new_label = f'<i class="fas fa-history"></i> <strong>Última actualización: {fecha_str}</strong>'

if old_label in txt:
    txt = txt.replace(old_label, new_label)
    p.write_text(txt, encoding="utf-8")
    print(f"OK: Fecha agregada -> {fecha_str}")
else:
    # Intentar variante por si los espacios o comillas cambiaron
    old_label2 = 'Última actualización:'
    if old_label2 in txt and fecha_str not in txt:
        txt = txt.replace(old_label2, f'Última actualización: {fecha_str}')
        p.write_text(txt, encoding="utf-8")
        print(f"OK: Fecha agregada por variante -> {fecha_str}")
    else:
        print("NO se encontro el texto de la etiqueta")
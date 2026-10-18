from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\templates\onboarding_form.html")
txt = p.read_text(encoding="utf-8")

# Buscamos el final exacto (con el doble </html>)
old_end = """</script>
</body>
</html>
</html>"""

new_end = """</script>
{% endblock %}
</body>
</html>"""

if old_end in txt:
    txt = txt.replace(old_end, new_end)
    p.write_text(txt, encoding="utf-8")
    print("OK: endblock agregado y html duplicado eliminado")
else:
    # Variante por si hay saltos de línea raros
    print("Variante exacta no encontrada. Buscando otra forma...")
    lines = txt.split("\n")
    # Quitar último </html> duplicado
    if lines[-1].strip() == "</html>" and lines[-2].strip() == "</html>":
        lines = lines[:-1]
        print("Html duplicado eliminado")
    # Agregar endblock antes de </body>
    for i in range(len(lines)-1, -1, -1):
        if "</body>" in lines[i]:
            lines.insert(i, "{% endblock %}")
            print("Endblock insertado")
            break
    txt = "\n".join(lines)
    p.write_text(txt, encoding="utf-8")
    print("OK: corrección aplicada por variante")
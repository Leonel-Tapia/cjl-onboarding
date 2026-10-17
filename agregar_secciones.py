from pathlib import Path

p = Path(r"C:\cjl_onboarding\app\templates\onboarding_form.html")
txt = p.read_text(encoding="utf-8")

nuevas_secciones = '''    <div class="card section-card"><div class="card-body">
        <h5 class="section-title"><i class="fas fa-shield-alt"></i> 4. Tipo de Garantías que Ofrecen</h5>
        <div class="mb-2">
            <label class="form-label d-block"><input type="checkbox" name="garantias[]" value="Fugas y filtraciones (por vida)"> Garantía contra fugas y filtraciones (de por vida)</label>
            <label class="form-label d-block"><input type="checkbox" name="garantias[]" value="Mano de obra / instalacion"> Garantía de mano de obra / instalación</label>
            <label class="form-label d-block"><input type="checkbox" name="garantias[]" value="Fabrica del vidrio"> Garantía de fábrica del vidrio</label>
            <label class="form-label d-block"><input type="checkbox" name="garantias[]" value="Molduras y empaques"> Garantía en molduras y empaques</label>
        </div>
        <div class="row g-3">
            <div class="col-md-6"><label class="form-label">Otro (especificar)</label><input type="text" class="form-control" name="garantia_otro"></div>
            <div class="col-12"><label class="form-label">Texto oficial de garantía (para usar en anuncios)</label><textarea class="form-control" name="texto_garantia_oficial" rows="2"></textarea></div>
        </div>
    </div></div>

    <div class="card section-card"><div class="card-body">
        <h5 class="section-title"><i class="fas fa-clock"></i> 5. Información Básica Operativa</h5>
        <div class="row g-3">
            <div class="col-md-3"><label class="form-label">Horario L-V</label><input type="text" class="form-control" name="horario_lv" placeholder="8:00 AM a 6:00 PM"></div>
            <div class="col-md-3"><label class="form-label">Sábado</label><input type="text" class="form-control" name="horario_sabado" placeholder="9:00 AM a 2:00 PM"></div>
            <div class="col-md-3"><label class="form-label">Domingo</label><input type="text" class="form-control" name="horario_domingo" placeholder="Cerrado"></div>
            <div class="col-md-3"><label class="form-label">Días laborales / Cerrado</label><input type="text" class="form-control" name="dias_laborales"></div>
        </div>
        <hr>
        <div class="row g-3">
            <div class="col-md-3"><label class="form-label">¿Servicio móvil a domicilio?</label><select class="form-select" name="servicio_movil"><option value="No">No</option><option value="Si">Sí</option></select></div>
            <div class="col-md-3"><label class="form-label">Radio en millas</label><input type="text" class="form-control" name="radio_millas" placeholder="ej. 20 millas"></div>
            <div class="col-md-6"><label class="form-label">Dirección taller</label><input type="text" class="form-control" name="direccion_taller"></div>
        </div>
        <hr>
        <label class="form-label fw-bold">Tiempo promedio de instalación</label>
        <div class="row g-3">
            <div class="col-md-3"><label class="form-label small">Parabrisas (min)</label><input type="text" class="form-control" name="tiempo_parabrisas" placeholder="ej. 60"></div>
            <div class="col-md-3"><label class="form-label small">Lateral (min)</label><input type="text" class="form-control" name="tiempo_lateral" placeholder="ej. 30"></div>
            <div class="col-md-3"><label class="form-label small">Trasero (min)</label><input type="text" class="form-control" name="tiempo_trasero" placeholder="ej. 45"></div>
            <div class="col-md-3"><label class="form-label small">¿Cuántos instaladores disponibles?</label><input type="text" class="form-control" name="instaladores_disponibles" placeholder="ej. 3"></div>
        </div>
    </div></div>

    <div class="card section-card"><div class="card-body">
        <h5 class="section-title"><i class="fas fa-map-marked-alt"></i> 6. Áreas de Cobertura</h5>
        <div class="row g-3">
            <div class="col-12"><label class="form-label">Ciudades que cubren (McAllen, Edinburg, Mission, Pharr, etc.)</label><input type="text" class="form-control" name="ciudades_cobertura"></div>
            <div class="col-12"><label class="form-label">Zip codes que cubren</label><input type="text" class="form-control" name="zip_codes"></div>
            <div class="col-12"><label class="form-label">¿Zonas donde NO trabajan?</label><input type="text" class="form-control" name="zonas_no_trabajan"></div>
        </div>
        <hr>
        <div class="row g-3">
            <div class="col-md-4"><label class="form-label">¿Cobran extra por móvil lejano?</label><select class="form-select" name="cobran_extra_movil"><option value="No">No</option><option value="Si">Sí</option></select></div>
            <div class="col-md-4"><label class="form-label">¿Cuánto? ($)</label><input type="text" class="form-control" name="cuanto_extra" placeholder="ej. 25"></div>
        </div>
    </div></div>

    <div class="card section-card"><div class="card-body">
        <h5 class="section-title"><i class="fas fa-tags"></i> 7. Promociones Activas</h5>
        <div class="row g-3">
            <div class="col-md-6"><label class="form-label">Promoción actual</label><input type="text" class="form-control" name="promocion_actual"></div>
            <div class="col-md-6"><label class="form-label">Descuento por pago en efectivo</label><input type="text" class="form-control" name="descuento_efectivo" placeholder="ej. 10%"></div>
            <div class="col-md-4"><label class="form-label">Promo ADAS / Calibración</label><input type="text" class="form-control" name="promo_adas"></div>
            <div class="col-md-4"><label class="form-label">Promo por referidos</label><input type="text" class="form-control" name="promo_referidos"></div>
            <div class="col-md-4"><label class="form-label">Otra promo</label><input type="text" class="form-control" name="otra_promo"></div>
        </div>
    </div></div>

    <div class="card section-card"><div class="card-body">
        <h5 class="section-title"><i class="fas fa-credit-card"></i> 8. Métodos de Pago y Aseguradoras</h5>
        <label class="form-label fw-bold">Métodos de pago aceptados</label>
        <div class="mb-2">
            <label class="form-label d-inline me-3"><input type="checkbox" name="metodos_pago[]" value="Efectivo"> Efectivo</label>
            <label class="form-label d-inline me-3"><input type="checkbox" name="metodos_pago[]" value="Zelle"> Zelle</label>
            <label class="form-label d-inline me-3"><input type="checkbox" name="metodos_pago[]" value="Tarjeta credito/debito"> Tarjeta crédito/débito</label>
            <label class="form-label d-inline me-3"><input type="checkbox" name="metodos_pago[]" value="Transferencia"> Transferencia</label>
            <label class="form-label d-inline"><input type="checkbox" name="metodos_pago[]" value="Financiamiento"> Financiamiento</label>
        </div>
        <hr>
        <div class="row g-3">
            <div class="col-md-3"><label class="form-label">¿Trabajan con aseguradoras?</label><select class="form-select" name="trabajan_aseguradoras"><option value="No">No</option><option value="Si">Sí</option></select></div>
            <div class="col-md-9">
                <label class="form-label">¿Cuáles aseguradoras?</label><br>
                <label class="form-label d-inline me-3"><input type="checkbox" name="aseguradoras[]" value="State Farm"> State Farm</label>
                <label class="form-label d-inline me-3"><input type="checkbox" name="aseguradoras[]" value="Geico"> Geico</label>
                <label class="form-label d-inline me-3"><input type="checkbox" name="aseguradoras[]" value="Progressive"> Progressive</label>
                <label class="form-label d-inline me-3"><input type="checkbox" name="aseguradoras[]" value="Allstate"> Allstate</label>
                <label class="form-label d-inline"><input type="checkbox" name="aseguradoras[]" value="Otra"> Otra</label>
            </div>
            <div class="col-md-6"><label class="form-label">¿Manejan deducibles?</label><input type="text" class="form-control" name="manejan_deducibles"></div>
            <div class="col-md-6"><label class="form-label">¿Aceptan seguro con cita previa?</label><select class="form-select" name="aceptan_seguro_cita"><option value="No">No</option><option value="Si">Sí</option></select></div>
            <div class="col-12"><label class="form-label">¿Cómo cobran claims?</label><textarea class="form-control" name="como_cobran_claims" rows="2"></textarea></div>
        </div>
    </div></div>

    <div class="card section-card"><div class="card-body">
        <h5 class="section-title"><i class="fas fa-camera"></i> 9. Material Visual Requerido</h5>
        <p class="text-muted small">Marque lo que ya tiene listo para compartir:</p>
        <label class="form-label d-block"><input type="checkbox" name="material_visual[]" value="Logotipos PNG + vector"> Logotipos en PNG transparente + vector AI/EPS/PDF</label>
        <label class="form-label d-block"><input type="checkbox" name="material_visual[]" value="15-20 fotos trabajos reales"> 15-20 fotos de trabajos reales (instalaciones, taller, móvil)</label>
        <label class="form-label d-block"><input type="checkbox" name="material_visual[]" value="3-5 videos cortos"> 3-5 videos cortos verticales de 15-30 seg</label>
        <label class="form-label d-block"><input type="checkbox" name="material_visual[]" value="Fotos antes/despues"> Fotos antes/después</label>
        <label class="form-label d-block"><input type="checkbox" name="material_visual[]" value="Fotos equipo/uniformes"> Fotos del equipo / uniformes</label>
        <div class="mt-2"><label class="form-label">Notas sobre el material</label><textarea class="form-control" name="notas_material" rows="2"></textarea></div>
    </div></div>

    <div class="card section-card"><div class="card-body">
        <h5 class="section-title"><i class="fas fa-file-contract"></i> 10. Condiciones y Términos del Servicio CJL</h5>
        <ol class="small text-muted mb-3">
            <li>Depósito inicial: $500 USD para arranque + presupuesto de ads.</li>
            <li>Aprobación de contenido digital: máx 24h.</li>
            <li>Reporte semanal: cada lunes.</li>
            <li>Un mes gratis de prueba de sistema POS: valor $297 USD.</li>
            <li>Número de coordinación durante el día (8am-6pm hora McAllen).</li>
            <li>Propiedad: Todas las campañas se crean en el Business Manager del cliente.</li>
            <li>Modelo CJL: $500/mes gestión + $30-$40 solo por cita PAGADA y completada.</li>
            <li>Política de cancelación de citas.</li>
        </ol>
        <label class="form-label fw-bold"><input type="checkbox" name="acepta_terminos" required> Acepto los términos y condiciones del servicio</label>
    </div></div>

'''

old = '''    <div class="card section-card border-success mt-4"><div class="card-body">
        <h5 class="section-title text-success"><i class="fas fa-check-circle"></i> Client Authorization</h5>'''

new = nuevas_secciones + old

if "4. Tipo de Garant" not in txt:
    txt = txt.replace(old, new)
    p.write_text(txt, encoding="utf-8")
    print("OK 7 secciones agregadas")
else:
    print("Ya existian")

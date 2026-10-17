from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from xhtml2pdf import pisa
from io import BytesIO

from app.database import get_db
from app.models.onboarding import OnboardingOptiGlass
from app.models.vehiculo_catalogo import VehiculoCatalogo
from app.models.pieza_catalogo import PiezaCatalogo

router = APIRouter(prefix="/onboarding", tags=["onboarding"])
templates = Jinja2Templates(directory="app/templates")
ADMIN_KEY = "CJL_Admin_2026"

def generate_id_interno(db: Session) -> str:
    year = datetime.utcnow().year
    prefix = f"CJL-OPT-{year}-"
    # Usamos func.substr y startswith para evitar problemas con el wildcard % en Postgres
    from sqlalchemy import func
    count = db.query(OnboardingOptiGlass).filter(
        func.substr(OnboardingOptiGlass.id_interno, 1, len(prefix)) == prefix
    ).count()
    return f"{prefix}{count + 1:04d}"

@router.get("", response_class=HTMLResponse)
async def show_form(request: Request, db: Session = Depends(get_db)):
    vehiculos = db.query(VehiculoCatalogo).filter(VehiculoCatalogo.activo == True).order_by(VehiculoCatalogo.marca, VehiculoCatalogo.modelo).all()
    piezas_raw = db.query(PiezaCatalogo).filter(PiezaCatalogo.activo == True).all()
    
    grupos = {}
    for p in piezas_raw:
        prefijo = p.part_dw[:2] if len(p.part_dw) >= 2 else "OT"
        nombres = {"DW": "Domestic Windshield", "FW": "Foreign Windshield", "DD": "Domestic Door", "DB": "Domestic Back Window", "FD": "Foreign Door", "LD": "Left Door", "RD": "Right Door", "BD": "Back Window"}
        nombre_grupo = nombres.get(prefijo, "Other Parts")
        if nombre_grupo not in grupos:
            grupos[nombre_grupo] = []
        grupos[nombre_grupo].append(p)
    
    return templates.TemplateResponse(request=request, name="onboarding_form.html", context={"vehiculos": vehiculos, "piezas_agrupadas": grupos})

@router.post("/submit")
async def submit_form(
    request: Request, db: Session = Depends(get_db),
    email_cotizaciones: str = Form(...), telefono_cotizaciones: Optional[str] = Form(None),
    sistema_cotizaciones: Optional[str] = Form(None), tiempo_respuesta: Optional[str] = Form(None),
    numero_principal_grupo: Optional[str] = Form(None), texto_garantia_oficial: Optional[str] = Form(None),
    horario_lv: Optional[str] = Form(None), horario_sabado: Optional[str] = Form(None), horario_domingo: Optional[str] = Form(None),
    servicio_movil: Optional[str] = Form("false"), radio_millas: Optional[str] = Form(None), direccion_taller: Optional[str] = Form(None),
    tiempo_parabrisas: Optional[str] = Form(None), tiempo_lateral: Optional[str] = Form(None), tiempo_trasero: Optional[str] = Form(None),
    instaladores_disponibles: Optional[str] = Form(None), ciudades_cobertura: Optional[str] = Form(None), zip_codes: Optional[str] = Form(None),
    zonas_no_trabajan: Optional[str] = Form(None), cobran_extra_movil: Optional[str] = Form("false"), cuanto_extra: Optional[str] = Form(None),
    promocion_actual: Optional[str] = Form(None), descuento_efectivo: Optional[str] = Form(None), promo_adas: Optional[str] = Form(None),
    promo_referidos: Optional[str] = Form(None), otra_promo: Optional[str] = Form(None), trabajan_aseguradoras: Optional[str] = Form("false"),
    manejan_deducibles: Optional[str] = Form(None), como_cobran_claims: Optional[str] = Form(None), aceptan_seguro_cita: Optional[str] = Form("false"),
    notas_material: Optional[str] = Form(None), autoriza_cliente_nombre: str = Form(...), autoriza_cliente_sello: Optional[str] = Form(None),
):
    form = await request.form()
    garantias_json = {"fugas": "garantia_fugas" in form, "mano_obra": "garantia_mano_obra" in form, "fabrica": "garantia_fabrica" in form, "molduras": "garantia_molduras" in form, "otro": "garantia_otro" in form}
    metodos_pago_json = {"efectivo": "pago_efectivo" in form, "zelle": "pago_zelle" in form, "tarjeta": "pago_tarjeta" in form, "transferencia": "pago_transferencia" in form, "financiamiento": "pago_financiamiento" in form}
    aseguradoras_json = {"state_farm": "seguro_state_farm" in form, "geico": "seguro_geico" in form, "progressive": "seguro_progressive" in form, "allstate": "seguro_allstate" in form, "otra": "seguro_otra" in form}

    partes = form.getlist("precio_parte[]")
    vehiculos_form = form.getlist("precio_vehiculo[]")
    costos = form.getlist("precio_costo[]")
    ventas = form.getlist("precio_venta[]")
    precios = []
    for i in range(len(partes)):
        if partes[i] or vehiculos_form[i] or costos[i] or ventas[i]:
            try: c = float(costos[i]) if costos[i] else 0; v = float(ventas[i]) if ventas[i] else 0
            except ValueError: c, v = 0, 0
            ganancia = round(v - c, 2)
            margen = round((ganancia / c) * 100, 1) if c > 0 else 0
            precios.append({"parte": partes[i], "vehiculo": vehiculos_form[i], "costo": c, "venta": v, "ganancia": ganancia, "margen": margen})

    id_interno = generate_id_interno(db)
    client_ip = request.client.host if request.client else None

    registro = OnboardingOptiGlass(
        id_interno=id_interno, fecha_submit=datetime.utcnow(), estado="pending", precios_json=precios,
        email_cotizaciones=email_cotizaciones, telefono_cotizaciones=telefono_cotizaciones, sistema_cotizaciones=sistema_cotizaciones, tiempo_respuesta=tiempo_respuesta,
        numero_principal_grupo=numero_principal_grupo, garantias_json=garantias_json, texto_garantia_oficial=texto_garantia_oficial,
        horario_lv=horario_lv, horario_sabado=horario_sabado, horario_domingo=horario_domingo, servicio_movil=(servicio_movil == "true"), radio_millas=radio_millas, direccion_taller=direccion_taller,
        tiempo_parabrisas=tiempo_parabrisas, tiempo_lateral=tiempo_lateral, tiempo_trasero=tiempo_trasero, instaladores_disponibles=instaladores_disponibles,
        ciudades_cobertura=ciudades_cobertura, zip_codes=zip_codes, zonas_no_trabajan=zonas_no_trabajan, cobran_extra_movil=(cobran_extra_movil == "true"), cuanto_extra=cuanto_extra,
        promocion_actual=promocion_actual, descuento_efectivo=descuento_efectivo, promo_adas=promo_adas, promo_referidos=promo_referidos, otra_promo=otra_promo,
        metodos_pago_json=metodos_pago_json, trabajan_aseguradoras=(trabajan_aseguradoras == "true"), aseguradoras_json=aseguradoras_json, manejan_deducibles=manejan_deducibles, como_cobran_claims=como_cobran_claims, aceptan_seguro_cita=(aceptan_seguro_cita == "true"),
        material_recibido=("material_recibido" in form), notas_material=notas_material, acepta_terminos=("acepta_terminos" in form),
        autoriza_cliente=True, autoriza_cliente_nombre=autoriza_cliente_nombre, autoriza_cliente_sello=autoriza_cliente_sello, autoriza_cliente_fecha=datetime.utcnow(), autoriza_cliente_ip=client_ip,
    )
    db.add(registro); db.commit(); db.refresh(registro)
    return RedirectResponse(url=f"/onboarding/success/{registro.id_interno}", status_code=303)

@router.get("/pdf/{id_interno}")
async def generate_pdf(id_interno: str, request: Request, db: Session = Depends(get_db)):
    registro = db.query(OnboardingOptiGlass).filter(OnboardingOptiGlass.id_interno == id_interno).first()
    if not registro: return HTMLResponse(content="Registro no encontrado", status_code=404)
    template = templates.get_template("pdf_template.html")
    html_content = template.render(registro=registro)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), result)
    if not pdf.err:
        result.seek(0)
        return StreamingResponse(result, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=Onboarding_{id_interno}.pdf"})
    return HTMLResponse(content="Error generando PDF", status_code=500)

@router.get("/success/{id_interno}", response_class=HTMLResponse)
async def success(id_interno: str, request: Request):
    return templates.TemplateResponse(request=request, name="onboarding_success.html", context={"id_interno": id_interno})

@router.get("/admin/history", response_class=HTMLResponse)
async def admin_history(request: Request, key: str = "", db: Session = Depends(get_db)):
    if key != ADMIN_KEY: return HTMLResponse(content="<h3>Access Denied. Invalid Key.</h3>", status_code=403)
    registros = db.query(OnboardingOptiGlass).order_by(OnboardingOptiGlass.fecha_submit.desc()).all()
    return templates.TemplateResponse(request=request, name="admin_history.html", context={"registros": registros})

@router.get("/admin/view/{id_interno}", response_class=HTMLResponse)
async def admin_view(id_interno: str, request: Request, key: str = "", db: Session = Depends(get_db)):
    if key != ADMIN_KEY: return HTMLResponse(content="<h3>Access Denied.</h3>", status_code=403)
    registro = db.query(OnboardingOptiGlass).filter(OnboardingOptiGlass.id_interno == id_interno).first()
    return templates.TemplateResponse(request=request, name="admin_view.html", context={"registro": registro})

@router.post("/admin/update_status/{id_interno}")
async def admin_update_status(id_interno: str, request: Request, key: str = "", nuevo_estado: str = Form(...), cambiado_por: str = Form(...), db: Session = Depends(get_db)):
    if key != ADMIN_KEY: return HTMLResponse(content="<h3>Access Denied.</h3>", status_code=403)
    registro = db.query(OnboardingOptiGlass).filter(OnboardingOptiGlass.id_interno == id_interno).first()
    if registro:
        registro.estado = nuevo_estado; registro.status_changed_by = cambiado_por; registro.status_changed_at = datetime.utcnow(); db.commit()
    return RedirectResponse(url=f"/onboarding/admin/view/{id_interno}?key={ADMIN_KEY}", status_code=303)

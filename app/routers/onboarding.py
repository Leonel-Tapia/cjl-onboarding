from fastapi import APIRouter, Request, Depends, Form
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

def enviar_correo_notificacion(registro):
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    if not smtp_email or not smtp_password:
        print("Faltan credenciales SMTP")
        return

    msg = MIMEMultipart()
    msg['From'] = smtp_email
    msg['To'] = smtp_email
    msg['Subject'] = f"Nuevo Onboarding: {registro.id_interno}"

    body = f"""
    <h3>Nuevo formulario recibido</h3>
    <p><strong>ID:</strong> {registro.id_interno}</p>
    <p><strong>Email:</strong> {registro.email_cotizaciones}</p>
    <p><strong>Fecha:</strong> {registro.fecha_submit}</p>
    """
    msg.attach(MIMEText(body, 'html'))

    try:
        import ssl
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, smtp_email, msg.as_string())
        server.quit()
        print("✅ Correo enviado con éxito.")
    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")

from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import json
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
    
    # Fix: Usar func.max directo sin LIKE (Lección aprendida)
    ultimo_id = db.query(func.max(OnboardingOptiGlass.id_interno)).scalar()
    
    if ultimo_id and ultimo_id.startswith(prefix):
        try:
            numero = int(ultimo_id.split("-")[-1])
            return f"{prefix}{numero + 1:04d}"
        except ValueError:
            pass
            
    return f"{prefix}0001"

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
    nombre_negocio: str = Form(...), telefono_negocio: Optional[str] = Form(None),
    ciudad: Optional[str] = Form(None), estado_negocio: Optional[str] = Form(None), codigo_postal: Optional[str] = Form(None),
    email_cotizaciones: str = Form(...), telefono_cotizaciones: Optional[str] = Form(None),
    sistema_cotizaciones: Optional[str] = Form(None), tiempo_respuesta: Optional[str] = Form(None),
    numero_principal_grupo: Optional[str] = Form(None), texto_garantia_oficial: Optional[str] = Form(None),
    horario_lv: Optional[str] = Form(None), horario_sabado: Optional[str] = Form(None), horario_domingo: Optional[str] = Form(None),
    servicio_movil: Optional[str] = Form("false"), radio_millas: Optional[str] = Form(None), direccion_taller: Optional[str] = Form(None),
    tiempo_parabrisas: Optional[str] = Form(None), tiempo_lateral: Optional[str] = Form(None), tiempo_trasero: Optional[str] = Form(None),
    instaladores_disponibles: Optional[str] = Form(None), estado_geografico: Optional[str] = Form(None), ciudades_cobertura: Optional[str] = Form(None), zip_codes: Optional[str] = Form(None),
    zonas_no_trabajan: Optional[str] = Form(None), cobran_extra_movil: Optional[str] = Form("false"), cuanto_extra: Optional[str] = Form(None),
    promocion_actual: Optional[str] = Form(None), descuento_efectivo: Optional[str] = Form(None), promo_adas: Optional[str] = Form(None),
    promo_referidos: Optional[str] = Form(None), otra_promo: Optional[str] = Form(None), trabajan_aseguradoras: Optional[str] = Form("false"),
    manejan_deducibles: Optional[str] = Form(None), como_cobran_claims: Optional[str] = Form(None), aceptan_seguro_cita: Optional[str] = Form("false"),
    notas_material: Optional[str] = Form(None), autoriza_cliente_nombre: str = Form(...), autoriza_cliente_sello: Optional[str] = Form(None),
):
    form = await request.form()
    # Leemos los checkboxes con el mismo nombre que se puso en el HTML
    garantias_list = form.getlist("garantias[]")
    garantias_json = {"fugas": "Fugas y filtraciones (por vida)" in garantias_list, "mano_obra": "Mano de obra / instalacion" in garantias_list, "fabrica": "Fabrica del vidrio" in garantias_list, "molduras": "Molduras y empaques" in garantias_list, "otro": form.get("garantia_otro", "")}

    metodos_list = form.getlist("metodos_pago[]")
    metodos_pago_json = {"efectivo": "Efectivo" in metodos_list, "zelle": "Zelle" in metodos_list, "tarjeta": "Tarjeta credito/debito" in metodos_list, "transferencia": "Transferencia" in metodos_list, "financiamiento": "Financiamiento" in metodos_list}

    aseguradoras_list = form.getlist("aseguradoras[]")
    aseguradoras_json = {"state_farm": "State Farm" in aseguradoras_list, "geico": "Geico" in aseguradoras_list, "progressive": "Progressive" in aseguradoras_list, "allstate": "Allstate" in aseguradoras_list, "otra": "Otra" in aseguradoras_list}

    material_visual_list = form.getlist("material_visual[]")
    material_visual_json = {
        "logo": "Logo" in material_visual_list,
        "fotos_taller": "Fotos del taller" in material_visual_list,
        "fotos_trabajos": "Fotos de trabajos" in material_visual_list,
        "video": "Video" in material_visual_list,
        "otro": form.get("material_otro", "")
    }

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
        id_interno=id_interno, fecha_submit=func.now(), estado="pending", precios_json=precios if isinstance(precios, list) else json.loads(precios),
        email_cotizaciones=email_cotizaciones, telefono_cotizaciones=telefono_cotizaciones, sistema_cotizaciones=sistema_cotizaciones, tiempo_respuesta=tiempo_respuesta,
        numero_principal_grupo=numero_principal_grupo, garantias_json=garantias_json if isinstance(garantias_json, dict) else json.loads(garantias_json), texto_garantia_oficial=texto_garantia_oficial,
        horario_lv=horario_lv, horario_sabado=horario_sabado, horario_domingo=horario_domingo, servicio_movil=(servicio_movil == "true"), radio_millas=radio_millas, direccion_taller=direccion_taller,
        tiempo_parabrisas=tiempo_parabrisas, tiempo_lateral=tiempo_lateral, tiempo_trasero=tiempo_trasero, instaladores_disponibles=instaladores_disponibles,
        estado_geografico=estado_geografico, ciudades_cobertura=ciudades_cobertura, zip_codes=zip_codes, zonas_no_trabajan=zonas_no_trabajan, cobran_extra_movil=(cobran_extra_movil == "true"), cuanto_extra=cuanto_extra,
        promocion_actual=promocion_actual, descuento_efectivo=descuento_efectivo, promo_adas=promo_adas, promo_referidos=promo_referidos, otra_promo=otra_promo,
        metodos_pago_json=metodos_pago_json if isinstance(metodos_pago_json, dict) else json.loads(metodos_pago_json), trabajan_aseguradoras=(trabajan_aseguradoras == "true"), aseguradoras_json=aseguradoras_json if isinstance(aseguradoras_json, dict) else json.loads(aseguradoras_json), manejan_deducibles=manejan_deducibles, como_cobran_claims=como_cobran_claims, aceptan_seguro_cita=(aceptan_seguro_cita == "true"),
        material_recibido=("material_recibido" in form), notas_material=notas_material, material_visual_json=material_visual_json,
        acepta_terminos=("acepta_terminos" in form),
        autoriza_cliente=True, autoriza_cliente_nombre=autoriza_cliente_nombre, autoriza_cliente_sello=autoriza_cliente_sello, autoriza_cliente_fecha=func.now(), autoriza_cliente_ip=client_ip,
    )
    db.add(registro); db.commit(); db.refresh(registro)
    enviar_correo_notificacion(registro)
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
        registro.estado = nuevo_estado; registro.status_changed_by = cambiado_por; registro.status_changed_at = datetime.now(); db.commit()
    return RedirectResponse(url=f"/onboarding/admin/view/{id_interno}?key={ADMIN_KEY}", status_code=303)
# Force deploy 10/18/2026 15:17:36

@router.post("/admin/edit/{id_interno}")
async def admin_edit(
    request: Request, id_interno: str, db: Session = Depends(get_db),
    nombre_negocio: Optional[str] = Form(None), telefono_negocio: Optional[str] = Form(None),
    email_cotizaciones: Optional[str] = Form(None), direccion_taller: Optional[str] = Form(None),
    ciudad: Optional[str] = Form(None), estado_negocio: Optional[str] = Form(None), codigo_postal: Optional[str] = Form(None),
    promocion_actual: Optional[str] = Form(None), descuento_efectivo: Optional[str] = Form(None),
    notas_material: Optional[str] = Form(None)
):
    key = request.query_params.get("key")
    if key != ADMIN_KEY: return HTMLResponse(content="Access Denied", status_code=403)

    registro = db.query(OnboardingOptiGlass).filter(OnboardingOptiGlass.id_interno == id_interno).first()
    if not registro:
        return HTMLResponse(content="Registro no encontrado", status_code=404)

    # Actualizar solo si vienen datos
    if nombre_negocio is not None: registro.nombre_negocio = nombre_negocio
    if telefono_negocio is not None: registro.telefono_negocio = telefono_negocio
    if email_cotizaciones is not None: registro.email_cotizaciones = email_cotizaciones
    if direccion_taller is not None: registro.direccion_taller = direccion_taller
    if ciudad is not None: registro.ciudad = ciudad
    if estado_negocio is not None: registro.estado_negocio = estado_negocio
    if codigo_postal is not None: registro.codigo_postal = codigo_postal
    if promocion_actual is not None: registro.promocion_actual = promocion_actual
    if descuento_efectivo is not None: registro.descuento_efectivo = descuento_efectivo
    if notas_material is not None: registro.notas_material = notas_material

    db.commit()
    
    # Redirigir de vuelta al historial (catálogo)
    return RedirectResponse(url=f"/onboarding/admin/history?key={ADMIN_KEY}", status_code=303)

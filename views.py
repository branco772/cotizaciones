from ast import FormattedValue
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
import traceback
import json
from django.http import JsonResponse
from datetime import datetime
import locale
from reportlab.lib.enums import TA_RIGHT
from materiales.models import Materiales
# Create your views here.
def cotizacion(request):
    materiales=Materiales.objects.all()
    return render(request, "cotizacion.html", {'materiales':materiales})
def materiales(request):
    mostrarMateriales= Materiales.objects.all()
    return render(request, "materiales.html",  {'mostrarMateriales': mostrarMateriales})
ULTIMA_FACTURA = 0
def generarPdf(request):
    global ULTIMA_FACTURA
    # Establecer el idioma local en español
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

    # Obtener la fecha actual con el formato deseado
    fecha_actual = datetime.now().strftime("%d de %B de %Y")
    if request.method == "POST":
        ULTIMA_FACTURA += 1
        print(request.POST)
        cliente= request.POST.get('cliente')
        direccion= request.POST.get('direccion')
        telefono= request.POST.get('telefono')
        ciudad= request.POST.get('ciudad')
        # crear un objeto PDF utilizando ReportLab
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'

        p=canvas.Canvas(response)
        p.drawImage("./logoitx.png", 10, 750, width=130, height=80)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(230, 820, "COTIZACIÓN")
        p.drawString(550, 820, "A- {}".format(ULTIMA_FACTURA))
        p.setFont("Helvetica", 10)
        p.drawString(450, 790, "Fecha: {}".format(fecha_actual))
        p.setFont("Helvetica", 10)
        p.drawString(170, 790, "ITX - Information Technology Experts")
        p.drawString(170, 770, "Servicios de tecnología, información")
        p.drawString(180, 760, "y telecomunicaciones en general")
        p.drawString(10, 725, "Atendiendo su amable solicitud estamos enviando cotización de los productos requeridos,")
        p.drawString(10, 705, "para nosotros es un placer poner nuestra empresa a su servicio.")
        #PRIMERA TABLA
        tabla1 = [
            ['CLIENTE', 'DIRECCIÓN', 'TELEFONO', 'CIUDAD'],
            [ '{}'.format(cliente), '{}'.format(direccion), '{}'.format(telefono), '{}'.format(ciudad)],
            ['COSTO DE EQUIPOS'],
        ]
        table = Table(tabla1, colWidths=[2*inch, 2*inch, 2*inch, 2*inch], rowHeights=[0.4*inch]*3)
        table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0, (0, 0, 0)),
            ('TEXTCOLOR', (0,0), (-1,-1), (0, 0, 0)),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
            ('BACKGROUND', (0, 2), (-1, 2), colors.dodgerblue),# Fondo gris para la fila de títulos
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('SPAN', (0, -1), (-1, -1)),
            ('WORDWRAP', (0, 0), (-1, -1), 1),
            ('FONTSIZE', (0, 1), (-1, 1), 7), 
        ]))
        doc = SimpleDocTemplate(response, pagesize=letter)
        doc.build([table])
        table.drawOn(p, 10, 610)    
        #AQUI RECIBO LA TABLA
        datos = request.POST.get('tabla_data')
        print(datos)
        # agregar los datos a la tabla
        datos = eval(datos) 
        table_data = [[
            "Descripción", "Cantidad", "Valor unitario", "Valor total"
        ]]
        for dato in datos:
            table_data.append([
            dato["descripcion"],
            dato["cantidad"],
            dato["vrunitario"],
            dato["vrtotal"],
            ])

        # crear la tabla y agregar los estilos
        tabledos = Table(table_data, colWidths=[2*inch, 2*inch, 2*inch, 2*inch])
        tabledos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            #('BACKGROUND', (0, 1), (-1, -1), colors.transparent),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements = []  
        doc2 = SimpleDocTemplate(response, pagesize=letter)
        # agregar la tabla al PDF
        elements.append(tabledos)
        
        # generar el PDF y enviarlo como respuesta
        doc2.build(elements)
        tabledos.drawOn(p, 10, 537)
        p.save()
        return response
        # Devolver una respuesta al navegador
    return render(request, 'cotizacion.html')


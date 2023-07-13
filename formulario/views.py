from django.http import HttpResponse
from django.shortcuts import render
from .models import Cliente
from datetime import datetime, date
import locale
import json
from .models import Cliente
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from materiales.models import Materiales
from ordentrabajo.views import Orden
# Create your views here.
def registro(request):
    return render(request, "mostrarRegistro.html")
ULTIMA_FACTURA = 0
def enviarformulario(request):
    global ULTIMA_FACTURA
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    # Obtener la fecha actual con el formato deseado
    fecha_actual = datetime.now().strftime("%d-%m-%Y")
    fecha_actua2 = datetime.now().strftime("%y%m")
    if request.method=="POST":
        ULTIMA_FACTURA += 1
        cliente= request.POST.get('cliente')
        direccion= request.POST.get('direccion')
        telefono= request.POST.get('telefono')
        ciudad= request.POST.get('ciudad')
        descripcionServicio=request.POST.get('descripcionServicio')
        descuento=request.POST.get('descuento')
        codigo="CT"+ fecha_actua2+"-{}".format(ULTIMA_FACTURA)
        print(codigo)
        contadorPosicion=0
        totalSuma=0
        des=totalSuma*(int(descuento)/100)
        precioDescuento=totalSuma-des
        mensaje_alerta=None
        # Obtener otros datos del POST
        datos_tabla = request.POST.get('tabla_data')
        if datos_tabla:
            data=json.loads(datos_tabla)
            for item in data:
                descripcion=item['descripcion']
                material = Materiales.objects.get(nombrematerial=descripcion)
                cantidad=item['cantidad']
                valorunitario=item['vrunitario']
                valortotal=item['vrtotal']
                contadorPosicion +=1
                totalSuma=totalSuma+int(valortotal)
                des=totalSuma*(int(descuento)/100)
                precioDescuento=totalSuma-des
                if material.stock< int(cantidad):
                    messages.add_message(request, level=messages.WARNING, message= f"¡Alerta! El material {material.nombrematerial} tiene un stock insuficiente.") 
                    print(f"¡Alerta! El material {material.nombrematerial} tiene un stock insuficiente.")
                    mensaje_alerta=f"¡Alerta! El material {material.nombrematerial} tiene un stock insuficiente."
                usuario = Cliente(cliente=cliente, direccion=direccion, telefono=telefono, ciudad=ciudad, descripcion=descripcion, cantidad=cantidad, valorunitario=valorunitario, valortotal=valortotal, descuento=descuento, codigo=codigo, fecha=date.today(), descripcionservicio=descripcionServicio, serviciototal=totalSuma, preciodescuento=precioDescuento, material=material)
                usuario.save()
        else:
            print('NO HAY DATOS')
        
        #DESDE AQUI GENERAREMOS EL PDF
        # crear un objeto PDF utilizando ReportLab
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="COTIZACION.pdf"'

        p=canvas.Canvas(response)
        p.drawImage("./static/itx.jpg", 10, 750, width=130, height=70)
        p.setFont("Helvetica-Bold", 15)
        p.drawString(170, 810, "COTIZACIÓN DE INFRAESTRUCTURA")
        #tabla CERO
        tablacero= [['COTIZACIÓN'],
                    ['CT'+ fecha_actua2+"-{}".format(ULTIMA_FACTURA)],
                    ['{}'.format(fecha_actual)]]
        table_style = [('GRID', (0, 0), (-1, -1), 1, 'black'),
                        ('BACKGROUND', (0, 0), (0, 0), colors.dodgerblue),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONT', (0, 1), (0, 1), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 1), (0, 1), 13),]
        table = Table(tablacero, style=table_style)
        doc = SimpleDocTemplate(response, pagesize=letter)
        doc.build([table])
        
        table.drawOn(p, 510, 770)
        
        #p.drawString(520, 820, "CT"+ fecha_actua2+"-{}".format(ULTIMA_FACTURA))
        #p.drawString(450, 790, "Fecha: {}".format(fecha_actual))
        p.setFont("Helvetica-Bold", 10)
        p.drawString(230, 790, "ITX - Information Technology Experts")
        p.setFont("Helvetica", 10)
        p.drawString(160, 780, "Servicios de tecnología, información y telecomunicaciones en general")
        p.setFont("Helvetica-Bold", 15)
        p.drawString(120, 730, "COTIZACIÓN DE DISPOSITIVOS DE SEGURIDAD")
        p.drawString(240, 710, "ELECTRÓNICA")
        #p.drawString(10, 705, "para nosotros es un placer poner nuestra empresa a su servicio.")
        #PRIMERA TABLA
        tabla1 = [
            ['CLIENTE', 'DIRECCIÓN', 'TELEFONO', 'CIUDAD'],
            [ Paragraph('{}'.format(cliente)), Paragraph( '{}'.format(direccion)), '{}'.format(telefono), '{}'.format(ciudad)],
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
            ('FONTSIZE', (0, 1), (-1, 1), 10), 
        ]))
        doc = SimpleDocTemplate(response, pagesize=letter)
        doc.build([table])
        
        table.drawOn(p, 10, 610)
        #INJERTO DE LA SEGUNDA TABLA
        table_data = [[
            "DESCRIPCIÓN", "CANTIDAD", "VALOR UNITARIO", "VALOR TOTAL"
        ]]
        datos=json.loads(datos_tabla)
        num_filas = len(datos) + 1 # +1 para la fila de encabezado
        print(num_filas)
        alturas_filas = [0.3*inch] * num_filas
        for dato in datos:
            table_data.append([
            dato["descripcion"],
            dato["cantidad"],
            dato["vrunitario"],
            dato["vrtotal"],
            ])
        tabledos = Table(table_data, colWidths=[2*inch, 2*inch, 2*inch, 2*inch], rowHeights=alturas_filas)
        tabledos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            #('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            #('BACKGROUND', (0, 1), (-1, -1), colors.transparent),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements = []  
        doc2 = SimpleDocTemplate(response, pagesize=letter)
        # agregar la tabla al PDF
        elements.append(tabledos)
        
        # generar el PDF y enviarlo como respuesta
        doc2.build(elements)
        if contadorPosicion==1:
            tabledos.drawOn(p, 10,560)
        else:
            if contadorPosicion==2:
                tabledos.drawOn(p, 10, 537)    
            else:
                if contadorPosicion==3:
                    tabledos.drawOn(p, 10, 514)
                else:
                    if contadorPosicion==4:
                        tabledos.drawOn(p, 10, 491)
                    else:
                        if contadorPosicion==5:
                            tabledos.drawOn(p, 10, 468)
                        else:
                            if contadorPosicion==6:
                                tabledos.drawOn(p, 10,445)
                            else:
                                if contadorPosicion==7:
                                    tabledos.drawOn(p, 10, 422)    
                                else:
                                    if contadorPosicion==8:
                                        tabledos.drawOn(p, 10, 399)
                                    else:
                                        if contadorPosicion==9:
                                            tabledos.drawOn(p, 10, 376)
                                        else:
                                            if contadorPosicion==10:
                                                tabledos.drawOn(p, 10, 353)
                                            else:
                                                if contadorPosicion==11:
                                                    tabledos.drawOn(p, 10,330)
                                                else:
                                                    if contadorPosicion==12:
                                                        tabledos.drawOn(p, 10, 307)    
                                                    else:
                                                        if contadorPosicion==13:
                                                            tabledos.drawOn(p, 10, 284)
                                                        else:
                                                            if contadorPosicion==14:
                                                                tabledos.drawOn(p, 10, 261)
                                                            else:
                                                                if contadorPosicion==15:
                                                                    tabledos.drawOn(p, 10, 238)
                                                                else:
                                                                    if contadorPosicion==16:
                                                                        tabledos.drawOn(p, 10, 215)
                                                                    else:
                                                                        if contadorPosicion==17:
                                                                            tabledos.drawOn(p, 10, 192)    
                                                                        else:
                                                                            if contadorPosicion==18:
                                                                                tabledos.drawOn(p, 10, 169)    
                                                                            
        #TERCERA TABLA
        tabla3 = [[Paragraph('{}'.format(descripcionServicio)), 'Costo Total en Bs.', '{}'.format(totalSuma)],
                ['', 'Costo con descuento: '+'{}'.format(descuento), '{}'.format(precioDescuento)],
                ['', 'Celda 6']]
        tablatres = Table(tabla3, colWidths=[4*inch, 2*inch, 2*inch], rowHeights=[1*inch, 0.5*inch, 0.2*inch])

        # Agregar estilo a la tabla
        estilo = TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # Color de letra negro en todas las celdas
                            ('BACKGROUND', (0, 0), (0, -1), colors.white),  # Fondo blanco en la primera columna
                            ('SPAN', (0, 0), (0, -1)),  # Hacer que la primera columna sea una sola celda
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),# Alinear todas las celdas al centro
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  # Fuente en negrita en todas las celdas
                            ('FONTSIZE', (0, 0), (-1, 0), 10),  # Tamaño de fuente 10 en la primera fila
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior en la primera fila
                            ('BACKGROUND', (1, 1), (-1, -1), colors.white),  # Fondo blanco en las demás celdas
                            ('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ('SPAN', (1, 1), (1, 2)),
                            ('SPAN', (2, 1), (2, 2)),
                            ('FITA', (0, 0), (-1, -1)),
                            ('SHRINK', (0, 0), (-1, -1)),
                            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                            ('VALIGN', (0, 0), (0, -1), 'TOP'),
                            ('WORDWRAP', (0, 0), (-1, -1), 'CJK'),
                            ('INERGRID', (0,0),(-1,-1),0.25, colors.black),
                            ('BOX',(0,0),(-1,-1),0.25,colors.black),])
                            
        tablatres.setStyle(estilo)

        # Agregar la tabla al documento
        contenido = []
        contenido.append(tablatres)
        doc.build(contenido)
        tablatres.drawOn(p, 10, 40)
        p.setFont("Helvetica", 7)
        p.drawString(200, 30, "Calle: Nueva Granada # 1541 Telf. (591) 67403647- (591) 4-4401633")
        p.drawString(250, 20, "E-mail: itx.servicios@gmail.com")
        p.drawString(260, 10, "Cochabamba - Bolivia")
        p.save()    
        return response
    return render(request, 'cotizacion.html', {'mensaje_alerta':mensaje_alerta})
    
# Definir una vista para mostrar los datos de la base de datos en una tabla
def mostrarRegistro(request):
    formularios= Cliente.objects.all()
    ordenes=Orden.objects.all()
    # Renderizar los datos en la vista
    return render(request, 'mostrarRegistro.html', {'formularios': formularios, 'ordenes': ordenes})


def delete(request, formulario):
    registro=Cliente.objects.get(id=formulario)
    registro.delete()
    formularios=Cliente.objects.all()
    return render(request, "mostrarRegistro.html", {'formularios': formularios})


def verificarMaterial(request):
    if request.method=="POST":
        descuento=request.POST.get('descuento')
        contadorPosicion=0
        totalSuma=0
        mensaje_alerta=None
        # Obtener otros datos del POST
        datos_tabla = request.POST.get('tabla_data')
        print(datos_tabla)
        if datos_tabla:
            data=json.loads(datos_tabla)
            for item in data:
                descripcion=item['descripcion']
                material = Materiales.objects.get(nombrematerial=descripcion)
                cantidad=item['cantidad']
                valorunitario=item['vrunitario']
                valortotal=item['vrtotal']
                contadorPosicion +=1
                totalSuma=totalSuma+int(valortotal)
                des=totalSuma*(int(descuento)/100)
                precioDescuento=totalSuma-des
                if material.stock< int(cantidad):
                    messages.add_message(request, level=messages.WARNING, message= f"¡Alerta! El material {material.nombrematerial} tiene un stock insuficiente.") 
                    print(f"¡Alerta! El material {material.nombrematerial} tiene un stock insuficiente.")
                    mensaje_alerta=f"¡Alerta! El material {material.nombrematerial} tiene un stock insuficiente."
            des=totalSuma*(int(descuento)/100)
            precioDescuento=totalSuma-des
        else:
            print('NO HAY DATOS')
    return render(request, 'cotizacion.html', {'mensaje_alerta':mensaje_alerta})    
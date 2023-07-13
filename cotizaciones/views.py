from django.shortcuts import render
from django.http import HttpResponse
from .models import Cliente

def crearUsuario(request):
    if request.method == 'POST':
        cliente= request.POST.get('cliente')
        direccion= request.POST.get('direccion')
        telefono= request.POST.get('telefono')
        ciudad= request.POST.get('ciudad')
        # Obtener otros datos del POST

        usuario = Cliente(cliente=cliente, direccion=direccion, telefono=telefono, ciudad=ciudad)
        # Crear el objeto Usuario con los datos recibidos

        usuario.save()
        # Guardar el objeto Usuario en la base de datos
        print("se guardo")
        return HttpResponse('Usuario creado exitosamente')
    else:
        return render(request, 'materiales.html')

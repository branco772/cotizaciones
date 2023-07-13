from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import JsonResponse
from .models import Materiales, MaterialForm
from django.contrib import messages
# Create your views here.


def materiales(request):
    mostrarMateriales= Materiales.objects.all()
    return render(request, "materiales.html",  {'mostrarMateriales': mostrarMateriales})

def registrarMaterial(request):
    if request.method=="POST": 
        nombreMaterial=request.POST.get('nombre')
        modeloMaterial=request.POST.get('modelo')
        tipoMedida=request.POST.get('tipoMedida')
        cantidad=request.POST.get('cantidad')
        costoMaterial=request.POST.get('costoMaterial')
        stock=request.POST.get('stock')
        registrarMaterial=Materiales(nombrematerial=nombreMaterial, modelomaterial=modeloMaterial, tipomedida=tipoMedida, cantidad=cantidad, costomaterial=costoMaterial, stock=stock)
        registrarMaterial.save()
        mostrarMateriales= Materiales.objects.all()
        return render(request, 'materiales.html',  {'mostrarMateriales': mostrarMateriales})
    else:
        print('no se envio')

def mostrarMaterial(request):
    mostrarMateriales= Materiales.objects.all()
    return render(request, 'materiales.html',  {'mostrarMateriales': mostrarMateriales})

def editarRegistro(request, mostrarMaterial):
    material = Materiales.objects.get(id=mostrarMaterial)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('materiales')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'editarRegistro.html', {'form': form})


def eliminarRegistro(request, mostrarMaterial):
    registro=Materiales.objects.get(id=mostrarMaterial)
    registro.delete()
    messages.success(request, 'El registro se eliminó exitosamente.')
    registro=Materiales.objects.all()
    return render(request, "materiales.html")


    """
    def actualizarRegistro(request, mostrarMaterial):
    material=Materiales.objects.get(pk=mostrarMaterial)
    form=MaterialForm(request.POST, instance=material)
    if form.is_valid():
        form.save()
    return render(request, 'materiales.html')
    """
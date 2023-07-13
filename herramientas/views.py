from django.shortcuts import render, redirect
from herramientas.models import Herramienta, HerramientaForm
# Create your views here.
def herramientas(request):
    mostrarHerramientas= Herramienta.objects.all()
    return render(request, 'herramientas.html', {'mostrarHerramientas':mostrarHerramientas})

def registrarHerramienta(request):
    if request.method=="POST": 
        nombreMaterial=request.POST.get('nombre')
        modeloMaterial=request.POST.get('modelo')
        cantidad=request.POST.get('cantidad')
        registrarMaterial= Herramienta(nombrematerial=nombreMaterial, modelomaterial=modeloMaterial, cantidad=cantidad)
        registrarMaterial.save()
        mostrarHerramientas= Herramienta.objects.all()
        return render(request, 'herramientas.html', {'mostrarHerramientas':mostrarHerramientas})
    else:
        print('no se envio')


def mostrarHerramienta(request):
    mostrarHerramientas= Herramienta.objects.all()
    return render(request, 'herramientas.html',  {'mostrarHerramientas': mostrarHerramientas})

def editarHerramienta(request, mostrarHerramienta):
    material = Herramienta.objects.get(id=mostrarHerramienta)
    if request.method == 'POST':
        form = HerramientaForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('herramientas')
    else:
        form = HerramientaForm(instance=material)
    mostrarHerramientas= Herramienta.objects.all()
    return render(request, 'editarHerramienta.html', {'form': form, 'mostrarHerramientas': mostrarHerramientas})


def eliminarHerramienta(request, mostrarHerramienta):
    registro=Herramienta.objects.get(id=mostrarHerramienta)
    registro.delete()
    mostrarHerramientas=Herramienta.objects.all()
    return render(request, "herramientas.html",  {'mostrarHerramientas': mostrarHerramientas})
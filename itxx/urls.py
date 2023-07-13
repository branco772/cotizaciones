"""
URL configuration for itxx project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from views import cotizacion
from materiales.views import materiales, mostrarMaterial, registrarMaterial, eliminarRegistro, editarRegistro
from views import generarPdf
from formulario.views import enviarformulario, mostrarRegistro, delete, verificarMaterial
from cotizaciones.views import crearUsuario
from ordentrabajo.views import registroOrden, enviarformularioOrden, buscarcotizaciones
from herramientas.views import herramientas, registrarHerramienta, mostrarHerramienta, editarHerramienta, eliminarHerramienta
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cotizacion, name="cotizacion"),
    path('materiales/', materiales, name='materiales'),
    path('registrarMaterial/', registrarMaterial, name='registrarMaterial'),
    path('mostrarMaterial/', mostrarMaterial, name='mostrarMaterial'),
    path('mostrarMaterial/eliminarRegistro/<int:mostrarMaterial>/', eliminarRegistro, name='eliminarRegistro'),
    path('editarRegistro/<int:mostrarMaterial>/',  editarRegistro, name='editarRegistro'),
    path('generarPdf/', generarPdf, name='generarPdf'),
    path('enviarformulario/', enviarformulario, name='enviarformulario'),
    path('crearUsuario/', crearUsuario, name='crearUsuario'),
    path('mostrarRegistro/', mostrarRegistro, name='mostrarRegistro'),
    path('eliminarRegistroForm/<int:formulario>/', delete, name='delete'),
    path('registroOrden/', registroOrden, name='registroOrden'),
    path('enviarformularioOrden/', enviarformularioOrden, name='enviarformularioOrden'),
    path('herramientas/', herramientas, name='herramientas'),
    path('registrarHerramienta/', registrarHerramienta, name='registrarHerramienta'),
    path('mostrarHerramienta/', mostrarHerramienta, name='mostrarHerramienta'),
    path('editarHerramienta/<int:mostrarHerramienta>/',  editarHerramienta, name='editarHerramienta'),
    path('eliminarHerramienta/<int:mostrarHerramienta>/', eliminarHerramienta, name='eliminarHerramienta'),
    path('buscarcotizaciones/', buscarcotizaciones, name='buscarcotizaciones'),
    path('verificarMaterial/', verificarMaterial, name='verificarMaterial'),
]

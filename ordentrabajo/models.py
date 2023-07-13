from django.db import models
from materiales.models import Materiales
# Create your models here.
class Orden(models.Model):
    cliente=models.CharField(max_length=100)
    direccion=models.CharField(max_length=100)
    telefono=models.CharField(max_length=8)
    ciudad=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=100)
    cantidad=models.IntegerField()
    valorunitario=models.IntegerField()
    valortotal=models.IntegerField()
    descuento=models.IntegerField()
    codigo=models.CharField(max_length=999999)
    fecha=models.DateField()
    descripcionservicio=models.CharField(max_length=100)
    serviciototal=models.IntegerField()
    preciodescuento=models.IntegerField()
    materialutilizado = models.ForeignKey(Materiales, on_delete=models.CASCADE)
    cantidadutilizado = models.PositiveIntegerField()
    class Meta:
        db_table = 'ordenTrabajo'
# Create your models here.

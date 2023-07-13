from django.db import models

# Create your models here.
class Cliente(models.Model):
    cliente=models.CharField(max_length=100)
    direccion=models.CharField(max_length=100)
    telefono=models.CharField(max_length=8)
    ciudad=models.CharField(max_length=50)
class CostoEquipos(models.Model):
    descripcion=models.CharField(max_length=100)
    cantidad=models.IntegerField()
    valorunitario=models.IntegerField()
    valortotal=models.IntegerField()
class Opcionales(models.Model):
    descripciono=models.CharField(max_length=100)
    cantidado=models.IntegerField()
    valorunitarioo=models.IntegerField()
    valortotalo=models.IntegerField()
    descuento=models.IntegerField()
    valorTotalIva=models.IntegerField()
    
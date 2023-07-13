
from django.db import models
from django import forms
# Create your models here.


class Materiales(models.Model):
    nombrematerial = models.CharField(max_length=1000)
    modelomaterial = models.CharField(max_length=1000)
    tipomedida=models.CharField(max_length=1000)
    cantidad = models.IntegerField()
    costomaterial=models.IntegerField()
    stock = models.IntegerField()

    class Meta:
        db_table = 'material'

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Materiales
        fields = ['nombrematerial', 'modelomaterial', 'tipomedida', 'cantidad', 'costomaterial', 'stock']
        
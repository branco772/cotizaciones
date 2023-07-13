from django.db import models
from django import forms
# Create your models here.
class Herramienta(models.Model):
    nombrematerial = models.CharField(max_length=1000)
    modelomaterial = models.CharField(max_length=1000)
    cantidad = models.IntegerField()

    class Meta:
        db_table = 'herramientas'

class HerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ['nombrematerial', 'modelomaterial', 'cantidad']
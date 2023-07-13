# Generated by Django 4.2 on 2023-05-11 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0003_materiales_modelomaterial'),
        ('formulario', '0002_cliente_descripcionservicio_cliente_preciodescuento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='material',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='materiales.materiales'),
            preserve_default=False,
        ),
    ]
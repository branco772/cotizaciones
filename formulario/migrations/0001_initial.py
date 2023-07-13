# Generated by Django 4.2 on 2023-04-28 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=8)),
                ('ciudad', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
                ('cantidad', models.IntegerField()),
                ('valorunitario', models.IntegerField()),
                ('valortotal', models.IntegerField()),
                ('descuento', models.IntegerField()),
                ('codigo', models.CharField(max_length=999999)),
                ('fecha', models.DateField()),
            ],
            options={
                'db_table': 'formulario',
            },
        ),
    ]
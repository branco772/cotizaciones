# Generated by Django 4.2 on 2023-06-05 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Herramienta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombrematerial', models.CharField(max_length=1000)),
                ('modelomaterial', models.CharField(max_length=1000)),
                ('cantidad', models.IntegerField()),
            ],
            options={
                'db_table': 'herramientas',
            },
        ),
    ]

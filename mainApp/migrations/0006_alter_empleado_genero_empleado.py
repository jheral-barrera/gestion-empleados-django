# Generated by Django 4.2.6 on 2023-11-07 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0005_perfil_rut_perfil_alter_perfil_tipo_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='genero_empleado',
            field=models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')], max_length=20),
        ),
    ]

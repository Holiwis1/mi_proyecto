# Generated by Django 5.0.3 on 2024-04-09 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_remove_cliente_fecha_alta_alter_empleado_fecha_alta_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='foto_dni',
            field=models.FileField(blank=True, null=True, upload_to='dnis/'),
        ),
    ]
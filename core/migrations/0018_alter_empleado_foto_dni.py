# Generated by Django 5.0.3 on 2024-04-09 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_empleado_foto_dni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='foto_dni',
            field=models.ImageField(blank=True, null=True, upload_to='dnis/'),
        ),
    ]

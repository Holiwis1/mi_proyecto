# Generated by Django 5.0.3 on 2024-04-03 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_empleado_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='imagen',
            field=models.ImageField(upload_to='photos'),
        ),
    ]

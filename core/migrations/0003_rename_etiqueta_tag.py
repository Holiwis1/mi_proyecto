# Generated by Django 5.0.3 on 2024-06-20 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_tareas_cliente_tareas_cliente'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Etiqueta',
            new_name='Tag',
        ),
    ]
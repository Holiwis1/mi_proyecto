# Generated by Django 5.0.3 on 2024-05-14 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_notas_remove_etiqueta_color_proyecto_fecha_cobro_iva_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Etiqueta',
        ),
        migrations.AlterField(
            model_name='ticketattachment',
            name='file',
            field=models.FileField(upload_to='ticket_attachments/'),
        ),
    ]
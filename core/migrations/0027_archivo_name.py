# Generated by Django 5.0.3 on 2024-04-22 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_alter_archivo_archivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivo',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.0.3 on 2024-06-06 10:29

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('nombre_comercial', models.CharField(blank=True, max_length=120, null=True)),
                ('nif', models.CharField(blank=True, max_length=9, null=True)),
                ('tipo', models.CharField(blank=True, choices=[('empresa', 'Empresa'), ('particular', 'Particular'), ('proveedor', 'Proveedor'), ('leads', 'Leads')], default='empresa', max_length=120, null=True)),
                ('razon_social', models.CharField(blank=True, max_length=120, null=True)),
                ('telefono', models.IntegerField(blank=True, null=True)),
                ('telefono2', models.IntegerField(blank=True, null=True)),
                ('direccion', models.CharField(blank=True, max_length=120, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('notas', models.TextField(blank=True, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('web', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', models.CharField(default='#007bff', max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=120)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('fecha_creación', models.DateField(auto_now_add=True, null=True)),
                ('fecha_editado', models.DateField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('header_color', models.CharField(default='#ffffff', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('rol', models.CharField(choices=[('admin', 'Administrador'), ('empleado', 'Empleado'), ('ventas', 'Ventas'), ('marketing', 'Marketing'), ('redes_sociales', 'Redes Sociales'), ('desarrollo', 'Desarrollo')], default='admin', max_length=120, null=True)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('telefono', models.IntegerField(blank=True, null=True)),
                ('direccion', models.CharField(blank=True, max_length=120, null=True)),
                ('num_seguridad_social', models.IntegerField(blank=True, null=True)),
                ('telefono2', models.IntegerField(blank=True, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('foto_dni', models.ImageField(blank=True, null=True, upload_to='dnis/')),
                ('foto_dni2', models.ImageField(blank=True, null=True, upload_to='dnis/')),
                ('fecha_alta', models.DateField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('fecha_inicio', models.DateField(blank=True, null=True)),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('num_acuerdo', models.IntegerField(blank=True, null=True)),
                ('prioridad', models.CharField(blank=True, choices=[('alta', 'Alta'), ('muy_alta', 'Muy Alta'), ('media', 'Media'), ('baja', 'Baja'), ('muy_baja', 'Muy Baja'), ('sin_prioridad', 'Sin Prioridad')], default='sin_prioridad', max_length=120, null=True)),
                ('estado', models.CharField(blank=True, choices=[('pendiente', 'Pendiente'), ('activo', 'Activo'), ('finalizado', 'Finalizado'), ('cancelado', 'Cancelado'), ('permanente', 'Permanente')], default='pendiente', max_length=120, null=True)),
                ('valor', models.IntegerField(blank=True, null=True)),
                ('tipo', models.CharField(blank=True, choices=[('1ª Justificacion', '1ª Justificacion'), ('2ª Justificacion', '2ª Justificacion'), ('Acuerdos', 'Acuerdos'), ('Diseño Gráfico', 'Diseño Gráfico'), ('E-Commerce', 'E-Commerce'), ('Factura electrónica', 'Factura electrónica'), ('Gestión Clientes', 'Gestión Clientes'), ('Gestión Procesos', 'Gestión Procesos'), ('Kit Digital', 'Kit Digital'), ('Marketing', 'Marketing'), ('Solicitud KD', 'Solicitud KD'), ('Redes Sociales', 'Redes Sociales'), ('SEO', 'SEO'), ('Web', 'Web'), ('TPV', 'TPV'), ('Diseño Gráfico', 'Diseño Gráfico'), ('URL', 'URL')], max_length=120, null=True)),
                ('firma_acuerdo', models.DateField(blank=True, null=True)),
                ('fecha_facturacion', models.DateField(blank=True, null=True)),
                ('num_factura', models.IntegerField(blank=True, null=True)),
                ('fecha_cobro_IVA', models.DateField(blank=True, null=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.cliente')),
                ('empleados', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tareas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('fecha_inicio', models.DateField(blank=True, null=True)),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('prioridad', models.CharField(blank=True, choices=[('alta', 'Alta'), ('muy_alta', 'Muy Alta'), ('media', 'Media'), ('baja', 'Baja'), ('muy_baja', 'Muy Baja'), ('sin_prioridad', 'Sin Prioridad')], default='sin_prioridad', max_length=120, null=True)),
                ('estado', models.CharField(blank=True, choices=[('pendiente', 'Pendiente'), ('activo', 'Activo'), ('finalizado', 'Finalizado'), ('cancelado', 'Cancelado'), ('permanente', 'Permanente')], default='pendiente', max_length=120, null=True)),
                ('Cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.cliente')),
                ('empleado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('proyecto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='core.table')),
            ],
        ),
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='archivos_clientes/')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='archivos', to='core.cliente')),
                ('Proyecto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='archivos', to='core.proyecto')),
                ('Tareas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='archivos', to='core.tareas')),
                ('tickets', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='archivos', to='core.ticket')),
            ],
        ),
        migrations.CreateModel(
            name='TicketAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='ticket_attachments/')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='core.ticket')),
            ],
        ),
    ]

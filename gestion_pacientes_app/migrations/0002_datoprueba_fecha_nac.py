# Generated by Django 5.2.1 on 2025-05-12 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_pacientes_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datoprueba',
            name='fecha_nac',
            field=models.DateTimeField(null=True),
        ),
    ]

# Generated by Django 3.0.4 on 2020-04-03 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='remito',
            options={'ordering': ['-Fecha'], 'verbose_name': 'Remito', 'verbose_name_plural': 'Remitos'},
        ),
        migrations.AlterField(
            model_name='certificaciones',
            name='Fecha',
            field=models.DateField(help_text='Ingresar Fecha con Formato MM/DD/AA'),
        ),
        migrations.AlterField(
            model_name='movimientos',
            name='Remito',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_movimientos', to='Inventory.Remito'),
        ),
    ]

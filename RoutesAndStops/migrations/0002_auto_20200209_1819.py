# Generated by Django 2.2.4 on 2020-02-09 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoutesAndStops', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='direction',
            field=models.CharField(choices=[('UP', 'UP'), ('Down', 'Down')], max_length=10, verbose_name='Direction'),
        ),
        migrations.AlterField(
            model_name='route',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=10, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='route',
            name='type',
            field=models.CharField(choices=[('AC', 'AC'), ('General', 'General')], max_length=10, verbose_name='Type'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-18 21:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0002_auto_20160918_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='ofertas',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='personas.Oferta'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='empresa',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='personas.Empresa'),
        ),
    ]

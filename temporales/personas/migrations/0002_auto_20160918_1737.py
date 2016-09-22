# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-18 17:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='oferta',
            name='nombre',
            field=models.CharField(default='no name', max_length=250, verbose_name='nombre oferta'),
        ),
        migrations.AddField(
            model_name='salario',
            name='nombre',
            field=models.CharField(default='no name', max_length=250, verbose_name='nombre salario'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='nombre',
            field=models.CharField(default='no name', max_length=250, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='nombre',
            field=models.CharField(default='no name', max_length=250, verbose_name='nombre'),
        ),
    ]

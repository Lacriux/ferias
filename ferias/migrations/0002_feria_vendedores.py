# Generated by Django 3.2.7 on 2021-10-18 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feria',
            name='vendedores',
            field=models.ManyToManyField(to='ferias.Vendedor'),
        ),
    ]
